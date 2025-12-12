import base64
import datetime
import json
import os
from typing import Any, Dict, Tuple

import requests
from boto3 import Session
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

from annotate.environment_utils import is_buildkite_itests
from annotate.users_service import UsersService
from annotate.util_no_dependencies import UtilNoDependencies


class ServiceTokenService:
    url: str
    session: requests.sessions
    user_service: UsersService

    STS_SIGNED_REQUEST_EXP_HEADER_NAME = "X-Bnch-Exp"
    STS_SIGNED_REQUEST_EXP_S = 60
    STS_SIGNED_REQUEST_REGION_HEADER_NAME = "X-Bnch-Sts-Region"
    STS_SIGNATURE_HEADER_NAME = "X-Bnch-Sts-Signed-Headers-V1"

    STS_SIGNATURE_VERIFICATION_HEADER_KEYS = [
        STS_SIGNED_REQUEST_EXP_HEADER_NAME,
        STS_SIGNED_REQUEST_REGION_HEADER_NAME,
        "X-Amz-Security-Token",
        "X-Amz-Date",
        "Authorization",
    ]

    token_cache: Dict[str, Tuple[str, datetime.datetime]]

    @staticmethod
    def _token_issuer_uri() -> str:
        if os.environ.get('TOKEN_ISSUER_URI'):
            return os.environ['TOKEN_ISSUER_URI']
        elif is_buildkite_itests():
            return f"https://token-issuer.int.{os.environ['BNCH_SERVICE_STACK']}.{os.environ['BNCH_SERVICE_ACCOUNT']}.bnch.services"
        else:
            return 'http://token-issuer.token-issuer.svc.cluster.local'

    def __init__(self, url: str, session: requests.sessions):
        self.url = f'{url}/api/v2'
        self.session = session
        self.user_service = UsersService(url, session)
        self.token_cache = {}

    def _vend_admin_internal_token_from_buildkite(
            self, oidc_token: str, subject: str, benchling_details: dict[str, Any]
    ) -> str:
        vend_headers = {'content-type': 'application/json', 'Authorization': f"Bearer {oidc_token}"}
        vend_body = {
            'client_id': 'buildkite',
            'subject': subject,
            'subject_type': 'pipebio',
            'audience': 'buildkite',
            'tenant_guid': benchling_details['tenantId'],
            'tenant_subdomain': benchling_details['tenantSubdomain'],
        }

        vend_response = self.session.post(
            url=f'{self._token_issuer_uri()}/api/v1/vend_admin_internal_token_for_buildkite',
            headers=vend_headers,
            json=vend_body,
            timeout=10,  # seconds
        )
        UtilNoDependencies.raise_detailed_error(vend_response)

        return vend_response.json()["token"]

    def _exchange_admin_internal_token_for_internal_auth_token(self, admin_internal_token: str, service: str) -> str:
        exchange_headers = {'content-type': 'application/json'}
        sts_headers = self.get_sts_signed_headers(os.environ.get('AWS_REGION') or 'us-east-1')
        exchange_headers[self.STS_SIGNATURE_HEADER_NAME] = base64.b64encode(json.dumps(sts_headers).encode()).decode()
        exchange_headers['X-Bnch-Token-For-Exchange'] = admin_internal_token

        exchange_body = {'client_id': 'buildkite', 'audience': service}

        exchange_response = self.session.post(
            url=f'{self._token_issuer_uri()}/api/v1/exchange_for_internal_access_token',
            headers=exchange_headers,
            json=exchange_body,
            timeout=10,  # seconds
        )
        UtilNoDependencies.raise_detailed_error(exchange_response)

        return exchange_response.json()["token"]

    def vend_internal_token_for_buildkite(self, user_id: str, service: str = 'pipebio-dataproc') -> str:
        benchling_details = self.user_service.get_benchling_details()
        if benchling_details is None:
            raise Exception('No benchling_details found')

        admin_internal_token = self._vend_admin_internal_token_from_buildkite(
            oidc_token=os.environ['BUILDKITE_S2S_OIDC_TOKEN'], subject=user_id, benchling_details=benchling_details
        )

        return self._exchange_admin_internal_token_for_internal_auth_token(
            admin_internal_token=admin_internal_token, service=service
        )

    def vend_internal_token(self, user_id: str, service: str = 'pipebio-dataproc', tenant_id: str = "", tenant_subdomain: str = "") -> str:
        cache_key = f'{user_id}:{service}'
        if cache_key in self.token_cache:
            token, expiration = self.token_cache[cache_key]
            if datetime.datetime.now(datetime.timezone.utc) < expiration:
                # Return cached token if it is not expired.
                print(
                    f'[ServiceTokenService:vend_internal_token] Using cached token for {user_id} and service {service}, expires at {expiration}'
                )
                return token

        headers = {
            'content-type': 'application/json'
        }

        is_local_dev = os.environ.get('LOCAL_DEVELOPMENT', False)
        if is_local_dev:
            sts_region = os.environ.get('BNCH_REGION_NAME', None)
            sts_headers = self.get_sts_signed_headers(sts_region)
            if sts_headers is not None:
                headers[self.STS_SIGNATURE_HEADER_NAME] = base64.b64encode(json.dumps(sts_headers).encode()).decode()

        client_id = 'local-dev' if is_local_dev else 'pipebio'

        body = {
            'client_id': client_id,
            'subject': user_id,
            'subject_type': 'pipebio',
            'audience': service,
            'tenant_guid': tenant_id,
            'tenant_subdomain': tenant_subdomain,
        }

        response = self.session.post(url=f'{self._token_issuer_uri()}/api/v1/vend_internal_token',
                                     headers=headers,
                                     json=body)

        UtilNoDependencies.raise_detailed_error(response)

        response_json = response.json()
        token = response_json['token']

        now = datetime.datetime.now(datetime.timezone.utc)
        # Expected to be 15min.
        expires_in = datetime.timedelta(seconds=response_json['expires_in'])
        # Expire the token slightly early to be sure it's never really expired when used.
        safety_factor = datetime.timedelta(minutes=2)
        expiration = now + expires_in - safety_factor
        # Cache the token and its expiration time - also overwrites existing tokens
        self.token_cache[cache_key] = (token, expiration)
        print(
            f'[ServiceTokenService:vend_internal_token] Cached and returned token for {user_id} and service {service}, expires at {expiration}'
        )
        return token

    def get_sts_signed_headers(self, sts_region):
        sts_url = 'https://sts.amazonaws.com' if sts_region is None else f'https://sts.{sts_region}.amazonaws.com'

        sts_request_headers = {
            'User-Agent': 'bnch-sts-auth/1.0',
            'Host': 'sts.amazonaws.com',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            self.STS_SIGNED_REQUEST_REGION_HEADER_NAME: sts_region,
            self.STS_SIGNED_REQUEST_EXP_HEADER_NAME: str(
                datetime.datetime.now(datetime.timezone.utc).timestamp() + self.STS_SIGNED_REQUEST_EXP_S
            )
        }
        try:
            sts_request = AWSRequest(
                method='POST',
                url=sts_url,
                headers=sts_request_headers,
                data=b'Action=GetCallerIdentity&Version=2011-06-15',
            )

            session = Session()
            region_name = 'us-east-1' if sts_region is None else sts_region
            signer = SigV4Auth(credentials=session.get_credentials(),
                               region_name=region_name,
                               service_name='sts')
            signer.add_auth(sts_request)

            print(f'get_sts_signed_headers: signed request headers for {sts_region}')
            return {k: sts_request.headers[k] for k in self.STS_SIGNATURE_VERIFICATION_HEADER_KEYS}

        except Exception as e:
            print(f'[ServiceTokenService:get_sts_signed_headers] Error: {e}')
            return None


def set_sts_token(benchling_user_id: str, url: str, service='pipebio', tenant_id: str = "", tenant_subdomain: str = ""):
    service_token_service = ServiceTokenService(url, requests.session())
    os.environ['BENCHLING_S2S_TOKEN'] = service_token_service.vend_internal_token_for_buildkite(
        benchling_user_id,
        service
    ) \
        if is_buildkite_itests() \
        else service_token_service.vend_internal_token(
        benchling_user_id,
        service,
        tenant_id,
        tenant_subdomain
    )
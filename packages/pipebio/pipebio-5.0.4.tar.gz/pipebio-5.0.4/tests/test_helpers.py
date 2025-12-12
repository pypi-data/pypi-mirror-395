from pipebio.pipebio_client import PipebioClient


def get_adimab_vh_id(client:PipebioClient) -> int:
    return 2324904 if client.is_aws else 1083832

def get_project_id(client:PipebioClient) -> str:
    return '0bc60f88-3444-49be-a5f7-117f4bfedbc4' if client.is_aws else 'e0d0c886-a294-44d5-89bd-02d471cfbfc2'

def get_parent_id(client:PipebioClient) -> int:
    """
    e.g. group test results together so we can easily delete them in PipeBio UI.
    """
    return 2402463 if client.is_aws else None
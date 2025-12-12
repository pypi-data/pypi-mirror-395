import pytest
from unittest.mock import patch, MagicMock
from pipebio.pipebio_client import PipebioClient


class TestPipeBioClient:

    def test_get_user(self):
        """Test getting user information."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "firstName": "Test",
            "lastName": "User",
            "orgs": [{"id": "test-org-id"}]
        }

        with patch('requests_toolbelt.sessions.BaseUrlSession') as mock_session_class, \
             patch.dict('os.environ', {'PIPE_API_KEY': 'test-key'}):
            
            # Create a mock session instance
            mock_session = MagicMock()
            mock_session.get.return_value = mock_response
            mock_session_class.return_value = mock_session
            
            # Create the client and test
            client = PipebioClient(url='https://test-api.pipebio.com')
            result = client.get_user()
            
            assert result["firstName"] == "Test"
            assert result["lastName"] == "User"
            assert mock_session.get.call_args_list[-1].args[0] == 'me'

    def test_upload_file(self):
        """Test file upload functionality."""
        # Create separate mock responses for each API call
        mock_aws_response = MagicMock()
        mock_aws_response.status_code = 200
        mock_aws_response.json.return_value = {"stack": "test-stack"}

        mock_user_response = MagicMock()
        mock_user_response.status_code = 200
        mock_user_response.json.return_value = {
            "firstName": "Test",
            "lastName": "User",
            "org": {"id": "test-org-id"}
        }

        with patch('requests_toolbelt.sessions.BaseUrlSession') as mock_session_class, \
             patch.dict('os.environ', {'PIPE_API_KEY': 'test-key'}):
            
            # Set up session mock with different responses for different endpoints
            mock_session = MagicMock()
            mock_session.get.side_effect = lambda url: mock_aws_response if 'debug/about' in url else mock_user_response
            mock_session_class.return_value = mock_session
            
            # Create client
            client = PipebioClient(url='https://test-api.pipebio.com')
            
            # Mock the jobs component
            with patch.object(client.jobs, 'create_signed_upload') as mock_create_upload, \
                 patch.object(client.jobs, 'upload_data_to_signed_url') as mock_upload:
                
                mock_create_upload.return_value = {
                    "data": {
                        "url": "https://test-upload-url.com",
                        "headers": {"test": "header"},
                        "job": {"id": "test-job-id"}
                    }
                }
                
                result = client.upload_file(
                    file_name="test.txt",
                    absolute_file_location="test.txt",
                    parent_id=123,
                    project_id="test-project"
                )
                
                assert result["id"] == "test-job-id"
                assert mock_create_upload.call_count == 1
                assert mock_upload.call_count == 1 
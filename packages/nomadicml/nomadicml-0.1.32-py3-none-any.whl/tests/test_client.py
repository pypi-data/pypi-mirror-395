"""
Tests for the NomadicML client.
"""

import pytest
from unittest.mock import patch, MagicMock, ANY

from nomadicml import NomadicML
from nomadicml.exceptions import ValidationError, AuthenticationError, APIError


class TestNomadicMLClient:
    """Test cases for the NomadicML client."""
    
    def test_init_with_valid_api_key(self):
        """Test initialization with a valid API key."""
        client = NomadicML(api_key="valid_api_key")
        assert client.api_key == "valid_api_key"
        assert client.base_url == "https://fdixgrmuam.us-west-2.awsapprunner.com"
        assert client.timeout == 900
        assert client.collection_name == "videos"
        assert hasattr(client, "video")
    
    def test_init_with_invalid_api_key(self):
        """Test initialization with an invalid API key."""
        with pytest.raises(ValidationError):
            NomadicML(api_key="")
    
    def test_init_with_custom_base_url(self):
        """Test initialization with a custom base URL."""
        client = NomadicML(api_key="valid_api_key", base_url="http://localhost:8099")
        assert client.base_url == "http://localhost:8099"
    
    def test_init_with_custom_timeout(self):
        """Test initialization with a custom timeout."""
        client = NomadicML(api_key="valid_api_key", timeout=60)
        assert client.timeout == 60
    
    def test_init_with_custom_collection_name(self):
        """Test initialization with a custom collection name."""
        client = NomadicML(api_key="valid_api_key", collection_name="custom_videos")
        assert client.collection_name == "custom_videos"
    
    @patch("requests.Session.request")
    def test_make_request_success(self, mock_request):
        """Test _make_request with a successful response."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "success"}
        mock_request.return_value = mock_response
        
        client = NomadicML(api_key="valid_api_key")
        response = client._make_request("GET", "/test")
        
        assert response == mock_response
        mock_request.assert_called_once_with(
            method="GET",
            url="https://fdixgrmuam.us-west-2.awsapprunner.com/test",
            headers={'X-Request-ID': ANY},
            params=None,
            data=None,
            json=None,
            files=None,
            timeout=900,
        )
    
    @patch("requests.Session.request")
    def test_make_request_auth_error(self, mock_request):
        """Test _make_request with an authentication error."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_request.return_value = mock_response
        
        client = NomadicML(api_key="invalid_api_key")
        with pytest.raises(AuthenticationError):
            client._make_request("GET", "/test")
    
    @patch("requests.Session.request")
    def test_make_request_api_error(self, mock_request):
        """Test _make_request with an API error."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"detail": "Internal server error"}
        mock_request.return_value = mock_response
        
        client = NomadicML(api_key="valid_api_key")
        with pytest.raises(APIError) as exc_info:
            client._make_request("GET", "/test")
        
        assert exc_info.value.status_code == 500
        assert "Internal server error" in str(exc_info.value)
    
    @patch("nomadicml.client.NomadicML._make_request")
    def test_verify_auth(self, mock_make_request):
        """Test verify_auth method."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"valid": True, "user_id": "test_user"}
        mock_make_request.return_value = mock_response
        
        client = NomadicML(api_key="valid_api_key")
        result = client.verify_auth()
        
        assert result == {"valid": True, "user_id": "test_user"}
        mock_make_request.assert_called_once_with("POST", "/api/keys/verify")

    def test_create_or_get_folder_proxy(self):
        client = NomadicML(api_key="valid_api_key")
        mock_video = MagicMock()
        mock_video.create_or_get_folder.return_value = {"id": "folder1"}
        client.__dict__["video"] = mock_video

        result = client.create_or_get_folder("Marketing")

        assert result == {"id": "folder1"}
        mock_video.create_or_get_folder.assert_called_once_with("Marketing")

    @patch("nomadicml.client.NomadicML._make_request")
    def test_cloud_integrations_list_filters(self, mock_make_request):
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"id": "g1", "name": "Fleet", "type": "gcs", "bucket": "fleet", "prefix": None},
            {"id": "s1", "name": "Archive", "type": "s3", "bucket": "archive", "prefix": None},
        ]
        mock_make_request.return_value = mock_response

        client = NomadicML(api_key="valid_api_key")
        results = client.cloud_integrations.list(type="gcs")

        assert results == [{"id": "g1", "name": "Fleet", "type": "gcs", "bucket": "fleet", "prefix": None}]
        mock_make_request.assert_called_once_with("GET", "/api/cloud-integrations")

    @patch("nomadicml.client.NomadicML._make_request")
    def test_cloud_integrations_add_gcs(self, mock_make_request):
        mock_response = MagicMock()
        payload = {
            "id": "int1",
            "name": "Fleet bucket",
            "type": "gcs",
            "bucket": "fleet",
            "prefix": None,
        }
        mock_response.json.return_value = payload
        mock_make_request.return_value = mock_response

        client = NomadicML(api_key="valid_api_key")
        service_account = {"type": "service_account", "project_id": "demo"}
        result = client.cloud_integrations.add(
            type="gcs",
            name="Fleet bucket",
            bucket="fleet",
            prefix=None,
            credentials=service_account,
        )

        assert result == payload
        mock_make_request.assert_called_once_with(
            "POST",
            "/api/cloud-integrations/gcs",
            json_data={
                "name": "Fleet bucket",
                "type": "gcs",
                "service_account": service_account,
                "bucket": "fleet",
                "prefix": None,
            },
        )

    @patch("nomadicml.client.NomadicML._make_request")
    def test_cloud_integrations_add_s3_accepts_camelcase(self, mock_make_request):
        mock_response = MagicMock()
        payload = {
            "id": "s3int",
            "name": "AWS footage",
            "type": "s3",
            "bucket": "archive",
            "prefix": "raw/",
            "region": "us-east-1",
        }
        mock_response.json.return_value = payload
        mock_make_request.return_value = mock_response

        client = NomadicML(api_key="valid_api_key")
        creds = {
            "accessKeyId": "AKIA...",
            "secretAccessKey": "secret",
            "sessionToken": "token",
        }

        result = client.cloud_integrations.add(
            type="s3",
            name="AWS footage",
            bucket="archive",
            prefix="raw/",
            region="us-east-1",
            credentials=creds,
        )

        assert result == payload
        mock_make_request.assert_called_once_with(
            "POST",
            "/api/cloud-integrations/s3",
            json_data={
                "name": "AWS footage",
                "type": "s3",
                "access_key_id": "AKIA...",
                "secret_access_key": "secret",
                "session_token": "token",
                "region": "us-east-1",
                "bucket": "archive",
                "prefix": "raw/",
            },
        )

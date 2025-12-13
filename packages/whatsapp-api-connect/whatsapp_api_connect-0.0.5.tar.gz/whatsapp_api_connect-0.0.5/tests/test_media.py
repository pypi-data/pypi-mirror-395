import os
import sys
import unittest
from unittest.mock import patch, mock_open, MagicMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from whatsapp_api.media.media_client import MediaClient


class TestMediaClient(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        # Mock environment variables
        self.access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
        self.phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        self.recipient_phone_number = os.getenv("TEST_RECIPIENT_PHONE_NUMBER")

        # Initialize MediaClient
        self.media_client = MediaClient(self.access_token, self.phone_number_id)

    @patch("os.path.isfile", return_value=True)
    @patch("mimetypes.guess_type", return_value=("image/jpeg", None))
    @patch("builtins.open", new_callable=mock_open, read_data=b"mock file content")
    @patch("requests.request")
    def test_upload_media_success(self, mock_request, mock_open, mock_guess_type, mock_isfile):
        """Test successful media upload."""
        # Mock successful API response
        mock_request.return_value = MagicMock(status_code=200, json=lambda: {"id": "mock_media_id"})

        # Call upload_media
        media_id = self.media_client.upload_media("/path/to/sample.jpg")

        # Assertions
        self.assertEqual(media_id, "mock_media_id")
        mock_request.assert_called_once_with(
            "POST",
            self.media_client.base_url + self.media_client.endpoint,
            data={"messaging_product": "whatsapp", "type": "image/jpeg"},
            files={
                "file": ("sample.jpg", mock_open.return_value, "image/jpeg", {"Expires": "0"})
            },
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

    @patch("os.path.isfile", return_value=False)
    def test_upload_media_file_not_found(self, mock_isfile):
        media_client = MediaClient(access_token="mock_access_token", phone_number_id="1234567890")
        with self.assertRaises(FileNotFoundError):
            media_client.upload_media("/path/to/nonexistent.jpg")

    @patch("os.path.isfile", return_value=True)
    @patch("mimetypes.guess_type", return_value=(None, None))
    def test_upload_media_mime_type_not_found(self, mock_guess_type, mock_isfile):
        with self.assertRaises(ValueError):
            self.media_client.upload_media("/path/to/unknown.file")

    @patch("os.path.isfile", return_value=True)
    @patch("mimetypes.guess_type", return_value=("audio/mpeg", None))
    @patch("builtins.open", new_callable=mock_open, read_data=b"mock audio content")
    @patch("requests.request")
    def test_upload_audio_success(self, mock_request, mock_open, mock_guess_type, mock_isfile):
        """Test successful upload of an audio file."""
        # Mock successful API response
        mock_request.return_value = MagicMock(status_code=200, json=lambda: {"id": "mock_audio_id"})

        # Call the upload_media method for an audio file
        media_id = self.media_client.upload_media("/path/to/sample.mp3")

        # Assertions
        self.assertEqual(media_id, "mock_audio_id")
        mock_request.assert_called_once_with(
            "POST",
            f"{self.media_client.base_url}{self.media_client.endpoint}",
            data={"messaging_product": "whatsapp", "type": "audio/mpeg"},
            files={
                "file": ("sample.mp3", mock_open.return_value, "audio/mpeg", {"Expires": "0"})
            },
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

    @patch("os.path.isfile", return_value=True)
    @patch("mimetypes.guess_type", return_value=("application/pdf", None))
    @patch("builtins.open", new_callable=mock_open, read_data=b"mock pdf content")
    @patch("requests.request")
    def test_upload_pdf_success(self, mock_request, mock_open, mock_guess_type, mock_isfile):
        """Test successful upload of a PDF file."""
        # Mock successful API response
        mock_request.return_value = MagicMock(status_code=200, json=lambda: {"id": "mock_pdf_id"})

        # Call the upload_media method for a PDF file
        media_id = self.media_client.upload_media("/path/to/sample.pdf")

        # Assertions
        self.assertEqual(media_id, "mock_pdf_id")
        mock_request.assert_called_once_with(
            "POST",
            f"{self.media_client.base_url}{self.media_client.endpoint}",
            data={"messaging_product": "whatsapp", "type": "application/pdf"},
            files={
                "file": ("sample.pdf", mock_open.return_value, "application/pdf", {"Expires": "0"})
            },
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

    @patch("requests.request")
    def test_get_media_url_success(self, mock_request):
        """Test successful media URL retrieval."""
        # Mock successful API response
        mock_request.return_value = MagicMock(
            status_code=200, 
            json=lambda: {
                "messaging_product": "whatsapp",
                "url": "<URL>",
                "mime_type": "image/jpeg",
                "sha256": "<HASH>",
                "file_size": "303833",
                "id": "2621233374848975"
            }
        )

        # Call media_retrieve
        media_id = "mock_media_id"
        response = self.media_client.get_media_url(media_id)

        # Assertions
        self.assertEqual(response, "<URL>")
        mock_request.assert_called_once_with(
            "GET",
            f"{self.media_client.base_url}{media_id}?phone_number_id={self.phone_number_id}",
            json=None,
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            },
        )

    # Download media from URL
    @patch("requests.request")
    def test_download_media_success(self, mock_request):
        """Test successful media download."""
        # Mock successful API response
        mock_request.return_value = MagicMock(
            status_code=200,
            content=b"mock file content",
            headers={"Content-Disposition": "attachment; filename=sample.jpg"},
        )

        media_url = "https://example.com/media/sample.jpg"
        response = self.media_client.download_media(media_url)

        self.assertEqual(response, b"mock file content")
        mock_request.assert_called_once_with(
            "GET",
            f"{self.media_client.base_url}{media_url}",
            json=None,
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            },
        )

    @patch("requests.request")
    def test_send_image_message_by_id_success(self, mock_request):
        """Test successful image message sending."""
        # Mock successful API response
        mock_request.return_value = MagicMock(
            status_code=200,
            json=lambda: {"messaging_product": "whatsapp", "messages": [{"id": "wamid.mock_message_id"}]},
        )

        # Call send_media_message_by_id
        media_id = "mock_media_id"
        context_message_id = "mock_context_message_id"
        response = self.media_client.send_media_message_by_id(
            recipient_phone_number=self.recipient_phone_number,
            media_id=media_id,
            media_type="image",
            context_message_id=context_message_id
        )

        # Assertions
        self.assertEqual(response["messages"][0]["id"], "wamid.mock_message_id")
        mock_request.assert_called_once_with(
            "POST",
            f"{self.media_client.base_url}{self.media_client.message_endpoint}",
            json={
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": self.recipient_phone_number,
                "type": "image",
                "image": {"id": media_id},
                "context": {"message_id": context_message_id}
            },
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            },
        )

    @patch("requests.request")
    def test_send_document_with_caption_and_filename(self, mock_request):
        """Test successful document message sending with caption and filename."""
        mock_request.return_value = MagicMock(
            status_code=200,
            json=lambda: {"messaging_product": "whatsapp", "messages": [{"id": "wamid.mock_message_id"}]},
        )

        media_id = "mock_document_id"
        response = self.media_client.send_media_message_by_id(
            recipient_phone_number=self.recipient_phone_number,
            media_id=media_id,
            media_type="document",
            caption="Here is your document.",
            filename="example.pdf"
        )

        # Assertions
        self.assertEqual(response["messages"][0]["id"], "wamid.mock_message_id")
        mock_request.assert_called_once_with(
            "POST",
            f"{self.media_client.base_url}{self.media_client.message_endpoint}",
            json={
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": self.recipient_phone_number,
                "type": "document",
                "document": {
                    "id": media_id,
                    "caption": "Here is your document.",
                    "filename": "example.pdf",
                },
            },
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            },
        )


    @patch("requests.request")
    def test_send_image_message_by_url_success(self, mock_request):
        """Test successful image message sending via URL."""
        # Mock successful API response
        mock_request.return_value = MagicMock(
            status_code=200,
            json=lambda: {"messaging_product": "whatsapp", "messages": [{"id": "wamid.mock_message_id"}]},
        )

        # Call send_media_message_by_url
        media_url = "https://example.com/media/image.jpg"
        context_message_id = "mock_context_message_id"
        response = self.media_client.send_media_message_by_url(
            recipient_phone_number=self.recipient_phone_number,
            media_url=media_url,
            media_type="image",
            context_message_id=context_message_id
        )

        # Assertions
        self.assertEqual(response["messages"][0]["id"], "wamid.mock_message_id")
        mock_request.assert_called_once_with(
            "POST",
            f"{self.media_client.base_url}{self.media_client.message_endpoint}",
            json={
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": self.recipient_phone_number,
                "type": "image",
                "image": {"link": media_url},
                "context": {"message_id": context_message_id}
            },
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            },
        )

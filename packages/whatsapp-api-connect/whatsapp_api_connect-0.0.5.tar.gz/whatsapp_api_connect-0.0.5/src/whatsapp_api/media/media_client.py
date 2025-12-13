import os
import requests
import mimetypes
from whatsapp_api.base_client import BaseClient


class MediaClient(BaseClient):
    def __init__(self, access_token, phone_number_id, version="v21.0"):
        """
        Media client for WhatsApp.

        :param access_token: Meta API access token
        :param phone_number_id: Phone number ID from WhatsApp
        """
        super().__init__(access_token, version)
        self.phone_number_id = phone_number_id
        self.endpoint = f"{phone_number_id}/media"
        self.message_endpoint = f"{phone_number_id}/messages"

    def _request_with_files(self, method, endpoint, payload, files):
        """
        Make an API request with file uploads.

        :param method: HTTP method (e.g., POST)
        :param endpoint: API endpoint (relative to base URL)
        :param payload: JSON payload
        :param files: Files to be uploaded
        :return: API response JSON
        :raises WhatsAppAPIException: If the API request fails
        """
        url = self.base_url + endpoint
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }

        # Send the request with the files and handle the response
        response = requests.request(method, url, data=payload, files=files, headers=headers)

        if response.status_code == 200:
            return response.json()

        raise Exception(f"Error: {response.status_code}, {response.text}")

    # Upload media file
    def upload_media(self, file_path):
        """
        Upload media to the Meta API.

        :param file_path: Path to the file to be uploaded.
        :return: Media ID from the API response.
        :raises FileNotFoundError: If the file does not exist.
        :raises ValueError: If the MIME type cannot be determined.
        """
        # Validate file existence
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File '{file_path}' does not exist.")

        # Determine the MIME type of the file
        mime_type = mimetypes.guess_type(file_path)[0]
        if not mime_type:
            raise ValueError(f"Could not determine the MIME type for file: {file_path}")

        # Prepare the files parameter for the request
        with open(file_path, 'rb') as file:
            files = {
                'file': (os.path.basename(file_path), file, mime_type, {'Expires': '0'}),
            }

            # Prepare the payload
            payload = {
                "messaging_product": "whatsapp",
                "type": mime_type,
            }

            response = self._request_with_files("POST", self.endpoint, payload, files)

        # Return the media ID from the response
        return response.get("id")

    # Retrieve Media URL
    def get_media_url(self, media_id):
        """
        Get the media URL from the Meta API.

        :param media_id: Media ID from the upload_media method.
        :return: Media objects from the API response.
        :raises Exception: If the API request fails.
        """
        endpoint = f"{media_id}?phone_number_id={self.phone_number_id}"
        response = self._request("GET", endpoint)
        return response

    # Download Media
    def download_media(self, media_url):
        """
        Download media from the given URL.

        :param media_url: URL of the media to download.
        :return: Binary data of the media.
        :raises Exception: If the download fails.
        """
        return self._request("GET", media_url, is_media=True)

    # Delete Media
    def delete_media(self, media_id):
        """
        Delete media

        :param media_id: Media ID to delete.
        :return: bool indicating whether the media was deleted successfully.
        :raises Exception: If the API request fails.
        """
        endpoint = f"{media_id}?phone_number_id={self.phone_number_id}"
        response = self._request("DELETE", endpoint)
        return response

    # Send media Message by ID
    def send_media_message_by_id(self, recipient_phone_number, media_id, media_type, context_message_id=None, **kwargs):
        """
        Send a media message using a media ID.

        :param recipient_phone_number: The recipient's WhatsApp phone number in international format (e.g., 1234567890, without the +).
        :param media_id: Media ID of the media to send.
        :param media_type: Type of the media to send (e.g., "image", "audio", "document", "sticker", "video").
        :param context_message_id: (Optional) Message ID of a previous message to reply to.
        :param kwargs: Additional fields for the media type (e.g., "caption" or "filename").
        :return: Response from the WhatsApp API.
        :raises ValueError: If an unsupported media type is provided or invalid parameters are used.
        :raises Exception: If the API request fails.
        """

        # Validate supported media types
        supported_media_types = {"image", "audio", "document", "sticker", "video"}
        if media_type not in supported_media_types:
            raise ValueError(f"Unsupported media type: {media_type}. Supported types are: {', '.join(supported_media_types)}")

        # media payload
        media_payload = {"id": media_id}

        # Handle caption and filename based on media type
        if "caption" in kwargs:
            if media_type in {"audio", "sticker"}:
                raise ValueError(f"Caption is not allowed for media type: {media_type}")
            media_payload["caption"] = kwargs["caption"]

        if media_type == "document" and "filename" in kwargs:
            media_payload["filename"] = kwargs["filename"]

        # payload
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_phone_number,
            "type": media_type,
            media_type: media_payload,
        }

        # Add context if provided
        if context_message_id:
            payload["context"] = {"message_id": context_message_id}

        # Send the request and return the response
        return self._request("POST", self.message_endpoint, payload)

    # Send media message by URL
    def send_media_message_by_url(self, recipient_phone_number, media_url, media_type, context_message_id=None, **kwargs):
        """
        Send a media message using a media URL.

        :param recipient_phone_number: The recipient's WhatsApp phone number in international format (e.g., 1234567890, without the +).
        :param media_url: Media URL of the media to send.
        :param media_type: Type of the media to send (e.g., "image", "audio", "document", "sticker", "video").
        :param context_message_id: (Optional) Message ID of a previous message to reply to.
        :param kwargs: Additional fields for the media type (e.g., "caption" or "filename").
        :return: Response from the WhatsApp API.
        :raises ValueError: If an unsupported media type is provided or invalid parameters are used.
        :raises Exception: If the API request fails.
        """

        # media payload
        media_payload = {"link": media_url}

        # Handle caption and filename based on media type
        if "caption" in kwargs:
            if media_type in {"audio", "sticker"}:
                raise ValueError(f"Caption is not allowed for media type: {media_type}")
            media_payload["caption"] = kwargs["caption"]

        # payload
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_phone_number,
            "type": media_type,
            media_type: media_payload,
        }

        # Add context if provided
        if context_message_id:
            payload["context"] = {"message_id": context_message_id}

        # Send the request and return the response
        return self._request("POST", self.message_endpoint, payload)

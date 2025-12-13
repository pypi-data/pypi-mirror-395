import requests


class BaseClient:
    def __init__(self, access_token, version="v21.0"):
        """
        Base client for WhatsApp API.

        :param access_token: Meta API access token
        :param version: API version (default is v21.0)
        """
        self.access_token = access_token
        self.base_url = f"https://graph.facebook.com/{version}/"

    def _request(self, method, endpoint, payload=None, is_media=False):
        """
        Make an API request.

        :param method: HTTP method (GET, POST, etc.)
        :param endpoint: API endpoint (relative to base URL)
        :param payload: JSON payload for POST/PUT requests
        :param is_media: Set to True if requesting media content (binary)
        :return: API response JSON
        """
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        url = self.base_url + endpoint

        response = requests.request(method, url, json=payload, headers=headers)

        # If response successful, return the JSON response
        if response.status_code == 200:
            if is_media:
                return response.content
            return response.json()

        # Handle rate limiting or other errors
        raise Exception(f"Error: {response.status_code}, {response.text}")

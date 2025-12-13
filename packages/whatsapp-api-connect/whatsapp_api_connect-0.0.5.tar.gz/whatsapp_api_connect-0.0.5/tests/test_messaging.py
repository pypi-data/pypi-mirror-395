import os
import sys
import unittest
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from whatsapp_api.message.messaging import MessagingClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class TestMessagingClient(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        # Load variables from .env
        self.access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
        self.phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        self.recipient_phone_number = os.getenv("TEST_RECIPIENT_PHONE_NUMBER")

        if not self.access_token or not self.phone_number_id or not self.recipient_phone_number:
            raise EnvironmentError("Missing environment variables in .env file.")

        # Initialize the MessagingClient
        self.client = MessagingClient(self.access_token, self.phone_number_id)

    # Send Text Message
    @patch("whatsapp_api.base_client.BaseClient._request")
    def test_send_text_message(self, mock_request):
        """Test sending a text message."""
        mock_request.return_value = {"success": True}

        response = self.client.send_text_message(self.recipient_phone_number, "Hello, World!")
        self.assertEqual(response, {"success": True})

        mock_request.assert_called_once_with(
            "POST",
            f"{self.phone_number_id}/messages",
            {
                "messaging_product": "whatsapp",
                "to": self.recipient_phone_number,
                "type": "text",
                "text": {
                    'preview_url': False,
                    "body": "Hello, World!"
                },
            },
        )

    # Send Location Message
    @patch("whatsapp_api.base_client.BaseClient._request")
    def test_send_location_message(self, mock_request):
        """Test sending a location message."""
        mock_request.return_value = {"success": True}

        latitude = 37.7749
        longitude = -122.4194
        name = "Golden Gate Park"
        address = "San Francisco, CA"
        context_message_id = "previous_message_id"

        response = self.client.send_location_message(
            recipient_phone_number=self.recipient_phone_number,
            latitude=latitude,
            longitude=longitude,
            name=name,
            address=address,
            context_message_id=context_message_id,
        )
        self.assertEqual(response, {"success": True})

        mock_request.assert_called_once_with(
            "POST",
            f"{self.phone_number_id}/messages",
            {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": self.recipient_phone_number,
                "type": "location",
                "location": {
                    "latitude": str(latitude),
                    "longitude": str(longitude),
                    "name": name,
                    "address": address,
                },
                "context": {"message_id": context_message_id},
            },
        )

    # Send Location Request Message
    @patch("whatsapp_api.base_client.BaseClient._request")
    def test_send_location_request_message(self, mock_request):
        """Test sending an interactive location request message."""
        mock_request.return_value = {"success": True}

        body_text = "Please share your location to find nearby stores."
        context_message_id = "previous_message_id"

        response = self.client.send_location_request_message(
            recipient_phone_number=self.recipient_phone_number,
            body_text=body_text,
            context_message_id=context_message_id,
        )
        self.assertEqual(response, {"success": True})

        mock_request.assert_called_once_with(
            "POST",
            f"{self.phone_number_id}/messages",
            {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": self.recipient_phone_number,
                "type": "interactive",
                "interactive": {
                    "type": "location_request_message",
                    "body": {"text": body_text},
                    "action": {"name": "send_location"},
                },
                "context": {"message_id": context_message_id},
            },
        )

    # Send Interactive Catalog Message
    @patch("whatsapp_api.base_client.BaseClient._request")
    def test_send_interactive_catalog_message(self, mock_request):
        """Test sending an interactive catalog message."""
        mock_request.return_value = {"success": True}

        body_text = "Explore our featured planter"
        product_retailer_id = 12345
        footer_text = "Limited time offer"
        context_message_id = "previous_message_id"

        response = self.client.send_interactive_catalog_message(
            recipient_phone_number=self.recipient_phone_number,
            body_text=body_text,
            product_retailer_id=product_retailer_id,
            footer_text=footer_text,
            context_message_id=context_message_id,
        )
        self.assertEqual(response, {"success": True})

        mock_request.assert_called_once_with(
            "POST",
            f"{self.phone_number_id}/messages",
            {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": self.recipient_phone_number,
                "type": "interactive",
                "interactive": {
                    "type": "catalog_message",
                    "body": {"text": body_text},
                    "action": {
                        "name": "catalog_message",
                        "product_retailer_id": str(product_retailer_id),
                    },
                    "footer": {"text": footer_text},
                },
                "context": {"message_id": context_message_id},
            },
        )

    # Send Reply with Reaction Message
    @patch("whatsapp_api.base_client.BaseClient._request")
    def test_send_reaction_message(self, mock_request):
        """Test sending a reaction message."""
        mock_request.return_value = {"success": True}

        message_id = "wam1234567890..."
        emoji = "👍"

        response = self.client.send_reaction_message(self.recipient_phone_number, message_id, emoji)
        self.assertEqual(response, {"success": True})

        mock_request.assert_called_once_with(
            "POST",
            self.client.endpoint,
            {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": self.recipient_phone_number,
                "type": "reaction",
                "reaction": {
                    "message_id": message_id,
                    "emoji": emoji,
                },
            },
        )

    # Send Interactive Message with Buttons
    @patch("whatsapp_api.base_client.BaseClient._request")
    def test_send_button_message(self, mock_request):
        """Test sending a button message."""
        mock_request.return_value = {"success": True}

        buttons = [
            {"type": "reply", "reply": {"id": "btn1", "title": "Button 1"}},
            {"type": "reply", "reply": {"id": "btn2", "title": "Button 2"}},
        ]

        response = self.client.send_button_message(self.recipient_phone_number, "Choose an option:", buttons)
        self.assertEqual(response, {"success": True})

        mock_request.assert_called_once_with(
            "POST",
            f"{self.phone_number_id}/messages",
            {
                "messaging_product": "whatsapp",
                "to": self.recipient_phone_number,
                "type": "interactive",
                "interactive": {
                    "type": "button",
                    "body": {"text": "Choose an option:"},
                    "action": {"buttons": buttons},
                },
            },
        )

    # Send Interactive Message with List
    @patch("requests.request")
    def test_send_list_message(self, mock_request):
        """Test sending a list message."""
        mock_request.return_value = MagicMock(
            status_code=200,
            json=lambda: {"messaging_product": "whatsapp", "messages": [{"id": "wamid.mock_message_id"}]},
        )

        sections = [
            {
                "title": "I want it ASAP!",
                "rows": [
                    {"id": "priority_express", "title": "Priority Mail Express", "description": "Next Day to 2 Days"},
                    {"id": "priority_mail", "title": "Priority Mail", "description": "1–3 Days"},
                ],
            },
        ]

        response = self.client.send_list_message(
            self.recipient_phone_number,
            body_text="Which shipping option do you prefer?",
            sections=sections,
            button_cta="Shipping Options",
            header_text="Choose Shipping Option",
            footer_text="Lucky Shrub: Your gateway to succulents™"
        )
        # self.assertEqual(response, {"success": True})
        self.assertEqual(response["messages"][0]["id"], "wamid.mock_message_id")

        mock_request.assert_called_once_with(
            "POST",
            f"{self.client.base_url}{self.client.endpoint}",
            json={
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": self.recipient_phone_number,
                "type": "interactive",
                "interactive": {
                    "type": "list",
                    "body": {"text": "Which shipping option do you prefer?"},
                    "header": {"type": "text", "text": "Choose Shipping Option"},
                    "footer": {"text": "Lucky Shrub: Your gateway to succulents™"},
                    "action": {
                        "button": "Shipping Options",
                        "sections": sections,
                    },
                },
            },
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            },
        )

    # Send Flow Message
    @patch("whatsapp_api.base_client.BaseClient._request")
    def test_send_flow_message(self, mock_request):
        """Test sending a flow message."""
        mock_request.return_value = {"success": True}

        body_text = "Flow message body"
        flow_cta = "Book!"
        flow_action = "navigate"
        flow_id = "1"
        header_text = "Flow message header"
        footer_text = "Flow message footer"
        flow_token = "AQAAAAACS5FpgQ_cAAAAAD0QI3s."
        flow_action_payload = {
            "screen": "FIRST_ENTRY_SCREEN",
            "data": {
                "product_name": "name",
                "product_description": "description",
                "product_price": 100,
            },
        }
        context_message_id = "previous_message_id"

        response = self.client.send_flow_message(
            recipient_phone_number=self.recipient_phone_number,
            body_text=body_text,
            flow_cta=flow_cta,
            flow_action=flow_action,
            flow_id=flow_id,
            header_text=header_text,
            footer_text=footer_text,
            flow_token=flow_token,
            flow_action_payload=flow_action_payload,
            context_message_id=context_message_id,
        )

        self.assertEqual(response, {"success": True})

        mock_request.assert_called_once_with(
            "POST",
            f"{self.phone_number_id}/messages",
            {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": self.recipient_phone_number,
                "type": "interactive",
                "interactive": {
                    "type": "flow",
                    "header": {"type": "text", "text": header_text},
                    "body": {"text": body_text},
                    "footer": {"text": footer_text},
                    "action": {
                        "name": "flow",
                        "parameters": {
                            "flow_message_version": "3",
                            "flow_cta": flow_cta,
                            "flow_action": flow_action,
                            "mode": "published",
                            "flow_id": flow_id,
                            "flow_token": flow_token,
                            "flow_action_payload": flow_action_payload,
                        },
                    },
                },
                "context": {"message_id": context_message_id},
            },
        )

if __name__ == "__main__":
    unittest.main()

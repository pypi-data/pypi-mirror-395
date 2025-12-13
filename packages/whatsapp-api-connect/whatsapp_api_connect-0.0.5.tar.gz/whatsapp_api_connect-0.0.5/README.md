# WhatsApp API

A Python wrapper for the Meta WhatsApp Business API. This package allows developers to interact with the WhatsApp Business API for sending messages, buttons, and list messages.


## Documentation

For detailed usage instructions, examples, and validation rules, check out the full documentation:

- [View Documentation](https://github.com/mahiuddin-dev/whatsapp-api-wrapper/blob/main/docs/index.md)


## Installation

### Clone the Repository

1. Clone the repository:
   ```bash
   git clone https://github.com/mahiuddin-dev/whatsapp-api-wrapper
   cd whatsapp-api-wrapper
   ```

### Create and Activate a Virtual Environment

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

### Install Dependencies

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### Create a `.env` File

1. Create a `.env` file in the root directory:
   ```bash
   touch .env
   ```

2. Add the following environment variables to the `.env` file:
   ```env
   WHATSAPP_ACCESS_TOKEN=your_access_token_here
   WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id_here
   TEST_RECIPIENT_PHONE_NUMBER=recipient_whatsapp_number_here
   ```

   Replace the placeholders with your actual values.

## Example: Sending a Text Message

   ```python
   from whatsapp_api.message.messaging import MessagingClient
   client = MessagingClient(access_token, phone_number_id)
   response = client.send_text_message(recipient_phone_number, "Hello from WhatsApp API!")
   print("Response:", response)
   ```

## Contributing

Contributions are welcome! If you have ideas or improvements, feel free to open a pull request or an issue.

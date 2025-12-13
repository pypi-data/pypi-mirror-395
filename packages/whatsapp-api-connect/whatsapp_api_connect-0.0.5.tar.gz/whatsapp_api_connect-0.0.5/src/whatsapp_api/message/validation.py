
def validate_buttons(buttons):
    """
    Validate the structure and constraints of the buttons.

    :param buttons: List of button dictionaries
    :return: None (raises an exception if invalid)
    """
    if not isinstance(buttons, list):
        raise ValueError("Buttons must be a list of dictionaries.")

    if len(buttons) > 3:
        raise ValueError("A maximum of 3 buttons are allowed.")

    # To track unique IDs
    seen_ids = set()

    for button in buttons:
        if not isinstance(button, dict):
            raise ValueError("Each button must be a dictionary.")

        if button.get("type") != "reply":
            raise ValueError(f"Invalid button type: {button.get('type')}. Only 'reply' type is supported.")

        reply = button.get("reply")
        if not reply or "id" not in reply or "title" not in reply:
            raise ValueError(f"Each button must have a 'reply' key with 'id' and 'title'. Got: {button}")

        # Check that the button ID is unique
        if reply["id"] in seen_ids:
            raise ValueError(f"Duplicate button ID found: {reply['id']}")
        seen_ids.add(reply["id"])

        # Check title constraints
        if not isinstance(reply["title"], str) or len(reply["title"]) > 20:
            raise ValueError(f"Button title must be a string and a maximum of 20 characters. Got: {reply['title']} - {len(reply['title'])} characters.")

def validate_list_message(body_text, sections, button_cta, header_text, footer_text):
    """
    Validate the structure and constraints of the interactive list message.

    :param body_text: The main body text of the message.
    :param sections: List of section dictionaries.
    :param button_cta: Button label text.
    :param header_text: Optional header text.
    :param footer_text: Optional footer text.
    :return: None (raises exceptions if validation fails).
    """
    # Validate body text
    if not isinstance(body_text, str) or len(body_text) > 4096:
        raise ValueError("Body text must be a string with a maximum of 4096 characters.")

    # Validate button CTA
    if not isinstance(button_cta, str) or len(button_cta) > 20:
        raise ValueError("Button CTA must be a string with a maximum of 20 characters.")

    # Validate header text
    if header_text and (not isinstance(header_text, str) or len(header_text) > 60):
        raise ValueError("Header text must be a string with a maximum of 60 characters.")

    # Validate footer text
    if footer_text and (not isinstance(footer_text, str) or len(footer_text) > 60):
        raise ValueError("Footer text must be a string with a maximum of 60 characters.")

    # Validate sections
    if not isinstance(sections, list) or len(sections) == 0:
        raise ValueError("Sections must be a non-empty list of dictionaries.")

    for section in sections:
        if "title" not in section or not isinstance(section["title"], str) or len(section["title"]) > 24:
            raise ValueError("Each section must have a title (max 24 characters).")

        rows = section.get("rows")
        if not isinstance(rows, list) or len(rows) == 0:
            raise ValueError("Each section must have a non-empty list of rows.")

        if len(rows) > 10:
            raise ValueError("Each section can contain a maximum of 10 rows.")

        seen_row_ids = set()
        for row in rows:
            if "id" not in row or not isinstance(row["id"], str) or len(row["id"]) > 200:
                raise ValueError("Each row must have an ID (max 200 characters).")

            if row["id"] in seen_row_ids:
                raise ValueError(f"Duplicate row ID found: {row['id']}")
            seen_row_ids.add(row["id"])

            if "title" not in row or not isinstance(row["title"], str) or len(row["title"]) > 24:
                raise ValueError("Each row must have a title (max 24 characters).")

            if "description" in row and (not isinstance(row["description"], str) or len(row["description"]) > 72):
                raise ValueError("Row description must be a string with a maximum of 72 characters.")

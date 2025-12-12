import json
from pathlib import Path


def load_schema(file_name: str) -> dict:
    """
    Loads a json schema from the packages data folder.
    :param file_name: name of the file
    :return: JSON object as a dictionary
    """

    with open(
        Path(__file__).parent / "data" / file_name, "r", encoding="utf-8"
    ) as schema_file:
        return json.loads(schema_file.read())


input_message_schema = load_schema("input_message_schema.json")
output_message_schema = load_schema("output_message_schema.json")

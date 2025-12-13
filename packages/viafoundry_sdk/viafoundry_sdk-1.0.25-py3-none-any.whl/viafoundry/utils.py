import json


def pretty_print(data: dict) -> None:
    """
    Prints a dictionary in a nicely formatted JSON structure.

    Args:
        data (dict): The dictionary to be printed.
    """
    print(json.dumps(data, indent=4))

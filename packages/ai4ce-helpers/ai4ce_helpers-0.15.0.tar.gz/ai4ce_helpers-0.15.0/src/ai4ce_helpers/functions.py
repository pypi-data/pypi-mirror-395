# Here is the place to but general helper functions
import ast
import json
import warnings
from pathlib import Path

import httpx
import pandas as pd
import toml

from .logging_setup import logger_ai4cehelper


def load_file(filename: Path) -> dict | pd.DataFrame:
    """
    Load data from a file. The function currently supports JSON files.

    Parameters:
    filename (Path): The path to the file.

    Returns:
    dict: The data loaded from the file if it's a JSON.
    """
    if filename.suffix == ".csv":
        df = pd.read_csv(filename, sep=",", header=0, index_col=None, na_values=["NA", "?"])
        return df

    elif filename.suffix == ".json":
        with open(filename) as file:
            return json.load(file)

    elif filename.suffix == ".toml":
        with open(filename) as file:
            return toml.load(file)

    else:
        logger_ai4cehelper.error("(lf) Unsupported file format: " + filename.suffix)
        raise ValueError("You need to add the file format to the load_file function.")


def move_parameter_placeholder(component: dict) -> dict:
    """

    Because not every parameter from the parameter_unit.toml is on the main level of each component, but rather in a placeholder dictionary called "i_parameter_placeholder",
    we will move them to the main level for uniformity

    Refer to the relevant functions in the Backend:
    https://gitlab.com/ai4ce/ai4ce-03-backend/-/blob/main/backend/v2/routers/validators.py?ref_type=heads#L501-515
    https://gitlab.com/ai4ce/ai4ce-03-backend/-/blob/main/backend/v2/schemas/components/_base_component_schema.py?ref_type=heads#L18-67

    And the parameter unit toml in the AI4CE main repo
    https://gitlab.com/ai4ce/public-info/-/raw/main/docs/parameter_unit_list.toml
    """

    for key, value in component.get("i_parameter_placeholder", {}).items():
        if key not in component or component[key] is None:
            component[key] = value
        elif isinstance(value, list):
            component[key].extend(value)
        else:
            logger_ai4cehelper.warning(f"(mpp) Found conflicting value for key '{key}': {component[key]} vs {value}")
    return component


def cleanup_parameters(component: dict) -> dict:
    """
    Aims to remove the 'i_' prefix from parameters in a component dictionary.

    Checks if a key starts with 'i_' and if the corresponding key without the prefix does not exist or is empty.
    Does not delete the original 'i_' key to preserve data integrity.
    """
    for key in list(component.keys()):
        if key.startswith("i_"):
            new_key = key[2:]  # Remove the 'i_' prefix
            if new_key not in component or component[new_key] in [None, "", [], {}]:
                component[new_key] = component[key]
            # del component[key]
    return component


def get_toml_from_url(url: str) -> dict:
    """
    Downloads and parses a TOML file from the specified URL.

    This function sends a GET request to the given URL, retrieves the TOML content,
    and parses it into a Python dictionary.

    Args:
        url (str): The URL pointing to the TOML file.

    Returns:
        dict: The parsed TOML content as a dictionary.

    Raises:
        httpx.HTTPStatusError: If the request to the given URL fails.
        toml.TomlDecodeError: If the file cannot be parsed as valid TOML.
    """
    with httpx.Client() as client:
        response = client.get(url)
        response.raise_for_status()
        return toml.loads(response.text)
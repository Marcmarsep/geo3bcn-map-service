import os
import api.shared.xlsx_parser as xlp

import os
import api.shared.xlsx_parser as xlp
import logging

# Initialize logging
log = logging.getLogger(__name__)

def get_map(current_folder, volcanoes_path, volcano, map_type):
    """
    Fetches map metadata from an Excel file based on the specified volcano and map type.

    Args:
        current_folder (str): The base directory where volcano data is stored.
        volcanoes_path (str): The subdirectory within current_folder that contains volcano data.
        volcano (str): The name of the volcano for which metadata is being requested.
        map_type (str): The type of map for which metadata is being requested.

    Returns:
        dict: Parsed data from the Excel file if available, else an error message.
    """
    path = os.path.join(current_folder, volcanoes_path, volcano, 'metadata', map_type + ".xlsx")
    try:
        # Attempt to parse the Excel file and return its content
        return xlp.parse_xlsx(path)
    except FileNotFoundError:
        # Log and return a meaningful error message if the file doesn't exist
        log.error(f"File not found: {path}")
        return {"error": "File not available"}
    except Exception as e:
        # Log any other exceptions and return a generic error message
        log.error(f"An error occurred while parsing {path}: {e}")
        return {"error": "Oops! File not available"}


def get_map_summary(current_path, volcanoes_path, map_type):
    """
    Lists all available maps of a specified type across all volcanoes.

    Args:
        current_path (str): The base directory where volcano data is stored.
        volcanoes_path (str): The subdirectory within current_path that contains volcano data.
        map_type (str): The type of map for which a summary list is being requested.

    Returns:
        list: A list of map names available for the specified map type.
    """
    # Construct the path to the directory containing the maps
    path = os.path.join(current_path, volcanoes_path)

    try:
        # Return the list of available map names
        return xlp.map_name_list(path, map_type)
    except Exception as e:
        # Log the error and return an empty list or error message
        log.error(f"An error occurred while listing maps for type '{map_type}' at path '{path}': {e}")
        return {"error": "Unable to fetch map summary"}

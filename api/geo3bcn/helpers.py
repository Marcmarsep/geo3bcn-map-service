import json
import os
from flask import send_file, abort, make_response
from shared.tools import dir_files_list  # Utility functions shared across the project
from shared.xlsx_parser import parse_xlsx, map_name_list  # Functions to parse Excel files and list map names
import logging

log = logging.getLogger(__name__)  # Setup logging for this module


def get_volcanoes_summary(volcano_path):
    """
    Loads and returns summaries from JSON files located in a specified directory.

    Args:
        volcano_path (str): Path to the directory containing JSON files for volcanoes.

    Returns:
        list: A list of dictionaries where each dictionary contains data from one JSON file.
    """
    summaries = []
    for file_path in dir_files_list(volcano_path):  # Loop through all files in the directory
        try:
            with open(file_path, 'r') as file:  # Open and read the JSON file
                data = json.load(file)
            summaries.append(data)  # Append the data to the summaries list
        except json.JSONDecodeError as e:
            log.error(f"Error reading {file_path}: {e}")  # Log JSON decoding errors
        except FileNotFoundError:
            log.error(f"File not found: {file_path}")  # Log if file is not found
        except Exception as e:
            log.error(f"An error occurred while reading {file_path}: {e}")  # Log any other exceptions
    return summaries


def get_metadata(current_path, volcanoes_path, volcano, _map):
    """
    Generates metadata for a given volcano and map by combining data from multiple Excel files.

    Args:
        current_path (str): Base path to the data directory.
        volcanoes_path (str): Relative path from the current path to the volcanoes directory.
        volcano (str): Name of the volcano.
        _map (str): Name of the map.

    Returns:
        dict: A dictionary containing combined metadata from the map and event tree.
    """
    try:
        # Construct full paths to the required metadata Excel files
        map_metadata_path = os.path.join(current_path, volcanoes_path, volcano, "event_tree", "metadata.xlsx")
        event_tree_metadata_path = os.path.join(current_path, volcanoes_path, volcano, 'metadata', _map + ".xlsx")

        # Fetch metadata from the Excel files
        map_metadata = get_map_metadata(map_metadata_path)
        event_tree_metadata = get_event_tree_metadata(event_tree_metadata_path)

        # Combine the metadata into a single dictionary
        metadata = {'map_metadata': map_metadata, 'event_tree_metadata': event_tree_metadata}
        return metadata
    except Exception as e:
        log.error(f"An error occurred while generating metadata for {volcano} and map {_map}: {e}")
        return {"error": "Failed to generate metadata."}  # Return an error message if exceptions occur


def get_map_metadata(path):
    """
    Fetches map metadata from an Excel file.

    Args:
        path (str): Path to the Excel file.

    Returns:
        Mixed: Parsed data from the Excel file or None if an error occurs.
    """
    try:
        return parse_xlsx(path)  # Attempt to parse the Excel file
    except FileNotFoundError:
        log.error(f"Metadata file not found: {path}")
        return None  # Return None to indicate file not found
    except Exception as e:
        log.error(f"Error parsing metadata file {path}: {e}")
        return None  # Return None for any other parsing errors


def get_maps_summary(current_path, volcanoes_path, file_name):
    """
    Fetches summaries for maps associated with a specific volcano.

    Args:
        current_path (str): Base path to the data directory.
        volcanoes_path (str): Relative path from the current path to the volcanoes directory.
        file_name (str): Name of the volcano (without file extension).

    Returns:
        dict: A dictionary containing the list of map names and the target volcano.
    """
    try:
        file_name, _ = os.path.splitext(file_name)  # Remove file extension
        path = os.path.join(current_path, volcanoes_path, file_name, "metadata")  # Construct path to metadata
        response = {"data": map_name_list(path), "volcano_target": file_name}  # Generate response
        return response
    except Exception as e:
        log.error(f"Error fetching map summaries for {file_name}: {e}")
        return {"error": f"Unable to fetch map summaries for {file_name}."}


def get_event_tree_metadata(path):
    """
    Fetches event tree metadata from an Excel file.

    Args:
        path (str): Path to the Excel file.

    Returns:
        Mixed: Parsed data from the Excel file or None if an error occurs.
    """
    try:
        return parse_xlsx(path)  # Attempt to parse the Excel file
    except FileNotFoundError:
        log.error(f"Event tree metadata file not found: {path}")
        return None  # Return None to indicate file not found
    except Exception as e:
        log.error(f"Error fetching event tree metadata from {path}: {e}")
        return None  # Return None for any other parsing errors


def get_file(file_name_no_ext, filetype, timestamp=None):
    """
    Serves a file based on its type for a given identifier.

    Args:
        file_name_no_ext (str): Identifier of the file without extension.
        filetype (str): Type of file to serve (e.g., 'event-tree-img', 'preview-img', 'kml').
        timestamp (str, optional): Timestamp for cache busting (unused in current implementation).

    Returns:
        Flask Response: A Flask response object to serve the file.
    """
    base_path = f'./volcanoes/{file_name_no_ext}'
    try:
        if filetype in ['event-tree-img', 'preview-img']:
            filename = 'eventtree.png' if filetype == 'event-tree-img' else 'preview.png'
            filepath = os.path.join(base_path, 'imgs', filename)
            return send_file(filepath, mimetype='image/png')
        elif filetype == 'kml':
            filepath = os.path.join(base_path, 'kml', 'preview.kml')
            with open(filepath, 'rb') as file:
                content = file.read()
                response = make_response(content)
                response.headers['Content-Type'] = 'application/vnd.google-earth.kml+xml'
                response.headers['Content-Disposition'] = f'attachment; filename="{file_name_no_ext}.kml"'
                return response
        else:
            abort(400, "Invalid file type requested.")
    except FileNotFoundError:
        abort(404, f"File {file_name_no_ext} not found.")
    except Exception as e:
        log.error(f"An error occurred while serving file for {file_name_no_ext}: {e}")
        abort(500, "Internal server error.")

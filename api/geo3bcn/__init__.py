import logging
import os
from flask import request, abort
from flask_restx import Resource

from flask import current_app as app

# Import serializers for data validation and response marshalling
from api.geo3bcn.serializers import map_summary, file_name, target, metadata, volcano
from api.restx import api

# Import helper functions for data retrieval and file serving
from geo3bcn.helpers import get_volcanoes_summary, get_event_tree_metadata, get_map_metadata, get_metadata, \
    get_maps_summary, get_file

# Configure logging for this module
log = logging.getLogger(__name__)

# Define a namespace for the geospatial data endpoints related to volcanoes
description = (
    'This namespace houses all the endpoints that support the volcanboxws '
    'volcanic map display application hosted at {...}'
)
ns = api.namespace('geo3bcn', description=description)

# Endpoint for retrieving summaries of volcanoes
@ns.route('/volcano-summary')
class VolcanoSummaryResource(Resource):
    @ns.marshal_list_with(volcano)
    def post(self):
        """
        Handles POST request to return a list of volcano summaries.
        """
        try:
            # Retrieve volcano summaries using the configured paths
            response = get_volcanoes_summary(
                os.path.join(app.config['paths']['current'], app.config['paths']['volcano']))
            return response, 200
        except Exception as e:
            # Log and return an error if the operation fails
            log.error(f"Error getting volcano summaries: {str(e)}")
            abort(500, "Internal server error.")

# Endpoint for retrieving map summaries based on a given volcano
@ns.route('/map-summary')
class MapSummaryResource(Resource):
    @api.expect(file_name, validate=True)
    @api.marshal_with(map_summary)
    def post(self):
        """
        Handles POST request to return a list of map names for a given volcano.
        """
        try:
            _file_name = request.json['file_name']
            if not _file_name:
                # Validate input
                abort(400, "The 'file_name' parameter is required.")

            # Retrieve map summaries
            response = get_maps_summary(app.config['paths']['current'], app.config['paths']['volcano'], _file_name)
            log.debug(f"Map summary response: {response}")
            return response, 201
        except Exception as e:
            # Log and return an error if the operation fails
            log.error(f"Error getting map summaries: {str(e)}")
            abort(500, "Internal server error.")

# Endpoint for serving event tree images
@ns.route('/event-tree-img/<string:file_name_no_ext>')
class EventTreeImage(Resource):
    def get(self, file_name_no_ext):
        """
        Serves the event tree image for a given volcano.
        """
        return get_file(file_name_no_ext, 'event-tree-img')

# Endpoint for serving preview images
@ns.route('/preview-img/<string:file_name_no_ext>')
class PreviewImage(Resource):
    def get(self, file_name_no_ext):
        """
        Serves the preview image for a given volcano.
        """
        return get_file(file_name_no_ext, 'preview-img')

# Endpoint for serving KML files
@ns.route('/kml/<string:file_name_no_ext>')
class Kml(Resource):
    def get(self, file_name_no_ext):
        """
        Serves the KML file for a given volcano.
        """
        return get_file(file_name_no_ext, 'kml')

# Endpoint for retrieving map metadata
@ns.route('/map-metadata')
class MapMetadataResource(Resource):
    @api.expect(target, validate=True)
    def post(self):
        """
        Handles POST request to return the metadata of a given map and event tree.
        """
        try:
            _volcano, _ = os.path.splitext(str(request.json['volcan']))
            map = request.json['map']
            if not _volcano or not map:
                # Validate input
                abort(400, "Both 'volcan' and 'map' parameters are required.")

            # Retrieve and return metadata
            response = get_metadata(app.config['paths']['current'], app.config['paths']['volcano'], _volcano, map)
            return response, 201
        except FileNotFoundError:
            # Handle file not found error
            abort(404, f"Metadata for {_volcano} or map {map} not found.")
        except Exception as e:
            # Log and return an error if the operation fails
            log.error(f"Error getting map metadata: {str(e)}")
            abort(500, "Internal server error.")

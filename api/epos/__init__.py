import logging
import os
from flask import request, jsonify, send_from_directory, abort
from flask_restx import Resource

# Importing custom Excel parser utilities for processing spreadsheet data
import api.shared.xlsx_parser as xlp

from flask import current_app as app
from api.restx import api

# Importing serializers for data validation and schema definition
from api.epos.serializers import type_summary, _type, map_parameters
from api.geo3bcn.serializers import map_summary, metadata

# Importing helper functions for retrieving map data
from api.epos.helpers import get_map_summary, get_map

# Setting up logging for this module
log = logging.getLogger(__name__)

# Defining a namespace for the EPOS endpoints within the API
namespace = 'epos'
description = 'This namespace houses all the endpoints that support Volcanbox Sections of the epos ' \
              'application to Access to scientific data from the communities. The application is hosted at: ' \
              'https://epos-ics-c-staging.brgm-rec.fr/data/search'

ns = api.namespace('epos', description=description)

# Endpoint for retrieving files stored in the configured directories
@ns.route('/getfile/<path:path>', methods=['GET'])
class getFile(Resource):
    def get(self, path):
        # Wrapper function to facilitate file retrieval
        return self.get_file(path)

    def get_file(self, path):
        # Attempts to serve a file from the directory specified in the application's configuration
        try:
            return send_from_directory(app.config['paths']['current'] + app.config['paths']['volcano'], path,
                                       as_attachment=True)
        except:
            # Returns an error message if file retrieval fails
            return "Oops! File not available"

@api.marshal_with(type_summary)
@ns.route('/type-summary')
class type_summary(Resource):
    def post(self):
        """
        POST: Returns a summary of types based on the current configuration paths.
        Attempts to retrieve and return a summary of types. If an error occurs,
        logs the error and returns an appropriate message to the client.
        """
        try:
            # Attempt to get the types summary from the configured paths
            d = xlp.get_types_summary(app.config['paths']['current'], app.config['paths']['volcano'])
            return jsonify(d)
        except Exception as e:
            # Log the exception and return a 500 Internal Server Error status to the client
            log.error(f"Failed to get types summary: {e}")
            abort(500, "Failed to retrieve types summary due to an internal server error.")

    def get(self):
        """
        GET: Returns a summary of types for GET requests.
        Similar to the POST method, it retrieves and returns a summary of types,
        handling any errors that occur during the process.
        """
        try:
            d = xlp.get_types_summary(app.config['paths']['current'], app.config['paths']['volcano'])
            return d
        except Exception as e:
            log.error(f"Failed to get types summary: {e}")
            abort(500, "Failed to retrieve types summary due to an internal server error.")


@api.marshal_with(map_summary)
@ns.route('/map-summary/<type>', methods=['GET'])
@ns.route('/map-summary', methods=['POST'])
class map_summary(Resource):
    @api.expect(_type, validate=True)
    def post(self):
        """
        POST: Returns a list of volcanoes and their available map types based on a specified type.
        Validates input and handles errors gracefully, providing meaningful feedback to the client.
        """
        try:
            # Retrieve the type from the request
            type = str(request.json['type'])
            if not type:
                ns.abort(400, "Type parameter is required.")

            # Attempt to retrieve map summary data
            response = get_map_summary(app.config['paths']['current'], app.config['paths']['volcano'], type)
            return response
        except KeyError:
            # Handle case where type is not found
            ns.abort(404, f"Type '{type}' not found.")
        except Exception as e:
            # Log unexpected errors and return a generic error response
            log.error(f"Error retrieving map summaries for type '{type}': {e}")
            ns.abort(500, "Internal server error while retrieving map summaries.")

    def get(self, type):
        """
        GET: Serves a list of available map types for a given volcano, specified by the 'type' URL parameter.
        Performs similar error handling as the POST method to ensure consistent behavior.
        """
        try:
            if not type:
                ns.abort(400, "Type parameter is required in the URL.")

            response = get_map_summary(app.config['paths']['current'], app.config['paths']['volcano'], type)
            return response
        except KeyError:
            ns.abort(404, f"Type '{type}' not found.")
        except Exception as e:
            log.error(f"Error retrieving map summaries for type '{type}': {e}")
            ns.abort(500, "Internal server error while retrieving map summaries.")


@api.marshal_with(metadata)
@ns.route('/map-metadata/<_type>/<volcano>', methods=['GET'])
@ns.route('/map-metadata', methods=['POST'])
class map_metadata(Resource):
    @api.expect(map_parameters, validate=True)
    def post(self):
        """
        POST: Returns metadata for a given map and volcano based on provided parameters.
        Includes error handling to manage missing parameters, data retrieval issues, and other exceptions.
        """
        try:
            volcano = str(request.json.get('volcano'))
            map_type = str(request.json.get('type'))

            if not volcano or not map_type:
                ns.abort(400, "Both 'volcano' and 'type' parameters are required.")

            response = get_map(app.config['paths']['current'], app.config['paths']['volcano'], volcano, map_type)
            if not response:
                ns.abort(404, f"Metadata for map '{map_type}' and volcano '{volcano}' not found.")
            return response
        except KeyError:
            ns.abort(404, "Specified map type or volcano does not exist.")
        except Exception as e:
            log.error(f"Error retrieving metadata for map '{map_type}' and volcano '{volcano}': {e}")
            ns.abort(500, "Internal server error while retrieving map metadata.")

    def get(self, _type, volcano):
        """
        GET: Similar to POST, it returns metadata for a specified map and volcano.
        Handles errors gracefully and ensures meaningful feedback is provided to the client.
        """
        try:
            if not _type or not volcano:
                ns.abort(400, "URL must include both map type and volcano name.")

            response = get_map(app.config['paths']['current'], app.config['paths']['volcano'], volcano, _type)
            if not response:
                ns.abort(404, f"Metadata for map '{_type}' and volcano '{volcano}' not found.")
            return response
        except KeyError:
            ns.abort(404, "Specified map type or volcano does not exist.")
        except Exception as e:
            log.error(f"Error retrieving metadata for map '{_type}' and volcano '{volcano}': {e}")
            ns.abort(500, "Internal server error while retrieving map metadata.")

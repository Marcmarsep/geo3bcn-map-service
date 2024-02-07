from flask_restx import fields
from api.restx import api

# Define the basic fields for the API models with descriptions.
# These fields represent common attributes for epos related models.
epos_fields = {
    # Defines a read-only 'type' field to describe the type of map.
    'type': fields.String(readOnly=True, description='Type of map'),

    # Defines a read-only 'volcano' field to store the volcano name without spaces.
    'volcano': fields.String(readOnly=True, description='No white spaces name of the Volcano'),
}

# Define the 'volcano' model based on epos_fields.
# This model represents a single volcano and includes only the 'volcano' field.
volcano = api.model(
    epos_fields['volcano'].description, {
        'volcano': epos_fields['volcano']
    })

# Define the '_type' model based on epos_fields.
# This model represents the type of map and includes only the 'type' field.
_type = api.model(
    epos_fields['type'].description, {
        'type': epos_fields['type']
    })

# Define the 'map_parameters' model for receiving parameters needed to get map metadata.
# It includes both 'type' and 'volcano' fields as defined in epos_fields.
map_parameters = api.model('Needed parameters to get map metadata',
                           {
                               'type': epos_fields['type'],
                               'volcano': epos_fields['volcano'],
                           })

# Define the 'type_summary' model.
# This model is used to return a summary of available types, structured as a list of '_type' models.
type_summary = api.model(
    'List of available volcanoes summary metadata',
    {
        'available_types': fields.List(fields.Nested(_type)),
    })

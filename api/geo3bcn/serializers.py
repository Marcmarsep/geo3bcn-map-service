from flask_restx import fields, Model

from api.restx import api

# Fields for the volcano data model
volcano_fields = {
    'name': fields.String(readOnly=True, description='Name of the volcano'),
    'nwsname': fields.String(readOnly=True, description='No white spaces name of the volcano'),
    'file': fields.String(readOnly=True, description='The file name of the given volcano'),
    'json_file': fields.String(readOnly=True,
                               description='Name and extension of JSON file containing the route to the target volcano, without whitespaces'),
    'desc': fields.String(readOnly=True, description='Description of the volcano'),
    'lng': fields.Float(readOnly=True, description='Longitude of the volcano'),
    'lat': fields.Float(readOnly=True, description='Latitude of the volcano')
}

# Fields for the map data model
map_fields = {
    'type': fields.String(readOnly=True, description='Type of the target map'),
    'name': fields.String(required=True, description='The name field')
}

# Model for volcano metadata
volcano = api.model('Volcano', {
    'name': volcano_fields['name'],
    'nwsname': volcano_fields['nwsname'],
    'desc': volcano_fields['desc'],
    'lng': volcano_fields['lng'],
    'lat': volcano_fields['lat'],
})

map_fields_model = api.model('MapField', {
    'type': fields.String(readOnly=True, description='Type of the target map'),
    'name': fields.String(required=True, description='The name field')
})
map_summary = api.model('MapSummary', {
    'volcano_target': volcano_fields['nwsname'],
    'data': fields.List(fields.Nested(map_fields_model), description='List of data items')
})

# Model for the filename field
file_name = api.model('FileName', {
    'file_name': volcano_fields['file']
})

# Model for the target field
target = api.model('Target', {
    'target_volcano_json_file': volcano_fields['json_file']
})

map_metadata_model = metadata = api.model(
    'Metadata of a given map',
    {
        'Name': fields.String(readOnly=True),
        'Functionality': fields.String(readOnly=True),
        'Category': fields.String(readOnly=True),
        'Item type': fields.String(readOnly=True),
        'Authors': fields.String(readOnly=True),
        'Product reference': fields.String(readOnly=True),
        'Tag-keywords': fields.String(readOnly=True),
        'Dependencies': fields.String(readOnly=True),
        'Hazard type:': fields.String(readOnly=True),
        'Hazard type- Data source': fields.String(readOnly=True),
        'Hazard type- Model name': fields.String(readOnly=True),
        'Hazard type-  Scenario definition': fields.String(readOnly=True),
        'Hazard type-Product type': fields.String(readOnly=True),
        'Hazard type- Parameter': fields.String(readOnly=True),
        'Hazard type-Percentile': fields.String(readOnly=True),
        'Hazard type- Threshold': fields.String(readOnly=True),
        'Hazard type- Units': fields.String(readOnly=True),
        'Geographical location-  Country': fields.String(readOnly=True),
        'Geographical location- Volcano name': fields.String(
            readOnly=True),
        'Volcano ID': fields.String(readOnly=True),
        'Volcano Lat': fields.String(readOnly=True),
        'Volcano Long': fields.String(readOnly=True),
        'Grid-  Ll grid point (product reference system)': fields.String(
            readOnly=True),
        'Grid- Ur grid point (product reference system)': fields.String(
            readOnly=True),
        'Grid- Ll grid point (ll)': fields.String(readOnly=True),
        'Grid- Ur grid point (ll)': fields.String(readOnly=True),
        'Grid- Grid unit (product reference system)': fields.String(
            readOnly=True),
        'Language': fields.String(readOnly=True),
        'Date of creation (for static products)': fields.String(
            readOnly=True),
        'Dates- Range of validity (for forecast products)': fields.String(
            readOnly=True),
        'Date of event': fields.String(readOnly=True),
        'Temporal extension- Initial date of temporal coverage of the volcanological dataset': fields.String(
            readOnly=True),
        'Temporal extension- Final date of temporal coverage of the volcanological dataset': fields.String(
            readOnly=True),
        'Temporal extension- Initial date of temporal coverage of the meteorological dataset': fields.String(
            readOnly=True),
        'Temporal extension- Final date of temporal coverage of the meteorological dataset': fields.String(
            readOnly=True),
        'Reference system': fields.String(readOnly=True),
        'Additional data': fields.String(readOnly=True),
        'Access to map': fields.String(readOnly=True)
    })

event_tree_metadata_model = api.model('EventTreeMetadata', {
    'Name': fields.String(description='Name of the event tree'),
    'Functionality': fields.String(description='Functionality of the event tree'),
    'Category': fields.String(description='Category of the event tree'),
    'Item type': fields.String(description='Type of the item'),
    'Authors': fields.String(description='Authors of the event tree'),
    'Product reference': fields.String(description='Product reference'),
    'Tag-keywords': fields.String(description='Tag keywords associated with the event tree'),
    'Dependencies': fields.String(description='Dependencies of the event tree'),
    'Hazard type:': fields.String(description='Type of hazard associated with the event tree'),
    'Hazard type- Data source': fields.String(description='Data source of the hazard type'),
    'Hazard type- Model name': fields.String(description='Model name of the hazard type'),
    'Hazard type- Scenario definition': fields.String(description='Scenario definition of the hazard type'),
    'Hazard type-Product type': fields.String(description='Product type of the hazard type'),
    'Hazard type- Parameter': fields.String(description='Parameter of the hazard type'),
    'Hazard type-Percentile': fields.String(description='Percentile of the hazard type'),
    'Hazard type- Threshold': fields.String(description='Threshold of the hazard type'),
    'Hazard type- Units': fields.String(description='Units of the hazard type'),
    'Geographical location- Country': fields.String(description='Country of the geographical location'),
    'Geographical location- Volcano name': fields.String(description='Volcano name of the geographical location'),
    '·\xa0\xa0\xa0\xa0\xa0\xa0 Volcano ID': fields.String(description='Volcano ID'),
    '·\xa0\xa0\xa0\xa0\xa0\xa0 Volcano Lat': fields.String(description='Latitude of the volcano'),
    '·\xa0\xa0\xa0\xa0\xa0\xa0 Volcano Long': fields.String(description='Longitude of the volcano'),
    'Grid- Ll grid point (product reference system)': fields.String(
        description='Lower-left grid point in the product reference system'),
    'Grid- Ur grid point (product reference system)': fields.String(
        description='Upper-right grid point in the product reference system'),
    'Grid- Ll grid point (ll)': fields.String(description='Lower-left grid point in latitude and longitude'),
    'Grid- Ur grid point (ll)': fields.String(description='Upper-right grid point in latitude and longitude'),
    'Grid- Grid unit (product reference system)': fields.String(
        description='Grid unit in the product reference system'),
    'Language': fields.String(description='Language of the event tree'),
    'Date of creation (for static products)': fields.String(
        description='Creation date of the event tree for static products'),
    'Dates- Range of validity (for forecast products)': fields.String(
        description='Range of validity dates for forecast products'),
    'Date of event': fields.String(description='Date of the related event'),
    'Temporal extension- Initial date of temporal coverage of the volcanological dataset': fields.String(
        description='Initial date of the temporal coverage of the volcanological dataset'),
    'Temporal extension- Final date of temporal coverage of the volcanological dataset': fields.String(
        description='Final date of the temporal coverage of the volcanological dataset'),
    'Temporal extension- Initial date of temporal coverage of the meteorological dataset': fields.String(
        description='Initial date of the temporal coverage of the meteorological dataset'),
    'Temporal extension- Final date of temporal coverage of the meteorological dataset': fields.String(
        description='Final date of the temporal coverage of the meteorological dataset'),
    'Reference system': fields.String(description='Reference system used for the event tree'),
    'Additional data': fields.String(description='Any additional data or notes'),
    'Access to map': fields.String(description='URL for accessing the event tree')
})

metadata = api.model('Data', {
    'map_metadata': fields.Nested(map_metadata_model, description='Metadata of the map'),
    'event_tree_metadata': fields.Nested(event_tree_metadata_model, description='Metadata of the event tree')
})

api.model('MapSummary', map_summary)

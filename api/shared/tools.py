import os
from osgeo import osr
osr.UseExceptions()
from osgeo_utils import gdal2tiles



def dir_files_list(directory):
    """
    List all files in a given directory.

    Args:
        directory (str): Directory path to list files from.

    Returns:
        list: A list of file paths.
    """
    files = []
    for item in os.listdir(directory):
        full_path = os.path.join(directory, item)
        if os.path.isfile(full_path):
            files.append(full_path)
    return files


def tif_to_kml(input_tif, output_dir, map_name, volcano_name):
    """
    Convert a TIFF file to KML using gdal2tiles.

    Args:
        input_tif (str): Input path of the TIFF file.
        output_dir (str): Output directory to store the resulting tiles.
        map_name (str): Name of the map to be used in titles.
        volcano_name (str): Name of the volcano to be used in the URL.
    """
    print(f"Input TIFF: {input_tif}")
    print(f"Output Directory: {output_dir}")

    # Define options for gdal2tiles
    options = {
        'verbose': False,
        'title': map_name,
        'profile': 'mercator',
        'url': f'https://volcanboxws.obsea.es/volcanoes/{volcano_name}/kml/',
        'resampling': 'average',
        # ... (other options)
        'googlekey': 'Your_Google_Key_Here',  # Replace with your actual key
        'bingkey': 'Your_Bing_Key_Here',  # Replace with your actual key
        'nb_processes': 1
    }

    # Generate tiles
    gdal2tiles.generate_tiles(input_tif, output_dir, **options)

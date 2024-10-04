
import os
import zipfile
import json
from shapely.geometry import Point, Polygon


# Get current working directory
working_directory = os.getcwd()

# Get project file name passed into script by user
filename = input('Project file: ')

# The project name, filename remove the extension (last 4 characters)
project_name = filename[:-4]

# Unzip the .esx project file into folder named "project_name"
with zipfile.ZipFile(filename, "r") as zip_ref:
    zip_ref.extractall(project_name)

# Load the tagKeys.json file into the tagKeyJSON dictionary
with open(project_name + '/areas.json') as json_file:
    areasJSON = json.load(json_file)

# Load the accessPoints.json file into the tagKeyJSON dictionary
with open(project_name + '/accessPoints.json') as json_file:
    accessPointsJSON = json.load(json_file)


def is_point_in_polygon(area_coords, ap_coords):
    # Create a Polygon object using the list of coordinates
    polygon = Polygon([(coord['x'], coord['y']) for coord in area_coords])

    # Create a Point object for the specific point we want to check
    point = Point(ap_coords['x'], ap_coords['y'])

    # Use the 'contains' method to check if the point is inside the polygon
    return polygon.contains(point)


for area in areasJSON['areas']:
    if "E911" in area['name']:
        for ap in accessPointsJSON['accessPoints']:
            if ap['mine']:
                if "model" in ap.keys():
                    # If we run this against a set of simulated APs
                    if "UXI" not in ap['model']:
                        ap_coords = {}
                        ap_coords['x'] = ap['location']['coord']['x']
                        ap_coords['y'] = ap['location']['coord']['y']
                        if is_point_in_polygon(area['area'], ap_coords):
                            print(f"AP {ap['name']} is in {area['name']}")
                else:
                    # If we run this against a set of measured APs
                    ap_coords = {}
                    ap_coords['x'] = ap['location']['coord']['x']
                    ap_coords['y'] = ap['location']['coord']['y']
                    if is_point_in_polygon(area['area'], ap_coords):
                        print(f"AP {ap['name']} is in {area['name']}")

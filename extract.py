"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    if not neo_csv_path:
        raise Exception('Path is empty, no filename provided!')

    neos = set()
    with open(neo_csv_path) as f:
        # create reader
        reader = csv.DictReader(f)
        for row in reader:
            neo_data = {
                'designation': row['pdes'],
                'name': row['name'],
                'diameter': row['diameter'],
                'hazardous': True if row['pha'] in ('Y', 'y') else False
            }
            neo = NearEarthObject(**neo_data)
            if neo not in neos:
                neos.add(neo)

    return neos


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    if not cad_json_path:
        raise Exception('Path is empty, no filename provided!')

    approaches = []
    with open(cad_json_path) as f:
        contents = json.load(f)
    for data in contents['data']:
        approach_data = {
            'designation': data[0],
            'time': data[3],
            'distance': data[4],
            'velocity': data[7]
        }
        approach = CloseApproach(**approach_data)
        approaches.append(approach)

    # return collections without duplicates
    return list(set(approaches))

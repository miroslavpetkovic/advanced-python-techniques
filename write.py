"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    field_names = ('datetime_utc', 'distance_au', 'velocity_km_s',
                  'designation', 'name', 'diameter_km',
                  'potentially_hazardous')

    with open(filename, 'w') as f:
        # Write header
        f.writelines(','.join(field_names) + '\n')
        # Write results
        for result in results:
            if result.distance:
                distance = str(result.distance)
            else:
                distance = ''
            if result.velocity:
                velocity = str(result.velocity)
            else:
                velocity = ''
            if result.neo.name:
                name = result.neo.name
            else:
                name = ''
            if result.neo.diameter:
                diameter = str(result.neo.diameter)
            else:
                diameter = ''
            if result.neo.hazardous:
                hazardous = 'True'
            else:
                hazardous = 'False'
            result_str = (result.time_str, distance, velocity, result._designation,
                          name, diameter, hazardous)
            f.writelines(','.join(result_str) + '\n')


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    results_json = []

    for result in results:
        neo_serialized = result.neo.serialize()
        result_serialized = result.serialize()
        result_serialized['neo'] = neo_serialized
        results_json.append(result_serialized)

    with open(filename, 'w') as f:
        json.dump(results_json, f)

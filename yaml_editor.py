#!/usr/bin/python3
import argparse
import collections
import os
import cProfile
from pstats import SortKey

try:
    from collections.abc import Callable
except ImportError:
    from collections import Callable
import yaml


def flatten(data, parent_key='', sep='|'):
    items = []
    for key, value in data.items():
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, collections.abc.MutableMapping):
            items.extend(flatten(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


def yaml_editor():
    try:
        parser = argparse.ArgumentParser(
            description='Enter two files.. \n1. Original file to edit.\n2. File with values to edit')
        parser.add_argument('--f1', dest='f1', help='Path to the input directory.')
        parser.add_argument('--f2', dest='f2', help='Path to the output that contains the resumes.')
        file_one, file_two = parser.parse_args().f1, parser.parse_args().f2

        with open(file_one) as file:
            values = yaml.full_load(file)

        with open(file_two) as file:
            changes = flatten(yaml.full_load(file))

        look_out_keys_values = {key.split('|')[-1]: changes[key]
                                for key in changes.keys() if key in flatten(values)}

        def set_value(obj, key):
            if key in obj:
                obj[key] = look_out_keys_values[key]
                return obj[key]
            for k, v in obj.items():
                if isinstance(v, dict):
                    item = set_value(v, key)
                    if item is not None:
                        return item

        for i in look_out_keys_values.keys():
            set_value(values, i)

        destination_dir = os.path.abspath(file_one).split('/')
        final_destination = "/".join(destination_dir[:-1]) + "/final.yaml"

        with open(final_destination, 'w') as file:
            yaml.dump(values, file)
            print(values)

    except FileNotFoundError as file_error:
        print(file_error)
        print('Make sure that the file passed in the args exists')
    except TypeError as type_error:
        print(type_error)
        print('Please ensure that the files have been passed as arguments')
    except ValueError as ve:
        print(ve)
        raise ValueError('Please ensure that the files are in a correct format')


if __name__ == '__main__':
    yaml_editor()
    # cProfile.run('yaml_editor()', sort=SortKey.CALLS)

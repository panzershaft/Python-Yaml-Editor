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


def un_flatten(dictionary):
    items = dict()
    for key, value in dictionary.items():
        parts = key.split("|")
        items_copy = items
        for part in parts[:-1]:
            if part not in items_copy:
                items_copy[part] = dict()
            items_copy = items_copy[part]
        items_copy[parts[-1]] = value
    return items


def yaml_editor():

    try:
        parser = argparse.ArgumentParser(
            description='Enter two files.. \n1. Original file with missing values.\n2. File with values')
        parser.add_argument('--f1', dest='f1', help='Path to the input directory.')
        parser.add_argument('--f2', dest='f2', help='Path to the output that contains the resumes.')
        file_one, file_two = parser.parse_args().f1, parser.parse_args().f2

        with open(file_one) as file:
            values = flatten(yaml.full_load(file))

        with open(file_two) as file:
            changes = flatten(yaml.full_load(file))

        value_padding = un_flatten(dict(list(values.items()) + list(changes.items())))

        destination_dir = os.path.abspath(file_one).split('/')
        final_destination = "/".join(destination_dir[:-1]) + "/final.yaml"

        with open(final_destination, 'w') as file:
            yaml.dump(value_padding, file)
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

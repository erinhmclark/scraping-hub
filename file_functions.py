""" A collection of useful operations to read or write files """
import pickle
import csv
import os
from PIL import Image


def compress_image(filepath, quality=85):
    """ Compress an image file. """
    img = Image.open(filepath)

    base_name, ext = os.path.splitext(filepath)
    new_filename = base_name + "_compressed" + ext

    img.save(new_filename, quality=quality)
    print(f"Compressed image is saved as {new_filename}")


def pickle_in_and_out(func):
    """ A decorator to pickle files of the input and output of functions.
        Useful for testing.
    """
    def pickle_bits(*args, **kwargs):
        """ Dumps a pickle of the first function input to a file of the function name suffixed with '_in'
            and a dump of the function output to a file of the function name suffixed with '_out'
        """
        with open(f'{func.__name__}_in', 'wb') as file:
            first_arg, *a = args
            pickle.dump(first_arg, file)
        value = func(*args, **kwargs)
        with open(f'{func.__name__}_out', 'wb') as file:
            pickle.dump(value, file)

        return value

    return pickle_bits


def insert_dict_to_csv(course_dict, csv_file_path):
    # add title if not already there
    with open(csv_file_path, 'a') as csv_file_object:
        writer = csv.DictWriter(csv_file_object, fieldnames=course_dict.keys())
        writer.writerow(course_dict)


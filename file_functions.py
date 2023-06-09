""" A collection of useful operations to read or write files """
import pickle


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

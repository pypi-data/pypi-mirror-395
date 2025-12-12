import numpy as np
import datetime


# some useful names
INT32 = np.int32
UINT32 = np.uint32
FLOAT32 = np.float32
# this is needed for cython
NONE = -999.0


def convert_date_for_NXS(date):
    """
    A method to change the date object into the
    format needed for the muon nexus v2 file
    :param data: the date object
    :return: a string of the date
    (<year>-<month>-<day>T<hour>:<min><sec>)
    """
    return date.strftime('%Y-%m-%dT%H:%M:%S')


def convert_date(date):

    """
    Convert the muon nexus v2 file data string into a
    date object.
    Assume in the form f'{year} {month} {day}', time
    :param date: the date string in the above format
    :return: the date object
    """

    return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')


def stype(string):
    """
    A simple method for reporting
    the length of a string for saving
    to a muon nexus v2 file
    :param string: the string to be saved
    :return: a string that reports the length of the
    string
    """
    return 'S{}'.format(len(string)+1)


def make_noise(vec, RNG):
    """
    A simple function for creating Gassian noise
    with the same shape as the input.
    :param vec: the data to add noise to
    :param RNG: the random number generator
    :return: the noise to be added
    """
    return RNG.normal(0, 0.1, vec.shape)


def create_data_from_function(x1, x2, dx, params, function, seed=None):
    """
    A method for creating mock data that is roughly given by
    the function and parameters.
    This method will add some random noise to both the x and
    y values.
    :param x1: the start x value
    :param x2: the end x value
    :param dx: the average step size for x
    :param params: a list of the parameters for the function
    :param function: a callable of the function to use
    (must return the y values)
    :param seed: the seed for the random number generator (optional)
    :return: The x and y values with noise.
    """
    x = np.arange(x1, x2, dx)
    RNG = np.random.default_rng(seed=seed)
    noise = make_noise(x, RNG)*dx
    x += noise
    y = function(x, *params)
    y_noise = make_noise(y, RNG)
    y = y*(1 + 0.1*y_noise/np.max(y_noise))
    return x, y

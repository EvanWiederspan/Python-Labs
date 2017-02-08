# Although a little unneccessary for a lab of this scale,
# the functions that the server can run were split out into 
# a separate file to allow for easy extendability.
# If you want to add another function to the server,
# just write the function here and then add its name to the export list
# at the bottom, and the server will be able to run it

from os import listdir, sys
from os.path import abspath
from time import ctime, sleep as _sleep

# Exception that functions can throw to cause the server to quit
# only used by EXITSERVER right now
class ExitServerException(BaseException):
    pass

def ls(dir = "."):
    '''Returns list of files and folders in specified directory'''
    if not isinstance(dir, str):
        raise TypeError('Must be a string')
    try:
        res = ", ".join(listdir(dir))
    except FileNotFoundError:
        res = "Directory doesn't exist"
    return "ls '{}': {}".format(abspath(dir), res)

def date(*args):
    '''Returns current datetime as a string
    arguments are ignored, but taken to prevent errors if called with parameters'''
    return ctime()

def os(*args):
    '''Returns name of os as a string
    arguments are ignored, but taken to prevent errors if called with parameters'''
    return sys.version

def sleep(secs = 5):
    '''Sleeps for a specified amount of time
    returns string when done'''
    try:
        dur = float(secs)
        # cant sleep for negative time
        if dur < 0:
            raise ValueError
        _sleep(dur)
        return "Slept for " + secs + " seconds"
    except ValueError:
        # caught if given negative or bad value
        _sleep(5)
        return "Invalid time '{}', slept for 5 seconds".format(secs)

def EXITSERVER(*args):
    '''Raises exception telling the server to exit'''
    raise ExitServerException

# List of functions that the server can run
# This is so the server knows which functions in this file are meant
# to be pieces of functionality
exports = ('ls', 'date', 'os', 'sleep', 'EXITSERVER')
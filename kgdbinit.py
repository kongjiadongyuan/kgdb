import sys
from os import path

# sys.setdefaultencoding('utf8')

directory, f = path.split(__file__)
directory = path.expanduser(directory)
directory = path.abspath(directory)
sys.path.append(directory)
sys.path.append(path.abspath('.'))
import kgdb

if path.exists('localinit.py') and path.isfile('localinit.py'):
    from localinit import *

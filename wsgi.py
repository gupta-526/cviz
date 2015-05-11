#!/usr/bin/python
import os
import imp
import sys

virtenv = os.path.join(os.environ.get('OPENSHIFT_PYTHON_IP','.'), 'virtenv')
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
    pass
#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#

from run import app as application
#
# Below for testing only
#
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    # Wait for a single request, serve it and quit.
    make_server(IP, PORT, application.app).serve_forever()
    #make_server('localhost', '5000', application.app).serve_forever()

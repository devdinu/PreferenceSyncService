import sys
import os


sys.path.insert(0, os.path.dirname(__file__) or '.')

PY_DIR = os.path.join(os.environ['OPENSHIFT_HOMEDIR'], "python")

virtenv = PY_DIR + '/virtenv/venv'

PY_CACHE = os.path.join(virtenv, 'lib', 'python'+os.environ['OPENSHIFT_PYTHON_VERSION'], 'site-packages')

os.environ['PYTHON_EGG_CACHE'] = os.path.join(PY_CACHE)
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')

try:
	    exec(open(virtualenv).read(), dict(__file__=virtualenv))
except IOError:
	    pass

from sync_preference_service import application as application

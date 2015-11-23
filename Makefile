#
# Simple Makefile for a Flask project
#

##
## Except for installation, all commands should be run with
## the virtual environment active
##

# Configuration
#
PYVENV = /usr/bin/env pyvenv-3.4 --without-pip env # ix.cs.uoregon.edu
# PYVENV = /usr/bin/env pyvenv env # Mac OS X

##
## Install in a new environment:
##     We need to rebuild the Python environment to match
##
install:
	# pyvenv-3.4 env ### BUGGY on ix
	echo "pyvenv without PIP to work around ubuntu bug"
	$(PYVENV)
	echo ""
	(.  env/bin/activate; curl https://bootstrap.pypa.io/get-pip.py | python)
	(.  env/bin/activate; pip install -r requirements.txt)

dist:
	pip freeze >requirements.txt

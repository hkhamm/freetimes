"""
Configuration of 'gcal' Flask app.
Edit to fit development or deployment environment.

"""
import random

# localhost
# PORT = 5000
# DEBUG = True

# ix.cs.uoregon.edu
PORT = 7420  # random.randint(5000, 8000)
DEBUG = False  # Because it's unsafe to run outside localhost

# both
GOOGLE_LICENSE_KEY = '.client_secret.json'

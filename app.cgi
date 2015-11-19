#! /usr/bin/env python3

""" For deployment on ix under CGI """

import site
site.addsitedir("/home/users/hhamm/public_html/cis322/htbin/proj6-gcal/env/lib/python3.4/site-packages")

from wsgiref.handlers import CGIHandler
from main import app

CGIHandler().run(app)

# proj7-freetimes
Calculates busy and free times using fetched appointment data from a selection of a user's Google calendars.

### Installation and Execution

1) Download the repository.

2) Obtain a *Client Id* and *Client Secret* for Google [here](https://auth0.com/docs/connections/social/google) and download as a JSON file to `/path/to/proj7-gcal`.

3) Copy CONFIG.base.py to CONFIG.py and edit for your environment. Include the client secret JSON file.

4) Setup the virtual enviroment:
```shell
cd /path/to/proj7-freetimes
make
```

5) Run the flask app:
```shell
cd /path/to/proj7-freetimes
source env/bin/activate
python3 main.py
```

### Resources

#### Website

- [jQuery](https://jquery.com/)
- [Boostrap](http://getbootstrap.com/)
- [Moment](http://momentjs.com/)
- [Jinja2](http://jinja.pocoo.org/)

#### Server

- [Flask](http://flask.pocoo.org/)
- [Pymongo](https://api.mongodb.org/python/current/)
- [Arrow](http://crsmithdev.com/arrow/)
- [Google oauth2client](https://github.com/google/oauth2client)
- [Google API Client Library for Python](https://developers.google.com/api-client-library/python/)

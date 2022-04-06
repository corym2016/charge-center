#  Charging Center Project - Cory Miller

## Heroku Application


## Usage


## Installation
```bash
# Clone Repo
$ git clone https://github.com/corym2016/charge-center.git
$ cd charge-center

# Make virtual env
$ mkvirtualenv myvirtualenv

# Set virtualenv to project dir
$ cd /charge-center
$ setprojectdir .

# Install flask to virtualenv
$ pip install flask
  # leave virtualenv
  $ deactivate

# Set env variables
$ cd /project1
$ set FLASK_APP = app.py
$ set DATABASE_URL = Heroku Postgres DB URI
$ set FLASK_DEBUG = 1

# Install dependencies
$ pip install -r requirements.txt

# Flask run
$ cd /project1
$ flask run
```

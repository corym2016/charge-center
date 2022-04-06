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
$ cd /project1
$ setprojectdir .

# Install flask to virtualenv
$ pip install flask
  # leave virtualenv
  $ deactivate

# Set env variables
$ cd /project1
$ SET FLASK_APP = app.py
$ SET DATABASE_URL = Heroku Postgres DB URI
$ SET FLASK_DEBUG = 1

# Install dependencies
$ pip install -r requirements.txt

# Flask run
$ cd /project1
$ flask run
```

#  CS50W Project 1 (Books) - Cory Miller

## Project Requirements
 https://docs.cs50.net/web/2020/x/projects/1/project1.html

## Heroku Application
https://project1-book-cory.herokuapp.com/

## Usage
Search for books without registering
  Search by title, author, year or isbn (also partial searches)
Register and search for Books
  Leave personal reviews for books that will show up on your profile
  These reviews will display for other users when they look up the respective book

## Installation
```bash
# Clone Repo
$ git clone https://github.com/corym2016/project1.git
$ cd project1

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
$ SET FLASK_APP = application.py
$ SET DATABASE_URL = Heroku Postgres DB URI
$ SET FLASK_DEBUG = 1

# Install dependencies
$ pip install -r requirements.txt

# Flask run
$ cd /project1
$ flask run
```

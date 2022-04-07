# use this to create tables into your databases
# the tables come from classes created in models.py
#the main function also imports all data from your csv file

import csv
import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://postgres:Millecor98!@localhost:5433/chargecenter_db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db.init_app(app)

def main():
    # creating the tables
    db.create_all()
    # #importing csv data
    # f = open("books.csv")
    # reader = csv.reader(f)
    # for isbn, title, author, year in reader:
    #     book = Book(b_isbn=isbn, b_title=title, b_author=author, b_year=year)
    #     db.session.add(book)
    #     print('Added book', title, 'written by', author, 'isbn', isbn, 'in the year', year)
    # db.session.commit()
    print('complete')

if __name__ == "__main__":
    with app.app_context():
        main()

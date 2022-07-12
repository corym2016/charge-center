# This is your classes and tables for your database

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    u_id = db.Column(db.Integer, primary_key=True)
    u_username= db.Column(db.String, nullable=False)
    u_password = db.Column(db.String, nullable=False)
    u_firstname = db.Column(db.String, nullable=False)
    u_lastname = db.Column(db.String, nullable=False)
    # making relationships /
    # #  all reviews for a given user
    # u_reviews = db.relationship("Review", backref="user", lazy=True)
    #
    # def add_review(self, rating, response, book_id):
    #     rv = Review(r_rating=rating, r_response=response, r_book_id=book_id, r_user_id=self.u_id)
    #     db.session.add(rv)
    #     db.session.commit()

class Charger(db.Model):
    __tablename__ = "chargers"
    ch_num = db.Column(db.Integer, primary_key=True)
    ch_ports = db.Column(db.Integer, nullable=False)

class Charger1(db.Model):
    __tablename__ = "charger1"
    # username = db.Column(db.String, primary_key=True)
    port_req = db.Column(db.Integer, primary_key=True)
    time_req = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Integer, nullable=False)
    end_time = db.Column(db.Integer, nullable=False)


# class Book(db.Model):
#     __tablename__ = "books"
#     b_id = db.Column(db.Integer, primary_key=True)
#     b_isbn = db.Column(db.String, nullable=False)
#     b_title = db.Column(db.String, nullable=False)
#     b_author = db.Column(db.String, nullable=False)
#     b_year = db.Column(db.String, nullable=False)
#     # making relationships / all reviews for a given book
#     b_reviews = db.relationship("Review", backref="book", lazy=True)
#
# class Review(db.Model):
#     __tablename__ = "reviews"
#     r_id = db.Column(db.Integer, primary_key=True)
#     r_rating = db.Column(db.Integer, nullable=False)
#     r_response = db.Column(db.String, nullable=True)
#     r_book_id = db.Column(db.Integer, db.ForeignKey("books.b_id"), nullable=False)
#     r_user_id = db.Column(db.Integer, db.ForeignKey("users.u_id"), nullable=False)

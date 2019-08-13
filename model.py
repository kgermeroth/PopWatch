"""Models and database functions for hotels db."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

######################################################

class Hotel(db.Model):
	"""Hotel model."""

	__tablename__ = 'hotels'

	hotel_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	hotel_name = db.Column(db.String(100), nullable=False)
	hotel_nickname = db.Column(db.String(10), nullable=False)
	ta_url = db.Column(db.Text, nullable=False)

	def __repr__(self):
		return f'<hotel_id={self.hotel_id} hotel_name={self.hotel_name}>'

class Scrape(db.Model):
	"""Scrape model - details info collected from each scrape"""

	__tablename__ = 'scrapes'

	scrape_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.hotel_id'), nullable=False)
	ta_id = db.Column(db.String(20), nullable=True)
	shop_timestamp = db.Column(db.DateTime, nullable=False)
	ranking = db.Column(db.Integer, nullable=True)
	num_hotels = db.Column(db.Integer, nullable=True)
	avg_score = db.Column(db.Float, nullable=True)
	review_count = db.Column(db.Integer, nullable=True)

	hotel = db.relationship('Hotel', backref='scrapes')

	def __repr__(self):
		return(f'<scrape_id={self.scrape_id} hotel_id={self.hotel_id}>')

	

class User(db.Model):
	"""User model."""

	__tablename__ = 'users'

	user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.Text, nullable=False)
	password = db.Column(db.String, nullable=False)
	default_view = db.Column(db.Integer, db.ForeignKey('view.view_id'), nullable=True)

	defaultview = db.relationship('View', foreign_keys='User.default_view')

	# 'views' is available for the back reference

	def __repr__(self):
		return(f'<user_id={self.user_id}> default_view={self.default_view}')


class View(db.Model):
	"""View model."""

	__tablename__ = 'view'

	view_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
	view_name = db.Column(db.String(50), nullable=False)

	user = db.relationship('User', foreign_keys='View.user_id', backref='views')
	viewhotels = db.relationship('ViewHotel')


	def __repr__(self):
		return(f'<view_id={self.view_id} user_id={self.user_id} view_name={self.view_name}>')

class ViewHotel(db.Model):
	"""View Hotel Model - the hotels associated with a view."""

	__tablename__ = 'view_hotel'

	view_id = db.Column(db.Integer, db.ForeignKey('view.view_id'), primary_key=True)
	hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.hotel_id'), primary_key=True)

	def __repr__(self):
		return(f'<view_id={self.view_id} hotel_id={self.hotel_id}>')

######################################################
# Helper functions

def init_app():
	# need to make a Flask app so we can use Flask-SQLAlchemy
	from flask import Flask
	app = Flask(__name__)

	connect_to_db(app)


def connect_to_db(app):
	"""Connect the database to our Flask app"""

	# Configure to use our database
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///hotels'
	app.config['SQLALCHEMY_ECHO'] = False
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.app = app
	db.init_app(app)

if __name__ == '__main__':

	init_app()
	db.create_all()
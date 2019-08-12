"""Models and database functions for hotels db."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy

######################################################

class Hotel(db.Model):
	"""Hotel model."""

	__tablename__ = 'hotels'

	hotel_id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
	hotel_name = db.Column(db.String(100), nullable=False,)
	hotel_nickname = db.Column(db.String(10), nullable=False,)
	ta_url = db.Column(db.Text(), nullable=False,)

	def __repr__(self):
		return f'<hotel_id={self.hotel_id} hotel_name={self.hotel_name}>'

class Scrape(db.Model):
	"""Scrape model - details info collected from each scrape"""

	__tablename__ = 'scrapes'

	scrape_id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
	hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.hotel_id'), nullable=False,)
	ta_id = db.Column(db.String(20), nullable=True,)
	shop_timestamp = db.Column(db.DateTime, nullable=False,)
	ranking = db.Column(db.Integer, nullable=True,)
	num_hotels = db.Column(db.Integer, nullable=True,)
	avg_score = db.Column(db.Float, nullable=True,)
	review_count = db.Column(db.Integer, nullable=True,)

	def __repr__(self):
		print(f'<scrape_id={self.scrape_id} hotel_id={self.hotel_id}>')

	hotel = db.relationship('Hotel', backref='scrapes')




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
	app.config['SQLALCHEMY_DATABASE-URI'] = 'postgres:///hotels'
	app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == '__main__':

	init_app()
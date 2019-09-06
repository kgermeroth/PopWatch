
from model import example_data, db

import unittest, datetime
from server import app
from flask_sqlalchemy import SQLAlchemy

class FlaskTests(unittest.TestCase):
	"""Tests for TripAdvisor Site"""

	def setUp(self):
		"""Stuff to do before every test."""
		self.client = app.test_client()
		app.config['TESTING'] = True


	def test_register_page(self):
		result = self.client.get('/register')
		self.assertIn(b'Submit the form', result.data)

	def test_login_page(self):
		result = self.client.get('/')
		self.assertIn(b'TripAdvisor Activity', result.data)

	def test_dashboard_page(self):

		with self.client as c:
			with c.session_transaction() as sess:
				sess['user_id'] = 1
				sess['set_choice'] = 1
				sess['metric_choice'] = 'Rank'
				sess['timeframe_choice'] = 'Daily'
				sess['hotels_selection'] = []

		result = self.client.get('/dashboard')
		self.assertIn(b'Performance Dashboard', result.data)

	def test_create_set_page(self):
		result = self.client.get('/create')
		self.assertIn(b'Create Your Comp Set', result.data)

	def test_manage_set_page(self):
		result = self.client.get('/manage')
		self.assertIn(b'Manage Your Comp Set', result.data)

	def test_add_hotel_page(self):
		result = self.client.get('/add-hotel')
		self.assertIn(b'Add a New Hotel', result.data)

class FlaskDatabaseTests(unittest.TestCase):
	""" Test database related items"""


	def init_app(self, app):
		"""Need to make a Flask app so we can use Flask-SQLALchemy"""

		self.connect_to_db(app)

		client = app.test_client
		self.client = app.test_client()

	def connect_to_db(self, app):
		"""Connect the database to our Flask app"""

		app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///testdb'
		app.config['TESTING'] = True
		app.config['SQLALCHEMY_ECHO'] = False
		app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
		db.app = app
		db.init_app(app)


	def setUp(self):
		"""Stuff to do before every test."""

		self.init_app(app)
		db.create_all()
		example_data()

	def test_table_creation(self):
		"""forces database to be created"""

		pass

def no_test_dbsetup():
	"""Set up test database when no tests exist"""
	def init_app():
		"""Need to make a Flask app so we can use Flask-SQLALchemy"""

		connect_to_db(app)

		client = app.test_client

	def connect_to_db(app):
		"""Connect the database to our Flask app"""

		app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///testdb'
		app.config['TESTING'] = True
		app.config['SQLALCHEMY_ECHO'] = False
		app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
		db.app = app
		db.init_app(app)

	init_app()
	db.create_all()
	example_data()


if __name__ == '__main__':
	
	unittest.main()



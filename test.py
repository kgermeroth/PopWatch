
from model import *

import unittest
from server import app


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
		self.assertIn(b'Monitor TripAdvisor', result.data)

class FlaskDatabaseTests(unittest.TestCase):
	""" Test database related items"""


	def init_app(self):
		"""Need to make a Flask app so we can use Flask-SQLALchemy"""

		connect_to_db(app)

		client = app.test_client
		self.client = app.test_client()

	def connect_to_db(app):
		"""Connect the database to our Flask app"""

		app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///testdb'
		app.config['TESTING'] = True
		app.config['SQLALCHEMY_ECHO'] = False
		app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
		db.app = app
		db.init_app(app)


	def setUp(self):
		"""Stuff to do before every test."""

		init_app()
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

		app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///testdb'
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



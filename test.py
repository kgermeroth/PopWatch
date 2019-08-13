
from model import *
from datetime import datetime

def init_app():
	# need to make a Flask app so we can use Flask-SQLAlchemy
	from flask import Flask
	app = Flask(__name__)

	connect_to_db(app)


def connect_to_db(app):
	"""Connect the database to our Flask app"""

	# Configure to use our database
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///testdb'
	app.config['TESTING'] = True
	app.config['SQLALCHEMY_ECHO'] = False
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.app = app
	db.init_app(app)

def setUp():
	"""Stuff to do before every test."""

	# Get the Flask test client
	from flask import Flask
	app = Flask(__name__)

	client = app.test_client
	app.config['TESTING'] = True
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///testdb'

	# Connect to test database
	connect_to_db(app)

	#create tables and add sample data


def example_data():
	"""Create some sample data"""

	ViewHotel.query.delete()
	View.query.delete()
	User.query.delete()
	Scrape.query.delete()
	Hotel.query.delete()

	# Add sample hotels
	h1 = Hotel(hotel_id=1, hotel_name='Sir Francis Drake', hotel_nickname='sfd', ta_url='https://www.tripadvisor.com/Hotel_Review-g60713-d81377-Reviews-Kimpton_Sir_Francis_Drake_Hotel-San_Francisco_California.html')
	h2 = Hotel(hotel_id=2, hotel_name='Grand Hyatt', hotel_nickname='ghyattus', ta_url='https://www.tripadvisor.com/Hotel_Review-g60713-d80999-Reviews-Grand_Hyatt_San_Francisco-San_Francisco_California.html')
	h3 = Hotel(hotel_id=3, hotel_name='Marriott Union Square', hotel_nickname='marrus', ta_url='https://www.tripadvisor.com/Hotel_Review-g60713-d124765-Reviews-San_Francisco_Marriott_Union_Square-San_Francisco_California.html')
	h4 = Hotel(hotel_id=4, hotel_name='Hotel Nikko', hotel_nickname='nikko', ta_url='https://www.tripadvisor.com/Hotel_Review-g60713-d80793-Reviews-Hotel_Nikko_San_Francisco-San_Francisco_California.html')
	h5 = Hotel(hotel_id=5, hotel_name='Spero', hotel_nickname='spero', ta_url='https://www.tripadvisor.com/Hotel_Review-g60713-d80802-Reviews-Hotel_Spero-San_Francisco_California.html')

	# Add sample scrapes
	now = datetime.now()
	s1 = Scrape(hotel_id=1, ta_id='N/A', shop_timestamp=now, ranking=136, num_hotels=242, avg_score=3.5, review_count=2000)
	s2 = Scrape(hotel_id=1, ta_id='N/A', shop_timestamp=now, ranking=135, num_hotels=242, avg_score=3.5, review_count=2005)
	s3 = Scrape(hotel_id=1, ta_id='N/A', shop_timestamp=now, ranking=135, num_hotels=242, avg_score=3.5, review_count=2010)
	s4 = Scrape(hotel_id=2, ta_id='N/A', shop_timestamp=now, ranking=40, num_hotels=242, avg_score=4.0, review_count=3500)
	s5 = Scrape(hotel_id=2, ta_id='N/A', shop_timestamp=now, ranking=42, num_hotels=242, avg_score=4.0, review_count=3505)
	s6 = Scrape(hotel_id=2, ta_id='N/A', shop_timestamp=now, ranking=42, num_hotels=242, avg_score=4.0, review_count=3510)
	s7 = Scrape(hotel_id=3, ta_id='N/A', shop_timestamp=now, ranking=15, num_hotels=242, avg_score=4.0, review_count=1500)
	s8 = Scrape(hotel_id=3, ta_id='N/A', shop_timestamp=now, ranking=15, num_hotels=242, avg_score=4.0, review_count=1510)
	s9 = Scrape(hotel_id=3, ta_id='N/A', shop_timestamp=now, ranking=15, num_hotels=242, avg_score=4.0, review_count=1515)	
	s10 = Scrape(hotel_id=4, ta_id='N/A', shop_timestamp=now, ranking=85, num_hotels=242, avg_score=4.0, review_count=2750)
	s11 = Scrape(hotel_id=4, ta_id='N/A', shop_timestamp=now, ranking=85, num_hotels=242, avg_score=4.0, review_count=2755)
	s12 = Scrape(hotel_id=4, ta_id='N/A', shop_timestamp=now, ranking=84, num_hotels=242, avg_score=4.0, review_count=2760)
	s13 = Scrape(hotel_id=5, ta_id='N/A', shop_timestamp=now, ranking=12, num_hotels=242, avg_score=4.5, review_count=200)
	s14 = Scrape(hotel_id=5, ta_id='N/A', shop_timestamp=now, ranking=12, num_hotels=242, avg_score=4.5, review_count=205)
	s15 = Scrape(hotel_id=5, ta_id='N/A', shop_timestamp=now, ranking=12, num_hotels=242, avg_score=4.5, review_count=208)

	# add sample users

	u1 = User(user_id=1, email='kg@gmail.com', password='password123')
	u2 = User(user_id=2, email='gb@gmail.com', password='password456')

	# add sample views
	v1 = View(view_id=1, user_id=1, view_name='kg default')
	v2 = View(view_id=2, user_id=1, view_name='kg secondary')
	v3 = View(view_id=3, user_id=2, view_name='gb secondary')
	v4 = View(view_id=4, user_id=2, view_name='gb default') 

	# add sample default views
	vh1 = ViewHotel(view_id=1, hotel_id=1)
	vh2 = ViewHotel(view_id=1, hotel_id=3)
	vh3 = ViewHotel(view_id=1, hotel_id=4)
	vh4 = ViewHotel(view_id=1, hotel_id=5)
	vh5 = ViewHotel(view_id=2, hotel_id=2)
	vh6 = ViewHotel(view_id=2, hotel_id=3)
	vh7 = ViewHotel(view_id=2, hotel_id=5)
	vh8 = ViewHotel(view_id=2, hotel_id=1)
	vh9 = ViewHotel(view_id=3, hotel_id=1)
	vh10 = ViewHotel(view_id=3, hotel_id=2)
	vh11 = ViewHotel(view_id=3, hotel_id=3)
	vh12 = ViewHotel(view_id=3, hotel_id=4)
	vh13 = ViewHotel(view_id=4, hotel_id=5)
	vh14 = ViewHotel(view_id=4, hotel_id=1)
	vh15 = ViewHotel(view_id=4, hotel_id=2)
	vh16 = ViewHotel(view_id=4, hotel_id=3)

	db.session.add_all([h1, h2, h3, h4, h5])
	db.session.commit()

	db.session.add_all([s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15])
	db.session.commit()

	db.session.add_all([u1, u2])
	db.session.commit()

	db.session.add_all([v1, v2, v3, v4])
	db.session.commit()

	db.session.add_all([vh1, vh2, vh3, vh4, vh5, vh6, vh7, vh8, vh9, vh10, vh11, vh12, vh13, vh14, vh15, vh16])
	db.session.commit()

	# u1.defaultview = 1
	# u2.defaultview = 4
	# db.session.commit()



if __name__ == '__main__':
	init_app()
	db.create_all()
	example_data()
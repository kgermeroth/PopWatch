"""Utility file to seed hotels database from collected data"""

from sqlalchemy import func
from model import connect_to_db, db, Hotel, Scrape, User, View, ViewHotel

def load_hotels():
	"""Load hotels from hotel_shopping_info.txt into database."""

	# delete all rows in table in case need to import multiple times
	Hotel.query.delete()

	for line in open('hotel_shopping_info.txt'):
		line = line.rstrip()
		hotel_id, hotel_name, hotel_nickname, ta_url = line.split('|')

		hotel = Hotel(hotel_id=hotel_id, 
					  hotel_name=hotel_name, 
					  hotel_nickname=hotel_nickname,
					  ta_url=ta_url)

		db.session.add(hotel)

	db.session.commit()



def set_val_hotel_id():
	"""Set value for the next hotel_id after seeding database"""

	# get Max hotel_id in database
	result = db.session.query(func.max(Hotel.hotel_id)).one()
	max_id = int(result[0])

	#set value for the next hotel_id to be max_id + 1
	query = 'SELECT setval('hotels_hotel_id', :new_id)'
	db.session.execute(query, {'new_id': max_id + 1})
	db.session.commit()

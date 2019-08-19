"""Utility file to seed hotels database from collected data"""

from sqlalchemy import func
from model import connect_to_db, db, init_app, Hotel, Scrape, User, View, ViewHotel

def load_hotels():
	"""Load hotels from hotel_shopping_info.txt into database."""

	# open file where data is stored
	file = open('hotel_shopping_info.txt')

	# go through each line in file, split on | and assign variables
	for line in file:
		line = line.rstrip()
		hotel_id, hotel_name, ta_url = line.split('|')

		# instantiate a hotel object
		hotel = Hotel(hotel_id=hotel_id, 
					  hotel_name=hotel_name, 
					  ta_url=ta_url)

		db.session.add(hotel)

	# commit all new hotels to database
	db.session.commit()

	file.close()

def load_scrapes():
	"""Load scrape data from hotel_data.csv into database."""

	# open file where data is stored
	file = open('hotel_data.csv')

	# go through each line in file, split on , and assign variables
	for line in file:
		line = line.rstrip()

		hotel_id, ta_id, shop_timestamp, ranking, num_hotels, avg_score, review_count = line.split(',')

		# need to account for NULLs. Postgres will not accept empty values or incorrect type
		# The '0' strings are to give a falsey value in case the variable is null, otherwise will get an error if variable is null
		ranking = int(ranking or '0') or None
		num_hotels = int(num_hotels or '0') or None
		avg_score = float(avg_score or '0') or None
		review_count = int(review_count or '0') or None

		# instantiate a scrape object
		scrape = Scrape(hotel_id=hotel_id,
						ta_id=ta_id,
						shop_timestamp=shop_timestamp,
						ranking=ranking,
						num_hotels=num_hotels,
						avg_score=avg_score,
						review_count=review_count)

		db.session.add(scrape)

	# commit all new scrapes to database
	db.session.commit()

	file.close()


def set_val_hotel_id():
	"""Set value for the next hotel_id after seeding database"""

	# get Max hotel_id in database
	result = db.session.query(func.max(Hotel.hotel_id)).one()
	max_id = int(result[0])

	#set value for the next hotel_id to be max_id + 1
	query = "SELECT setval('hotels_hotel_id_seq', :new_id)"
	db.session.execute(query, {'new_id': max_id + 1})
	db.session.commit()


def reset_val():
	"""Resets value for scrape_id to 1 after database is wiped"""

	query = "SELECT setval('scrapes_scrape_id_seq', :new_id)"
	db.session.execute(query, {'new_id': 1})
	db.session.commit()

if __name__ == "__main__":
	init_app()

	# delete all rows in table in case need to import multiple times
	
	Scrape.query.delete()
	Hotel.query.delete()
	reset_val()

	# import different types of data
	# must run load_scrapes first to avoid deleting what is a primary key in another table
	load_hotels()
	load_scrapes()
	set_val_hotel_id()
	
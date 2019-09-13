from server import *
from model import *
import os, re

def submit_new_hotel(inputs):
	"""Handles submission of new hotel to database"""
	hotel_name = inputs['hotel_name']
	ta_url = inputs['ta_url']

	# evaluate to see if URL appears valid
	match_obj = re.search(r'https:\/\/www.tripadvisor.com\/Hotel_Review-(\w+-\w+)-Reviews', ta_url)

	# if there is a match object, that means TA URL is valid
	if match_obj:
		
		# need to check to see if URL already exists
		if Hotel.query.filter(Hotel.ta_url == ta_url).all():
			message = Markup('<div class="alert alert-danger" role="alert">This hotel is already in the database.</div>')
			flash(message)
		
		# if the URL does not yet exist it is a new hotel
		else:
			# check to see if the provided hotel name has been used before
			if Hotel.query.filter(Hotel.hotel_name == hotel_name).all():
				message = Markup('<div class="alert alert-danger" role="alert">The provided Hotel Name already exists. Please choose a new name.</div>')
				flash(message)

			# if it hasn't been used before, submit it to database!
			else:
				hotel = Hotel(hotel_name=hotel_name, ta_url=ta_url)
				db.session.add(hotel)
				db.session.commit()

				message = Markup(f'<div class="alert alert-success" role="alert">{hotel_name} has been successfully added to database! You may now add hotel to a comp set.</div>')
				flash(message)

	# if there is no match object, then it is not a valid TA URL 		
	else:
		message = Markup('<div class="alert alert-danger" role="alert">The provided URL does not appear to be valid.</div>')
		flash(message)

def add_hotel_txtfile(ta_url):
	"""Adds new hotel to the back text file"""

	hotel = Hotel.query.filter(Hotel.ta_url == ta_url).one()

	row_to_add = f'{hotel.hotel_id}|{hotel.hotel_name}|{hotel.ta_url}\n'

	working_dir = str(os.path.dirname(os.path.realpath(__file__)))

	file_name = working_dir + '/hotel_shopping_info.txt'

	with open(file_name, "a") as myfile:
		myfile.write(row_to_add)


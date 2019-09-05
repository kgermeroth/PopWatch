from server import *
from model import *
import datetime

def submit_to_database(submission):
	"""Takes response object, parses it, and submits data to database."""

	default = False

	if submission.get('default') == 'true':
		default = True

	# this returns a list of all hotel choices where the choice is zero
	hotel_choices = submission.getlist('hotel_choice[]')

	view_name = submission['view_name']

	user_id = int(session['user_id'])

	# instantiate a View object and commit to database
	view = View(user_id=user_id, view_name=view_name)
	
	db.session.add(view)
	db.session.commit()

	# query to get the view number
	view_id = (View.query.filter(View.view_name == view_name, View.user_id == user_id).one()).view_id

	# check to see if a user already has a default. If not, set this as the default
	user = User.query.filter(User.user_id == user_id).one()

	if user.default_view == None:
		default = True
	
	if default == True:
		user.default_view = view_id

	db.session.add(user)
	db.session.commit()
			
	# add all the hotels to the view_hotel table in database
	for choice in hotel_choices:
		if choice != 'Select Hotel':
			view_hotel = ViewHotel(view_id=view_id, hotel_id=int(choice))

			db.session.add(view_hotel)
			db.session.commit()

	# obtain default_view number
	default = User.query.filter(User.user_id == user_id).one().default_view
	return default


def set_initial_session_options():
	"""Sets initial session options so chart on dashboard will have values to work with"""

	user_id = session['user_id']

	# get user object from the session
	user = User.query.get(user_id)

	session['set_choice'] = user.default_view

	hotel_views = ViewHotel.query.filter(ViewHotel.view_id == session['set_choice']).all()

	session['hotels_selection'] = [hotel_view.hotel_id for hotel_view in hotel_views]

	session['metric_choice'] = 'Rank'
	session['timeframe_choice'] = 'Weekly'


def get_hotel_information():
	"""Returns a list of all hotel objects in dictionary form"""

	# get a list of all hotel objects
	db_hotels = Hotel.query.all()

	hotels = []

	# loop through each hotel object and add hotel id and hotel name to the list in key:value pairs
	for hotel_obj in db_hotels:
		hotels.append(hotel_obj.hotel_to_dict())

	return hotels


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
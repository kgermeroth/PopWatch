from server import *
from model import Hotel, Scrape, User, View, ViewHotel, db
from flask_sqlalchemy import SQLAlchemy

def get_all_view_info():
	"""Gets all view data needed for manage set page"""

	# list of dicts with view_ids and view_name
	view_names = []

	# dictionary of hotels in views
	hotels_in_views = {}

	user_id = session['user_id']

	# query for all views under the user's id
	views = View.query.filter(View.user_id == user_id).all()

	default_view = views[0].user.default_view

	for view in views:
		# create a list of view_ids and view_names
		view_names.append(view.view_to_dict())

		# create a dictionary of all hotel_ids in the comp set
		hotel_ids = []

		for hotel in view.hotels:
			hotel_ids.append(hotel.hotel_id)

		hotels_in_views[view.view_id] = hotel_ids
		
	return 	(default_view, view_names, hotels_in_views)

def handle_set_changes(inputs):
	"""Takes data from manage set form and updates database as needed"""

	# get view_id of comp set we are modifying
	view_id = int(inputs['set_id'])

	# get user_id from session
	user_id = session['user_id']

	user = User.query.filter(User.user_id == user_id).one()

	# check to see if the set is to be deleted
	if inputs['delete_all'] == 'true':

		# check to see if this set is the default
		if user.default_view == view_id:
			user.default_view = None
			db.session.add(user)
			db.session.commit()
		
		# delete all view_hotels with that view_id
		view_hotels_to_delete = ViewHotel.query.filter(ViewHotel.view_id == view_id).all()
		for view_hotel in view_hotels_to_delete:
			db.session.delete(view_hotel)
			db.session.commit()
		
		# delete that view_id
		view_to_delete = View.query.filter(View.view_id == view_id).one()
		db.session.delete(view_to_delete)
		db.session.commit()

		message = Markup('<div class="alert alert-success" role="alert">Your comp set has been successfully deleted.</div>')

	else:
		view = View.query.filter(View.view_id == view_id).one()
		submitted_name = inputs['set_name']

		# compare view_name to submitted name and if they don't match update the comp set name in the database
		if not view.view_name == submitted_name:
			view.view_name = submitted_name
			db.session.add(view)
			db.session.commit()

		# if default is checked:
		if inputs['default_choice'] == 'true':
			user.default_view = view_id
			db.session.add(user)
			db.session.commit()

		# compare sets to see what needs to be updated using set math
		# variable for original set
		# variable for submitted set
		# hotels to be deleted = original set - submitted set
		# hotels to be added = new set - original set
		# if the list to delete (make sure that is what is returned) is not empty:
			# loop through list and delete hotels from view_hotels table
		# if the list to add is not empty:
			# loop through list and add hotels to view_hotels table
		# flash the comp set has been updated
	# do a user query
		# if user default is null:
			# get all views for user
			# if there are no views, redirect to create set page and flash message comp set must be created
			# else:
				# take first available set and set default to that
				# flash message saying which set name was set to the default


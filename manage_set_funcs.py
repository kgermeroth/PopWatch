from server import *
from model import *

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
	# get user_id from session
	# run a user query (to be used later)

	# check to see if the set is to be deleted
	# if yes, check to see if this set is the default
		# if it is, change the default to be null
		# else
			# delete all view_hotels with that view_id
			# delete that view_id
			# flash that comp set has been deleted
	# if set not to be deleted:
		# query the view by view_id
		# compare view_name to submitted name
		# if not view.view_name == submitted name:
			# set view name to submitted name and submit to db
		# if default is checked:
			# update default for user to this comp set
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


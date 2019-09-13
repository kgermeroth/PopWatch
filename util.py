from server import *
from model import *
import datetime

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



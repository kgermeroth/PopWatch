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


def set_initial_inputs():
	"""Sets up initial inputs"""

	user_id = session['user_id']

	# get user object from the session
	user = User.query.get(user_id)

	# set the session to have 'set_choice' with the default view. Update later via AJAX if choice changes
	set_choice = session['set_choice']

	# get a list of view objects for that user
	views = user.views

	# get the view object for the default view
	default_view = View.query.filter(View.view_id == user.default_view).one()

	# get a list of non-default views
	non_default_views = [view for view in views if view.view_id != user.default_view]

	metrics = ['Rank', 'Average Score', 'Number of Reviews']

	timeframes = ['Weekly', 'Daily']

	hotels_in_view = ViewHotel.query.filter(ViewHotel.view_id == set_choice).all()

	return (user, views, default_view, non_default_views, metrics, timeframes, hotels_in_view)

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

def get_border_color(index):
	"""Gets an rbga color from a list"""

	color_list = ['rgba(111,183,214,1)', 'rgba(165,137,193,1)', 'rgba(252,169,133,1)', 'rgba(142,210,144,1)',
				  'rgba(255,250,129,1)', 'rgba(249,140,182,1)', 'rgba(117,137,191,1)', 'rgba(72,181,163,1)']

	return color_list[index]


def get_background_color(index):
	"""Gets an rbga color from a list"""

	color_list = ['rgba(111,183,214,0.2)', 'rgba(165,137,193,0.2)', 'rgba(252,169,133,0.2)', 'rgba(142,210,144,0.2)',
				  'rgba(255,250,129,0.2)', 'rgba(249,140,182,0.2)', 'rgba(117,137,191,0.2)', 'rgba(72,181,163,0.2)']

	return color_list[index]


def get_hotel_information():
	"""Returns a list of all hotel objects in dictionary form"""

	# get a list of all hotel objects
	db_hotels = Hotel.query.all()

	hotels = []

	# loop through each hotel object and add hotel id and hotel name to the list in key:value pairs
	for hotel_obj in db_hotels:
		hotels.append(hotel_obj.hotel_to_dict())

	return hotels


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


def get_chart_data():
	"""Query database and get data into proper format"""

	chosen_hotels = session['hotels_selection']
	timeframe_choice = session['timeframe_choice']
	metric_choice = session['metric_choice']

	labels = []		# list of dates from scrapes
	datasets = []

	def get_data_from_scrape(i, scrape):
		"""Takes scrape and parses out data"""

		# for first set of hotels only, get the dates and add them to the labels list
		if i == 0:
			timestamp = scrape.shop_timestamp
			clean_stamp = timestamp.strftime('%a, %b %-d, %Y')
			labels.append(clean_stamp)

		# append the data to the data list
		if metric_choice == 'Rank':
			data.append(scrape.ranking)
		elif metric_choice == 'Average Score':
			data.append(scrape.avg_score)
		elif metric_choice == 'Number of Reviews':
			data.append(scrape.review_count)


	current_time = datetime.datetime.now()
	thirty_days_ago = current_time - datetime.timedelta(days=30)
	six_months_ago = current_time - datetime.timedelta(days=180)

	# run queries for each of the hotels and parse out the data
	for i, hotel in enumerate(chosen_hotels):
		
		data = []					# this will hold the actual data values for each hotel

		# @TODO change queries so they take timeframe into account

		# do a query
		scrapes = Scrape.query.filter(Scrape.hotel_id == hotel).all()

		# loop through scrape information to parse out data
		for j, scrape in enumerate(scrapes):

			# for first shop set a label equal to the hotel's name
			if j == 0:
				label = scrape.hotel.hotel_name

			# address weekly setting
			if timeframe_choice == 'Weekly':

				# if the shop is on a Sunday, get data
				if (scrape.shop_timestamp.weekday() == 6) and (scrape.shop_timestamp > six_months_ago):
					get_data_from_scrape(i, scrape)

			# address daily setting
			elif timeframe_choice == 'Daily':

				# if the shop is after thirty days ago:
				if scrape.shop_timestamp > thirty_days_ago:
					get_data_from_scrape(i, scrape)

		# get chart data compiled
		chart_line_info = {
			'label' : label,
			'fill' : False,
			'lineTension' : 0.5,
			'backgroundColor' : get_background_color(i),
			'borderColor' : get_border_color(i),
			'borderCapStyle' : 'butt',
			'borderDash' : [],
			'boderDashOffset' : 0.0,
			'borderJoinStyle' : 'miter',
			'pointBorderColor' : get_border_color(i),
			'pointBackgroundColor' : '#fff',
			'pointHoverBorderColor' : get_border_color(i),
			'pointHoverBorderWidth' : 2,
			'pointRadius' : 3,
			'pointHitRadius' : 10,
			'data' : data,
			'spanGaps' : False
			}

		datasets.append(chart_line_info)

	return {"labels" : labels, "datasets" : datasets}


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
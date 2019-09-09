from server import *
from model import *
import datetime

def set_initial_inputs():
	"""Sets up initial inputs for chart options"""

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


def get_border_color(index):
	"""Gets an rbga color from a list"""

	color_list = ['rgba(50,140,193,1)', 'rgba(235,110,128,1)', 'rgba(0,143,149,1)', 'rgba(109,121,147,1)',
				  'rgba(254,166,128,1)', 'rgba(110,196,216,1)', 'rgba(205,83,96,1)', 'rgba(73,39,74,1)']

	return color_list[index]


def get_background_color(index):
	"""Gets an rbga color from a list"""

	color_list = ['rgba(50,140,193,0.2)', 'rgba(235,110,128,0.2)', 'rgba(0,143,149,0.2)', 'rgba(109,121,147,0.2)',
				  'rgba(254,166,128,0.2)', 'rgba(110,196,216,0.2)', 'rgba(205,83,96,0.2)', 'rgba(73,39,74,0.2)']

	return color_list[index]


def get_chart_data():
	"""Query database and get data into proper format"""

	chosen_hotels = session['hotels_selection']
	timeframe_choice = session['timeframe_choice']
	metric_choice = session['metric_choice']

	all_dates = set()		
	datasets = []

	def get_data_from_scrape(scrape):
		"""Takes scrape and parses out data"""

		# get the dates and add them to the all_dates set
		timestamp = scrape.shop_timestamp
		date_only = timestamp.date()
		all_dates.add(date_only)

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
					get_data_from_scrape(scrape)

			# address daily setting
			elif timeframe_choice == 'Daily':

				# if the shop is after thirty days ago:
				if scrape.shop_timestamp > thirty_days_ago:
					get_data_from_scrape(scrape)


	
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

	# convert the date set into a sorted list with the desired format
	labels = list(all_dates)

	labels.sort()

	clean_dates = []

	for label in labels:
		clean_dates.append(label.strftime('%a, %b %-d, %Y'))

	# go through all data sets and pad the data as needed
	num_dates = len(clean_dates)

	for dataset in datasets:
		data_length = len(dataset['data'])
		if data_length != num_dates:
			dataset['data'] = ([None] * (num_dates - data_length)) + dataset['data']

	return { "labels" : clean_dates, "datasets" : datasets}


def get_csv_data():
	"""Pulls appropriate data and sends to html page in correct format"""

	chosen_hotels = session['hotels_selection']
	timeframe_choice = session['timeframe_choice']

	rows = [['Hotel ID', 'Hotel Name', 'Shop Date', 'TA Rank', 'TA Avg Score', 'Total Reviews', 'Num Hotels in Market']]		# list of each row

	current_time = datetime.datetime.now()
	thirty_days_ago = current_time - datetime.timedelta(days=30)
	six_months_ago = current_time - datetime.timedelta(days=180)

	def add_data_to_row():
		"""Takes info from scrape and adds it to the row"""

		clean_date = scrape.shop_timestamp.strftime('%d %b %Y')

		row.append(scrape.hotel_id)
		row.append(scrape.hotel.hotel_name)
		row.append(clean_date)
		row.append(scrape.ranking)
		row.append(scrape.avg_score)
		row.append(scrape.review_count)
		row.append(scrape.num_hotels)

		rows.append(row)

	# run queries for each of the hotels and parse out the data
	for hotel in chosen_hotels:
		
		# do a query
		scrapes = Scrape.query.filter(Scrape.hotel_id == hotel).all()

		# loop through scrape information to parse out data
		for scrape in scrapes:

			row = []

			# address weekly setting
			if timeframe_choice == 'Weekly':

				# if the shop is on a Sunday, get data
				if (scrape.shop_timestamp.weekday() == 6) and (scrape.shop_timestamp > six_months_ago):
					add_data_to_row()

			# address daily setting
			elif timeframe_choice == 'Daily':

				# if the shop is after thirty days ago:
				if scrape.shop_timestamp > thirty_days_ago:
					add_data_to_row()

	return rows

from jinja2 import StrictUndefined
from flask import Flask, render_template, request, redirect, flash, session, jsonify, Markup
from flask_debugtoolbar import DebugToolbarExtension
from model import *
from functions import *
import manage_set_funcs
import re

app = Flask(__name__)

# required to run Flask sessions and debug toolbar
app.secret_key = 'ABC123'

# gives an error in jinga template if undefined variable rather than failing silently
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def show_login_form():
	"""Displays the login form"""

	return render_template('home.html')


@app.route('/login')
def check_user_password():
	"""Checks the user provided email and password to ensure a match"""

	entered_email = request.args.get('email')
	entered_password = request.args.get('password')
	
	# validate user entry
	try:
		# try to get user by the entered email address
		stored_user = User.query.filter(User.email == entered_email).one()

		# if user exists and password is correct
		if stored_user.password == entered_password:

			# set the session id to be the user_id in the database
			session['user_id'] = stored_user.user_id
			message = Markup('<div class="alert alert-success" role="alert">You are logged in.</div>')
			flash(message)

			# if user hasn't set a default view, send them to page to set up comp set
			if stored_user.default_view is None:
				message = Markup('<div class="alert alert-secondary" role="alert">Please define a comp set to continue.</div>')
				flash(message)
				return redirect('/create')

			# if they do have a default page send them to the main dashboard and set initial session values for chart
			else:
				set_initial_session_options()
				return redirect('/dashboard')

		# if user exists but password is incorrect			
		elif stored_user.password != entered_password:
			message = Markup('<div class="alert alert-danger" role="alert">Password is incorrect. Please try again.</div>')
			flash(message)	
			return redirect('/')

		# if attempt to get user fails it is due to user not existing
	except:
		message = Markup('<div class="alert alert-danger" role="alert">That email does not exist. Please check spelling or register below.</div>')
		flash(messagae)
		return redirect('/')


@app.route('/register')
def show_registration_form():
	"""Displays registration form."""

	return render_template('register.html')


@app.route('/register', methods=['POST'])
def handle_registration():
	"""Push user info to database"""

	new_email = request.form.get('email')
	new_password = request.form.get('password')

	if User.query.filter(User.email==new_email).all():
		message = Markup('<div class="alert alert-warning" role="alert">This email address already exists. Please use a different email address.</div>')
		flash(message)
		return redirect('/register')

	else:
		new_user = User(email=new_email, password=new_password)

		db.session.add(new_user)
		db.session.commit()

		message = Markup('<div class="alert alert-success" role="alert">You have successfully registered! Please log in with your new credentials.</div>')
		flash(message)

		return redirect('/')	


@app.route('/create')
def show_manage_compset():
	"""Displays manage compset page"""
	
	return render_template('create.html')

@app.route('/hotels.json')
def create_hotels_json():
	"""Takes all hotels and converts them to JSON"""

	hotels = get_hotel_information()

	return jsonify(hotels)


@app.route('/set_comp_set', methods=["POST"])
def process_new_set():
	"""Takes in new comp set and processes it"""
	
	submission = request.form

	submit_to_database(submission)

	# set session placeholders
	set_initial_session_options()

	message = Markup('<div class="alert alert-success" role="alert">Your comp set has been submitted.</div>')
	flash(message)

	return redirect('/dashboard')


@app.route('/dashboard')
def show_dashboard():
	"""Displays dashboard page"""

	user, views, default_view, non_default_views, metrics, timeframes, hotels_in_view = set_initial_inputs()

	return render_template('dashboard.html', user=user,
											 views=views,
											 default_view=default_view,
											 non_default_views=non_default_views,
											 metrics=metrics,
											 timeframes=timeframes,
											 hotels_in_view=hotels_in_view)


@app.route('/set-chart-inputs.json', methods=['POST'])
def set_chart_inputs():
	"""Takes inputs from dashboard and update session/chart accordingly"""

	inputs = request.form

	session['set_choice'] = int(inputs['comp_set_choice'])
	session['metric_choice'] = inputs['metric_choice']
	session['timeframe_choice'] = inputs['timeframe_choice']
	session['hotels_selection'] = [int(hotel) for hotel in (inputs.getlist('hotels_selection[]'))]

	session.modified = True

	chart_data = get_chart_data()

	return jsonify(chart_data)


@app.route('/get-comp-set-hotels.json')
def get_comp_set_hotels():
	"""Gets view id for comp set from dashboard and returns the hotel ids"""

	inputs = request.args
	comp_set_choice = int(inputs['comp_set_choice'])

	view_hotels = ViewHotel.query.filter(ViewHotel.view_id == comp_set_choice).all()

	view_hotel_dicts = []
	new_selected_hotels = []

	# create a dictionary of view objects (and add hotel_ids to a new list)
	for view_hotel_obj in view_hotels:
		view_hotel_dicts.append(view_hotel_obj.viewhotel_to_dict())
		new_selected_hotels.append(view_hotel_obj.hotel_id)

	# update the session with the items that changed
	session['hotels_selection'] = new_selected_hotels
	session['set_choice'] = comp_set_choice
	session.modified = True

	return jsonify(view_hotel_dicts)


@app.route('/add-hotel')
def display_add_hotel_form():
	"""Renders template to add new hotel"""

	return render_template('add_hotel.html')

@app.route('/add-hotel-submission', methods=['POST'])
def handle_new_hotel_submission():
	"""Takes user input and submits it to database."""

	inputs = request.form

	submit_new_hotel(inputs)

	return redirect('/add-hotel')


@app.route('/manage')
def display_manage_set():
	"""Displays manage comp set html file"""

	return render_template('manage.html')


@app.route('/sets.json')
def get_comp_set_info():
	"""Gets all needed info about comp sets and returns a json object of data"""

	# get a list of hotel dictionaries which include hotel_id and hotel_name
	hotels = get_hotel_information()

	# get default view, list of dicts of view_num and view_name, and dictionary of all hotel_ids associated with a view
	default_view, view_names, hotels_in_views = manage_set_funcs.get_all_view_info()

	return jsonify({
				'hotels' : hotels,
				'default_view' : default_view,
				'view_names' : view_names,
				'hotels_in_views' : hotels_in_views
				})

@app.route('/handle-set-changes', methods=['POST'])
def handle_set_changes():
	"""Takes in changes to comp set and processes them"""

	inputs = request.form

	print('\n\ninputs from React:', inputs, '\n\n')

	return manage_set_funcs.handle_set_changes(inputs)

if __name__ == '__main__':

    app.debug = True

    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
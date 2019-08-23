
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import *
from functions import *

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
			flash('You are logged in.')

			# if user hasn't set a default view, send them to page to set up comp set
			if stored_user.default_view is None:
				flash('Please define a comp set to continue')
				return redirect('/create')

			# if they do have a default page send them to the main dashboard and set initial session values for chart
			else:
				set_initial_session_options()
				return redirect('/dashboard')

		# if user exists but password is incorrect			
		elif stored_user.password != entered_password:
			flash('Password is incorrect. Please try again.')	
			return redirect('/')

		# if attempt to get user fails it is due to user not existing
	except:
		flash('That email does not exist. Please check spelling or register below.')
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
		flash('This email address already exists. Please use a different email address.')
		return redirect('/register')

	else:
		new_user = User(email=new_email, password=new_password)

		db.session.add(new_user)
		db.session.commit()

		flash('You have successfully registered!')
		flash('Please log in with your new credentials')

		return redirect('/')	


@app.route('/create')
def show_manage_compset():
	"""Displays manage compset page"""
	
	return render_template('create.html')

@app.route('/hotels.json')
def create_hotels_json():
	"""Takes all hotels and converts them to JSON"""

	# get a list of all hotel objects
	db_hotels = Hotel.query.all()

	hotels = []

	# loop through each hotel object and add hotel id and hotel name to the list in key:value pairs
	for hotel_obj in db_hotels:
		hotel = {"hotel_id":hotel_obj.hotel_id, "hotel_name":hotel_obj.hotel_name}
		hotels.append(hotel)

	return jsonify(hotels)


@app.route('/set_comp_set', methods=["POST"])
def process_new_set():
	"""Takes in new comp set and processes it"""
	
	submission = request.form

	submit_to_database(submission)

	# set session placeholders
	set_initial_session_options()

	flash('Your comp set has been submitted.')

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

@app.route('/set-chart-inputs', methods=['POST'])
def set_chart_inputs():
	"""Takes inputs from dashboard rendering and update session accordingly"""

	inputs = request.form

	print('\n\n\n\n', inputs)

	session['set_choice'] = int(inputs['comp_set_choice'])
	session['metric_choice'] = inputs['metric_choice']
	session['timeframe_choice'] = inputs['timeframe_choice']
	session['hotels_selection'] = [int(hotel) for hotel in (inputs.getlist('hotel'))]

	session.modified = True

	# will query database, return jsonify, then in dashboard callback will update chart data

	return jsonify({'cat':2})

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
		view_hotel_dicts.append(view_hotel_obj.to_dict())
		new_selected_hotels.append(view_hotel_obj.hotel_id)

	# update the session with the items that changed
	session['hotels_selection'] = new_selected_hotels
	session['set_choice'] = comp_set_choice
	session.modified = True

	return jsonify(view_hotel_dicts)

if __name__ == '__main__':

    app.debug = True

    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
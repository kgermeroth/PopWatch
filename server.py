
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import *

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
		print("\n\n\n\n\n\n\n\nWell we tried to query!")
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

			# if they do have a default page send them to the main dashboard
			else:
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

	default = False

	if submission.get('default') == 'true':
		default = True

	# this returns a list of all hotel choices where the choice is zero
	hotel_choices = submission.getlist('hotel_choice[]')

	view_name = submission['view_name']

	user_id = int(session['user_id'])

	# instantiate a View object and commit to database
	view = View(user_id=user_id,
				view_name=view_name)
	
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


	flash('Your comp set has been submitted.')

	return redirect('/dashboard')

@app.route('/dashboard')
def show_dashboard():
	"""Displays dashboard page"""

	return render_template('dashboard.html')


if __name__ == '__main__':

    app.debug = True

    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
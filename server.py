
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, redirect, flash, session
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
		stored_user = User.query.filter(User.email == entered_email).one()

		# if user exists and password is correct
		if stored_user.password == entered_password:

			# set the session id to be the user_id in the database
			session['user_id'] = stored_user.user_id
			flash('You are logged in.')

			# if user hasn't set a default view, send them to page to set up comp set
			if stored_user.default_view is None:
				flash('Please define a comp set to continue')
				return redirect('/manage')

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

	if User.query.filter(User.email==new_email):
		flash('This email address already exists. Please use a different email address.')
		return redirect('/register')

	else:
		new_user = User(email=new_email, password=new_password)

		db.session.add(new_user)
		db.session.commit()

		flash('You have successfully registered!')
		flash('Please log in with your new credentials')

		return redirect('/')	


@app.route('/manage')
def show_mange_compset():
	"""Displays manage compset page"""
	
	return render_template('manage_ph.html')

@app.route('/dashboard')
def show_dashboard():
	"""Displays dashboard page"""

	return render_template('dashboard_ph.html')


if __name__ == '__main__':

    app.debug = True

    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
from server import *
from model import Hotel, Scrape, User, View, ViewHotel, db
from flask import Flask, render_template, request, redirect, flash, session, jsonify, Markup
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
		flash(message)

		return redirect('/manage')

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
		original = set()
		for view_hotel in view.viewhotels:
			original.add(view_hotel.hotel_id)

		print('original:', original)

		submitted = set()

		for hotel in (inputs.getlist('hotels_in_set[]')):
			submitted.add(int(hotel))

		print('submitted', submitted)

		# hotels to be deleted = original set - submitted set
		to_delete = original - submitted

		for hotel in to_delete:
			delete_view = ViewHotel.query.filter(ViewHotel.view_id == view_id, ViewHotel.hotel_id == hotel).one()
			db.session.delete(delete_view)
			db.session.commit()

		# hotels to be added = new set - original set
		to_add = submitted - original

		for hotel in to_add:
			add_view = ViewHotel(view_id=view_id, hotel_id=hotel)
			db.session.add(add_view)
			db.session.commit()

		message = Markup('<div class="alert alert-success" role="alert">Your comp set has been successfully updated.</div>')
		flash(message)

	# check to see if user default is empty after changes, and if so either assign a new comp set or dump user on create set page
	user = User.query.filter(User.user_id == user_id).one()
	if not user.default_view:
		print('the if statement ran ok')
		avail_views = user.views
		print('avail_views', avail_views)
		# if there are no views, redirect to create set page and flash message comp set must be created
		if not avail_views:
			message = Markup('<div class="alert alert-danger" role="alert">You have no defined comp sets. Please create one to continue.</div>')
			flash(message)
			return redirect('/create')

		# if there are views, choose the first one and assign it as the default
		else:
			user.default_view = avail_views[0].view_id
			db.session.add(user)
			db.session.commit()
			session['set_choice'] = user.default_view

			default_hotels = ViewHotel.query.filter(ViewHotel.view_id == user.default_view)
			session['hotels_selection'] = [hotel_view.hotel_id for hotel_view in default_hotels]
			session.modified = True
			message = Markup(f'<div class="alert alert-warning" role="alert">{avail_views[0].view_name} has been assigned as your current default.</div>')
			flash(message)
	else:
		session['set_choice'] = user.default_view
		default_hotels = ViewHotel.query.filter(ViewHotel.view_id == user.default_view)
		session['hotels_selection'] = [hotel_view.hotel_id for hotel_view in default_hotels]
		session.modified = True



				


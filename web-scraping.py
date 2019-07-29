import webbrowser
import bs4
import requests
import re
import csv
import time
from datetime import datetime

def get_html_data(url):
	"""Goes to URL and downloads html"""

	# download the main page from the website
	full_page = requests.get(url)

	full_page.raise_for_status()

	return full_page.text

def write_html_to_file(full_page, file_to_save_to):
	"""Writes data to a text file"""

	# creates a new text file and opens it in write mode
	text_file = open(file_to_save_to, 'w')

	# convert the url content to text and write to the file
	text_file.write(full_page)

	text_file.close()

	#add a datetime object here and return it?

	return file_to_save_to

def use_html_file(file_to_save_to):
	"""Takes in html file and coverts it to Beautiful Soup object"""

	with open(file_to_save_to, 'r') as f:
		the_text = f.read()

	soup_object = bs4.BeautifulSoup(the_text)

	return soup_object

def get_data_out_of_soup(soup_object):
	"""Take beautiful soup object and pull out releveant data"""

	# pull html with rank information out of soup object
	rankhtml = soup_object.find('span', class_='header_popularity popIndexValidation ui_link level_4').text

	# Match the rank # and number of hotels in the rank_text
	match_obj = re.search(r'\#(\d+) of (\d+)', rankhtml)
	rank = int(match_obj.group(1))
	num_all_hotels = int(match_obj.group(2))

	# Pull html with avg review score out of soup object and convert to float
	avgscore = float(soup_object.find('span', class_='hotels-hotel-review-about-with-photos-Reviews__overallRating--vElGA').text)

	# parse out review count and find num of reviews with regex
	reviewcount_html = soup_object.find('span', class_='reviewCount ui_link level_4').text
	match_obj = re.search(r'([0-9,]+)', reviewcount_html)
	reviewcount = match_obj.group(1)

	# need to account for commas before converting to int
	if len(reviewcount) < 4:															#less than 1,000 reviews
		reviewcount = int(reviewcount)

	elif len(reviewcount) > 3 and len(reviewcount) < 8:									#1,000 - 999,999 reviews
		reviewcount = int((reviewcount[:-4] + reviewcount[-3:]))

	else:																				#more 999,999 reviews
		reviewcount = int((reviewcount[:-8] + reviewcount[-7:-4] + reviewcount[-3:]))


	return (rank, avgscore, num_all_hotels, reviewcount)

def get_time_stamps():
	"""Collects time stamp after successful shop"""

	now = datetime.now()

	return now

def create_html_file_name(hotel_id, now):
	"""Creates custom file name to save html data to"""
	


def store_data_in_csv():
	"""Store all data in csv file"""
	pass

def scrape_store_webpages(filename):
	"""Compiles all pieces of webscraping process
	- pull hotel info from file. For each hotel:
		- scrape html data from TripAdvisor
		- collect approx time stamp of shop
		- create a filename to save data to
		- save data to that html file
		- parse data from html file
		- save data to master csv file
		- wait 5 minutes to shop next hotel """

	website_file = open(filename)

	for line in website_file:
		hotel, hotel_id, web_url = line.rstrip().split('|')


	website_file.close()




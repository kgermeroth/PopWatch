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

def write_html_to_file(full_page, filename):
	"""Writes data to a text file"""

	filepath = 'hotel_html_pages/' + filename

	# creates a new text file and opens it in write mode
	text_file = open(filepath, 'w')

	# convert the url content to text and write to the file
	text_file.write(full_page)

	text_file.close()

	return filepath

def convert_html_file(file_to_save_to):
	"""Takes in html file and coverts it to Beautiful Soup object"""

	with open(file_to_save_to, 'r') as f:
		the_text = f.read()

	soup_object = bs4.BeautifulSoup(the_text)

	return soup_object

def get_data_out_of_soup(soup_object):
	"""Take beautiful soup object and pull out releveant data"""

	# pull html with rank information out of soup object
	rankhtml = soup_object.find('span', class_='header_popularity')

	if rankhtml is None:
		num_all_hotels = ''
		rank = ''

	else:
		# Match the rank # and number of hotels in the rank_text
		rankhtml = rankhtml.text
		match_obj = re.search(r'\#(\d+) of (\d+)', rankhtml)
		rank = int(match_obj.group(1))
		num_all_hotels = int(match_obj.group(2))

	# Pull html with avg review score out of soup object and convert to float
	avgscore = soup_object.find('span', class_='hotels-hotel-review-about-with-photos-Reviews__overallRating--vElGA')

	if avgscore is None:
		avgscore = ''

	else:
		avgscore = float(avgscore.text)


	# parse out review count and find num of reviews with regex
	reviewcount_html = soup_object.find('span', class_='reviewCount')

	if reviewcount_html is None:
		reviewcount = ''

	else:
		reviewcount_html = reviewcount_html.text
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

def get_time_stamp():
	"""Collects time stamp after successful shop"""

	now = datetime.now()

	return now

def create_html_file_name(hotel_id, now):
	"""Creates custom file name to save html data to"""

	return hotel_id + str(now.year) + str(now.month) + str(now.day) + '.html'
	

def store_data_in_csv(hotelname, filename, now, rank, num_all_hotels, avgscore, reviewcount):
	"""Store all data in one row of the csv file"""

	date_shopped = str(now.month) + '/' + str(now.day) + '/' + str(now.year)
	time_shopped = str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)

	row = [hotelname, filename[:-5], date_shopped, time_shopped, rank, num_all_hotels, avgscore, reviewcount]

	with open('hotel_data.csv', 'a') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerow(row)

	csvFile.close()	


def scrape_store_webpages():
	"""Compiles all pieces of webscraping process
	- pull hotel info from file. For each hotel:
		- scrape html data from TripAdvisor
		- collect approx time stamp of shop
		- create a filename to save data to
		- save data to that html file
		- parse data from html file
		- save data to master csv file
		- wait 5 minutes to shop next hotel """

	hotel_info_file = open('hotel_shopping_info.txt')

	for line in hotel_info_file:
		hotelname, hotel_id, web_url = line.rstrip().split('|')

		text = get_html_data(web_url)						# pull html from webpage
		now = get_time_stamp()								# get the time stamp
		filename = create_html_file_name(hotel_id, now)		# creates a filename html file will be stored in
		filepath = write_html_to_file(text, filename)		# takes html text and puts it into a file with the created filename
		soup_object = convert_html_file(filepath)			# takes the html file and converts it into a soup object
		rank, avgscore, num_all_hotels, reviewcount = get_data_out_of_soup(soup_object) 	# takes soup object and parses it to pull data
		store_data_in_csv(hotelname, filename, now, rank, num_all_hotels, avgscore, reviewcount)	# takes all data and writes it to csv file


		# wait five minutes until next shop
		time.sleep(200)


	hotel_info_file.close()




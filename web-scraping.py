import webbrowser, requests, re, csv, time, os
from datetime import datetime
from model import *

def get_html_data(url):
	"""Goes to URL and downloads html"""

	# download the main page from the website
	full_page = requests.get(url)

	full_page.raise_for_status()

	return full_page.text

def get_ta_id(url):
	"""Gets the TripAdvisor id out of URL"""

	match_obj = re.search(r'view-(\w+-\w+)', url)

	return match_obj.group(1)

def get_time_stamp():
	"""Collects time stamp after successful shop"""

	return datetime.datetime.now()


def create_html_file_name(hotel_id, now):
	"""Creates custom file name to save html data to"""

	return str(hotel_id) + str(now.year) + str(now.month) + str(now.day) + '.html'


def write_html_to_file(full_page, filename):
	"""Writes data to a text file"""

	working_dir = str(os.path.dirname(os.path.realpath(__file__)))

	filepath = working_dir + '/hotel_html_pages/' + filename

	# creates a new text file and opens it in write mode
	text_file = open(filepath, 'w')

	# convert the url content to text and write to the file
	text_file.write(full_page)

	text_file.close()

	return filepath


def use_regex(file_to_save_to):
	"""Opens HTML file and uses Regex to get information"""

	# open the html file and get data out
	with open(file_to_save_to, 'r') as f:
		the_text = f.read()

	#find ranking and total number of hotels
	match_obj = re.search(r'ranked #(\d+) of (\d+)', the_text)

	if not match_obj: 
		rank = ''
		num_hotels = ''
	else:
		rank = int(match_obj.group(1))
		num_hotels = int(match_obj.group(2))

	# find the ranking
	match_obj = re.search(r'rated (\d?\.?\d+) of', the_text)

	if not match_obj: 
		avgscore = ''
	else:
		avgscore = float(match_obj.group(1))

	# find review count
	match_obj = re.search(r'See (\d?\,?\d+) traveler', the_text)
	
	if not match_obj:
		reviewcount = ''
	else:
		reviewcount = match_obj.group(1)
		# need to account for commas before converting to int
		if len(reviewcount) < 4:															#less than 1,000 reviews
			reviewcount = int(reviewcount)

		elif len(reviewcount) > 3 and len(reviewcount) < 8:									#1,000 - 999,999 reviews
			reviewcount = int((reviewcount[:-4] + reviewcount[-3:]))

		else:																				#more 999,999 reviews
			reviewcount = int((reviewcount[:-8] + reviewcount[-7:-4] + reviewcount[-3:]))

	return (rank, avgscore, num_hotels, reviewcount)


def store_data_in_csv(hotel_id, ta_id, now, rank, num_hotels, avgscore, reviewcount):
	"""Store all data in one row of the csv file"""

	row = [hotel_id, ta_id, now.isoformat(), rank, num_hotels, avgscore, reviewcount]

	working_dir = str(os.path.dirname(os.path.realpath(__file__)))

	with open(working_dir + '/hotel_data.csv', 'a') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerow(row)


def store_data_in_database(hotel_id, ta_id, now, rank, num_hotels, avgscore, reviewcount):
	"""Store all data in the database."""
	# need to account for NULLs. Postgres will not accept empty values or incorrect type
	# The '0' strings are to give a falsey value in case the variable is null, otherwise will get an error if variable is null
	
	rank = int(rank or '0') or None
	num_hotels = int(num_hotels or '0') or None
	avgscore = float(avgscore or '0') or None
	reviewcount = int(reviewcount or '0') or None
		
		# instantiate a scrape object with the shop data
	scrape = Scrape(hotel_id=hotel_id,
					ta_id=ta_id,
					shop_timestamp=now,
					ranking=rank,
					num_hotels=num_hotels,
					avg_score=avgscore,
					review_count=reviewcount)

	db.session.add(scrape)
	db.session.commit()


def scrape_store_webpages():
	"""Compiles all pieces of webscraping process

	Covers from downloading html up to storing data in csv.

 	"""
	# pull all hotel objects from database
	hotels = Hotel.query.all()

	# loop through all the hotels and assign the needed variables
	for hotel in hotels:
		hotel_id = hotel.hotel_id
		web_url = hotel.ta_url

		# do all the magic :)
		text = get_html_data(web_url)																# pull html from webpage
		ta_id = get_ta_id(web_url)																	# pulls TripAdvisor id out of URL
		now = get_time_stamp()																		# get the time stamp
		filename = create_html_file_name(hotel_id, now)												# creates a filename for the file html will be stored in
		filepath = write_html_to_file(text, filename)												# takes html text and puts it into a file with the created filename
		rank, avgscore, num_hotels, reviewcount = use_regex(filepath)							# takes html file and parses with regex
		store_data_in_csv(hotel_id, ta_id, now, rank, num_hotels, avgscore, reviewcount)		# takes all data and writes it to csv file
		store_data_in_database(hotel_id, ta_id, now, rank, num_hotels, avgscore, reviewcount)	# takes all data and writes it to database

		# wait 60 seconds until next shop (prevent TripAdvisor lockout)
		time.sleep(60)

if __name__ == '__main__':
	init_app()
	scrape_store_webpages()




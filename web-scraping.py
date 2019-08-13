import webbrowser, bs4, requests, re, csv, time
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

	return datetime.now()


def create_html_file_name(hotel_id, now):
	"""Creates custom file name to save html data to"""

	return hotel_id + str(now.year) + str(now.month) + str(now.day) + '.html'


def write_html_to_file(full_page, filename):
	"""Writes data to a text file"""

	filepath = '/media/storage/home/kristin/src/TripAdvisor_Project/hotel_html_pages/' + filename

	# creates a new text file and opens it in write mode
	text_file = open(filepath, 'w')

	# convert the url content to text and write to the file
	text_file.write(full_page)

	text_file.close()

	return filepath


def convert_html_file(file_to_save_to):
	"""Takes in html file and coverts it to Beautiful Soup object"""

	# open the html file and get data out
	with open(file_to_save_to, 'r') as f:
		the_text = f.read()

	# turn html into a beautifulsoup object
	soup_object = bs4.BeautifulSoup(the_text, features="html.parser")

	return soup_object


def get_data_out_of_soup(soup_object):
	"""Take beautiful soup object and pull out releveant data"""

	# pull html with rank information out of soup object
	rankhtml = soup_object.find('span', class_='header_popularity')

	# have to account for any missing class names when html doesn't pull properly
	if rankhtml is None:
		num_hotels = ''
		rank = ''

	else:
		# Match the rank # and number of hotels in the rank_text
		rankhtml = rankhtml.text
		match_obj = re.search(r'\#(\d+) of (\d+)', rankhtml)
		rank = int(match_obj.group(1))
		num_hotels = int(match_obj.group(2))

	# Pull html with avg review score out of soup object and convert to float
	avgscore = soup_object.find('span', class_='hotels-hotel-review-about-with-photos-Reviews__overallRating--vElGA')

	# have to account for any missing class names when html doesn't pull properly
	if avgscore is None:
		avgscore = ''

	else:
		avgscore = float(avgscore.text)


	# parse out review count and find num of reviews with regex
	reviewcount_html = soup_object.find('span', class_='reviewCount')

	# have to account for any missing class names when html doesn't pull properly
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


	return (rank, avgscore, num_hotels, reviewcount)
	

def store_data_in_csv(hotel_id, ta_id, now, rank, num_hotels, avgscore, reviewcount):
	"""Store all data in one row of the csv file"""

	row = [hotel_id, ta_id, now.isoformat(), rank, num_hotels, avgscore, reviewcount]

	with open('/media/storage/home/kristin/src/TripAdvisor_Project/hotel_data.csv', 'a') as csvFile:
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
 	# use csv to do shops:
	# hotel_info_file = open('/media/storage/home/kristin/src/TripAdvisor_Project/hotel_shopping_info.txt')

	# for line in hotel_info_file:
	# 	hotel_id, hotelname, nickname, web_url = line.rstrip().split('|')

	# pull all hotel objects from database
	hotels = Hotel.query.all()

	# loop through all the hotels and assign the needed variables
	for hotel in hotels:
		hotel_id = hotel.hotel_id
		nickname = hotel.hotel_nickname
		web_url = hotel.ta_url

		# do all the magic :)
		text = get_html_data(web_url)																# pull html from webpage
		ta_id = get_ta_id(web_url)																	# pulls TripAdvisor id out of URL
		now = get_time_stamp()																		# get the time stamp
		filename = create_html_file_name(nickname, now)												# creates a filename for the file html will be stored in
		filepath = write_html_to_file(text, filename)												# takes html text and puts it into a file with the created filename
		soup_object = convert_html_file(filepath)													# takes the html file and converts it into a soup object
		rank, avgscore, num_hotels, reviewcount = get_data_out_of_soup(soup_object) 			# takes soup object and parses it to pull data
		store_data_in_csv(hotel_id, ta_id, now, rank, num_hotels, avgscore, reviewcount)		# takes all data and writes it to csv file
		store_data_in_database(hotel_id, ta_id, now, rank, num_hotels, avgscore, reviewcount)

		# wait two minutes until next shop
		time.sleep(120)


	hotel_info_file.close()

if __name__ == '__main__':
	init_app()
	scrape_store_webpages()




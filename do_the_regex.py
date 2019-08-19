import webbrowser, requests, re, csv
from model import *

def use_regex(file_to_save_to):
	"""Opens HTML file and uses Regex to get information"""

	# open the html file and get data out
	with open(file_to_save_to, 'r') as f:
		the_text = f.read()

	#find ranking and total number of hotels
	match_obj = re.search(r'ranked #(\d+) of (\d+)', the_text)
	if match_obj is None:
		rank = ''
		num_hotels = ''

	else:
		rank = int(match_obj.group(1))
		num_hotels = int(match_obj.group(2))

	# find the ranking
	match_obj = re.search(r'rated (\d?\.?\d+) of', the_text)
	if match_obj is None:
		avgscore = ''

	else: 
		avgscore = float(match_obj.group(1))


	# find review count
	match_obj = re.search(r'See (\d?\,?\d+) traveler', the_text)
	if match_obj is None:
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


def store_data_in_csv(hotel_id, ta_id, datestamp, rank, num_hotels, avgscore, reviewcount):
	"""Store all data in one row of the csv file"""

	row = [hotel_id, ta_id, datestamp, rank, num_hotels, avgscore, reviewcount]

	with open('/media/storage/home/kristin/src/TripAdvisor_Project/new_data.csv', 'a') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerow(row)


def redo_data():
	"""Compiles all pieces of webscraping process

	Covers from downloading html up to storing data in csv.

 	"""
	the_text = open('hotel_data.csv')

	for line in the_text:
		hotel_id, ta_id, datestamp, *sadstuff = line.rstrip().split(',')

	# get file name
		regex_object = re.search(r'2019-(\d+)-(\d+)T', datestamp)

		month = regex_object.group(1)
		if month[0] == '0':
			month = month[1]

		day = regex_object.group(2)
		if day[0] == '0':
			day = day[1]

		filepath = 'hotel_html_pages/' + hotel_id + '2019' + month + day + '.html'

		# do all the magic :)
		rank, avgscore, num_hotels, reviewcount = use_regex(filepath)							# takes html file and parses with regex
		store_data_in_csv(hotel_id, ta_id, datestamp, rank, num_hotels, avgscore, reviewcount)		# takes all data and writes it to csv file


	the_text.close()


# to do:
		
	# loop through hotel_data file!!
		# split string on comma with hotel_id, ta_id, datestamp, *sadstuff

		# get the file name:
			# regex object = r'(2019-(\d+)-(\d+)T, datestring)				
			# hotel_id + 2019 + int(group1)(removing leading 0 separate out function earlier!) + (intgroup2)(remove leading 0 separate function out earlier)+ 'html'
		# open the file
		# feed it into html function, get the good stuff
		# create the row = [hotel_id, ta_id, datestamp, rank, num_hotels, avgscore,reviewcount]
		# add it to the csv file




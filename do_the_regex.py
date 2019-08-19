def get_ta_id(url):
	"""Gets the TripAdvisor id out of URL"""

	match_obj = re.search(r'view-(\w+-\w+)', url)

	return match_obj.group(1)

def use_regex(file_to_save_to):
	"""Opens HTML file and uses Regex to get information"""

	# open the html file and get data out
	with open(file_to_save_to, 'r') as f:
		the_text = f.read()

	#find ranking and total number of hotels
	match_obj = re.search(r'ranked #(\d+) of (\d+)', the_text)
	rank = match_obj.group(1)
	num_hotels = match_obj.group(2)

	if rank is None:
		rank = ''
	else:
		rank = int(rank)

	if num_hotels is None:
		num_hotels = ''
	else:
		num_hotels = int(num_hotels)

	# find the ranking
	match_obj = re.search(r'rated (\d?\.?\d+) of', the_text)
	avgscore = match_obj.group(1)

	if avgscore is None:
		avgscore = ''
	else:
		avgscore = float(avgscore)

	# find review count
	match_obj = re.search(r'See (\d?\,?\d+) traveler', the_text)
	reviewcount = match_obj.group(1)

	if reviewcount is None:
		reviewcount = ''
	else:
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


def scrape_store_webpages():
	"""Compiles all pieces of webscraping process

	Covers from downloading html up to storing data in csv.

 	"""
 
		# do all the magic :)
		text = get_html_data(web_url)																# pull html from webpage
		ta_id = get_ta_id(web_url)																	# pulls TripAdvisor id out of URL
		now = get_time_stamp()																		# get the time stamp
		filename = create_html_file_name(nickname, now)												# creates a filename for the file html will be stored in
		filepath = write_html_to_file(text, filename)												# takes html text and puts it into a file with the created filename
		rank, avgscore, num_hotels, reviewcount = use_regex(filepath)							# takes html file and parses with regex
		store_data_in_csv(hotel_id, ta_id, now, rank, num_hotels, avgscore, reviewcount)		# takes all data and writes it to csv file


	hotel_info_file.close()


# to do:

		# change file names to use hotel_ids? - yes!
			# also update the code that creates the data so all files are saved this way
		
	# loop through hotel_data file!!
		# split string on comma with hotel_id, ta_id, datestamp, *sadstuff

		# get the file name:
			# regex object = r'(2019-(\d+)-(\d+)T, datestring)				# 
			# hotel_id + 2019 + int(group1)(removing leading 0 separate out function earlier!) + (intgroup2)(remove leading 0 separate function out earlier)+ 'html'
		# open the file
		# feed it into html function, get the good stuff
		# create the row = [hotel_id, ta_id, datestamp, rank, num_hotels, avgscore,reviewcount]
		# add it to the csv file




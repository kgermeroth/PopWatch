import webbrowser
import bs4
import requests

def open_webpages(filename):
	"""Opens the webpages of the comp set hotels"""

	website_file = open(filename)

	for line in website_file:
		webbrowser.open(line.rstrip().split('|')[1])

	website_file.close()

def get_html_for_testing(url, file_to_save_to):
	"""Goes to URL, downloads html, and writes to a text file"""

	# download the main page from the website
	full_page = requests.get(url)

	full_page.raise_for_status()

	# creates a new text file and opens it in write mode
	text_file = open(file_to_save_to, 'w')

	# convert the url content to text and write to the file
	text_file.write(full_page.text)

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
	"""Take beautiful soup object and pull out releveant data
	
	#review count results
	>>>reviewcountstring = str(soup_object.find_all("span", class_="reviewCount ui_link level_4"))
	[<span class="reviewCount ui_link level_4">3,845 reviews</span>]

	"""
	# pull html with rank information out of soup object
	rankhtmlstring = soup_object("span", class_="header_popularity popIndexValidation ui_link level_4")

	rank_text = rankhtmlstring[0].text


	# parse out review count
	reviewcount_html = soup_object("span", class_="reviewCount ui_link level_4")

	reviewcount_text = reviewcount_html[0].text

	reviewcount = reviewcount_text[:reviewcount_text.index(" ")]

	# need to account for commas before converting to int
	if len(reviewcount) < 4:															#less than 1,000 reviews
		reviewcount = int(reviewcount)

	elif len(reviewcount) > 3 and len(reviewcount) < 8:									#1,000 - 999,999 reviews
		reviewcount = int((reviewcount[:-4] + reviewcount[-3:]))

	else:																				#more 999,999 reviews
		reviewcount = int((reviewcount[:-8] + reviewcount[-7:-4] + reviewcount[-3:]))

	return (reviewcount)

# to find the span with avg review score:
# >>> soup.find_all("span", {"class":"hotels-hotel-review-about-with-photos-Reviews__overallRating--vElGA"})
# [<span class="hotels-hotel-review-about-with-photos-Reviews__overallRating--vElGA">3.5</span>]

# this will find the rank and number of hotels in SF:
# >>> soup("span", class_="header_popularity popIndexValidation ui_link level_4")
# [<span class="header_popularity popIndexValidation ui_link level_4" onclick="ta.util.cookie.setPIDCookie(15191);"><b class="rank">#136</b> of 241 <a href="/Hotels-g60713-San_Francisco_California-Hotels.html">Hotels in San Francisco</a></span>]



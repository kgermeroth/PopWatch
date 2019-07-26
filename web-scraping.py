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
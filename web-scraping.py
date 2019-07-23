import webbrowser


def open_webpages(filename):
	"""Opens the webpages of the comp set hotels"""

	website_file = open(filename)

	for line in website_file:
		webbrowser.open(line.rstrip().split('|')[1])

	website_file.close()


# PopWatch

## Table of Contents

* [Summary](#summary)
* [Tech Stack](#tech-stack)
* [Setup/Installation](#setup)

## <a name="summary"></a>Summary
**PopWatch** is an easy-to-use tool for hoteliers to track TripAdvisor ranking, average score, and number of reviews for an unlimited number of user-defined competitive sets.

## <a name="tech-stack"></a>Tech Stack
__Front End:__ HTML5, Jinja2, CSS, JavaScript, AJAX, React, Bootstrap, chart.js<br/>
__Back End:__ Python, Flask, PostgreSQL, SQLAlchemy <br/>

## <a name="setup"></a>Setup/Installation

#### Requirements:

- Python 3.6.8
- PostgreSQL

To have this app running on your local computer, please follow the below steps:

Clone repository:
```
$ git clone https://github.com/kgermeroth/PopWatch.git
```

Create a virtual environment:
```
$ virtualenv env
```

Activate the virtual environment:
```
$ source env/bin/activate
```

Install dependencies:
```
$ pip3 install -r requirements.txt
```

Create database 'hotels':
```
$ createdb hotels
```

Create your database tables:
```
$ python3 model.py
```

Seed database with data (optional - provided data is from a selection of San Francisco hotels):
```
$ python3 seed.py
```

Data collection: the code in web-scraping.py needs to be run on a daily basis. Allow 60 seconds between hotels to be shopped. To run manually:
```
$ python3 web-scraping.py
```

Consider scheduling with cronjobs or similar. Note that filepaths in web-scraping.py (lines 37 and 100) may need to be absolute file paths.

Run app from the command line:
```
$ python3 server.py
```
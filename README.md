

<h1 align="center">
    <img width="100" src="https://repository-images.githubusercontent.com/229792945/c370bd80-267b-11ea-8dd0-eb1f97aa6e4f">
    <br>
    Blongo
</h1>

<p align=center>Blongo is an open-source Blog Web-App built on the Django Web Framework 2.x with Python3</p>

## About Blongo

[![](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![](https://img.shields.io/github/contributors/adityhere/Blongo.svg)](https://github.com/adityhere/Blongo/graphs/contributors)
![](https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7-blue.svg)

#### Features
* Generation of Atom and RSS feeds
* Generation of Sitemaps
* Post View Count
* Archive List with Yearly and Monthly categorization
* Tags for post
* [Trix](https://github.com/basecamp/trix) Rich Text Editor For Post Content
* Thumbnail/Cover Image for Post(supports image compression)
* Blog Configuration
* [Bootswatch 4 themes](https://www.bootstrapcdn.com/bootswatch/) (themes based on Bootstrap)

#### Dependencies
* [Django](https://pypi.org/project/Django/)
* pytz
* whitenoise
* [django-trix-fork](https://pypi.org/project/django-trix-fork/)

## Documentation

### Installation

##### To run Locally/Dev:
 1. Create a Python-3.x Virtual Environment [Creating Virtual Environments](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments)
 2. Install dependencies:
    `pip install -r requirements/dev.txt`
 3. Create a `.env` file with required environment variables (Sample -> [sample.env](sample.env))
 4. Create database schema
    `python manage.py makemigrations blog`
 5. Run the migrations
    `python manage.py migrate`
 6. Create a superuser
    `python manage.py createsuperuser`
 7. Create default Blog config 
    `python manage.py initialize_blog`
 8. Run Server
    `python manage.py runserver`

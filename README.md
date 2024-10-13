# Blog_App

## project Overview
The goal of the project is to create a blog web application using Python-Django, Tailwindcss The application will allow users to create Blog post,users can view a list of all posts with pagination, view the details of a specific blog post, edit and delete their own blog posts.. The data should persist by using a Mysql database.




## Setup

#### The first thing to do is to clone the repository:
$ git clone https://github.com/aswathy232/Blog_App.git
$ cd BlogProj
Create a virtual environment to install dependencies in and activate it:
$ virtualenv env
$ source env/bin/activate
Then install the dependencies:

(env)$ pip install -r requirements.txt or pip install i
Once pip has finished downloading the dependencies:

(env)$ cd blog
(env)$ python manage.py runserver
And navigate to http://127.0.0.1:8000

## for docker setup
$ docker-compose up --build


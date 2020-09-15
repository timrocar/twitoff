""" Main App/Routing File for Twitoff!"""


#import flask
from flask import Flask, render_template
from .models import DB, User, insert_example_users, insert_example_tweets

def create_app():
    #initializing flask and data models 
    app = Flask(__name__)

    #for storing inforomation in our database
    app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    #initializes database within our app
    DB.init_app(app)

    #listens for path '/' and executes function when heard
    @app.route('/')
    def root():
        #re creates our database to avoid errors and duplicates
        DB.drop_all()
        DB.create_all()
        #calls our function within the models.py file to insert users
        insert_example_users()
                
        #a select * query using SQLAlchemy
        users = User.query.all()
        # Rendering template that we creating passing home and query to template
        return render_template('base.html', title='Home', users=User.query.all())

    @app.route('/add_test_tweets')
    def add_tweets():
        insert_example_tweets()
        return 'tweets added'
    #returns the app with everything we are trying to render
    return app
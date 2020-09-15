""" Main App/Routing File for Twitoff!"""


#import flask
from flask import Flask, render_template
from .models import DB, User, Tweet
from .twitter import add_users, TWITTER_USERS

def create_app():
    #initializing flask and data models 
    app = Flask(__name__)

    #for storing information in our database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    #initializes database within our app
    DB.init_app(app)

    #listens for path '/' and executes function when heard
    @app.route('/')
    def root():
        # Rendering template that we creating passing home and query to template
        return render_template('base.html', title='Home', users=User.query.all())

    @app.route('/update')
    def update():
        # Reset the database
        add_users()  
        return render_template('base.html', title='Users updated!',
                               users=User.query.all())

    return app
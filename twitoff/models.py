""" SQLAlchemy models and utiliy functions for Twitoff!"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

#creating classes that act as 'tables' within our DB
class User(DB.Model):
    
    #creating columns using SQLAlchemy methods
    id = DB.Column(DB.BigInteger, primary_key=True) #primary key id
    name = DB.Column(DB.String(15), nullable=False) #str column that can't be null

    # for readability when accessesing info 
    def __repr__(self):
        return '-User {}-'.format(self.name)

class Tweet(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))

    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return '-Tweet {}-'.format(self.text)

#populates database when called (called in app.py)
def insert_example_users():
        #if we run multiple times error will occur. 
        tim = User(id=1, name='tim')
        elon = User(id=2, name='elon')
        #have to add our users then commit using SQLAlchemy
        DB.session.add(tim)
        DB.session.add(elon)
        DB.session.commit()

#adds tweets
def insert_example_tweets():
        t1 = Tweet(id=1 , text="Let's hope this works", user=tim)  
        t2 = Tweet(id=2 , text="Esperemos que esto funcione", user=elon) 
        t3 = Tweet(id=3 , text="Lass hoffen, dass das funktioniert", user=tim) 
        t4 = Tweet(id=4 , text="miejmy nadzieję, że to zadziała", user=elon) 
        t5 = Tweet(id=5 , text="Speriamo che funzioni", user=tim) 
        t6 = Tweet(id=6 , text="будем надеяться, что это сработает", user=elon)

        DB.session.add(t1)
        DB.session.add(t2)
        DB.session.add(t3)
        DB.session.add(t4)
        DB.session.add(t5)
        DB.session.add(t6)
        DB.session.commit()
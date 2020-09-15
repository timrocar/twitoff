""" SQLAlchemy models and utiliy functions for Twitoff!"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

#creating classes that act as 'tables' within our DB
class User(DB.Model):
    #creating columns using SQLAlchemy methods
    id = DB.Column(DB.BigInteger, primary_key=True) #primary key id
    name = DB.Column(DB.String(15), nullable=False) #str column;can't be null
    # Tweeet IDs are ordinal, so can be used to fetch only more recent
    newest_tweet_id = DB.Column(DB.BigInteger)


    # for readability when accessesing info 
    def __repr__(self):
        return '-User {}-'.format(self.name)

class Tweet(DB.Model):
    """tweets and their embeddings from Basilica."""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    embedding = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'),
                        nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return '-Tweet {}-'.format(self.text)

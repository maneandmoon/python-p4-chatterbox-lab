from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    username = db.Column(db.String)
    # created_at = db.Column(db.DateTime, server_default=db.func.now())
    # updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'body': self.body,
            'username': self.username,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    # flask db init
    # flask db revision --autogenerate -m'your message'
    # flask db upgrade
    # python seed.py

    #1. create model Productions
    #2. hook up Flask, Flask Migrate/alembic, Flask SQLAlchemy/SQLAlchemy 
    #3. migrate our model so that it shows up as a table in our app.db with the following commands:
    # flask db init - create template folders/files to handle migrations and database 
    # flask db revision --autogenerate -m 'message' OR flask db migrate - creates autogenerated alembic script that will populate our app.db 
        # there are some things that the autogenerated scripts cannot detect or will have trouble parsing (mostly happens when you are making a change to a previously created table/model)
        # worst comes to worst you can delete the migrations and instance folder and run flask db init again
    # flask db upgrade head - apply autogenerated script to most recent version
    #4. seeded our database (see seed.py)
    #5. we made our Flask routes in app.py
    #utilized SQLAlchemy query to access data from our database
    #https://docs.sqlalchemy.org/en/14/orm/query.html#the-query-object
    #SQLAlchemy (our ORM) automatically converts these database rows into Production instances

    # SerializerMixin to specify what columns/keyvalue pairs to include in our responses
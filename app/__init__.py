from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/george/learning/projects/InterviewPrepareHelper/database.db' 
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# from app import models
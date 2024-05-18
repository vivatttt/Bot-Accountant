from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = os.getenv('SECRET_KEY')

#добавляем секретный ключ для куки
app.secret_key = SECRET_KEY
# Устанавливаем срок действия куки сессии на 7 дней
app.permanent_session_lifetime = timedelta(days=7)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/george/learning/projects/InterviewPrepareHelper/database.db' 
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# from app import models
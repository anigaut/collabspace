# Import required frameworks/libraries
from flask import Flask, jsonify, request, render_template
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
import os

# Import necessary files and functions from the project
from models import *
from routes.student_routes import student
from routes.instructor_routes import instructor
from routes.TA_routes import ta
from routes.admin_routes import admin
from routes.authentication import auth
from routes.rag_routes import rag 
from routes.pdf_routes import pdf
from routes.chat_routes import chat

from celery_worker import celery_init_app
from celery.result import AsyncResult
# from tasks import send_deadline_reminder
from celery.schedules import crontab

# Initialize app
app = Flask(__name__)

# Setup CORS
CORS(app)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///collabspace_db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.app_context().push()
db.init_app(app)

# Initialize Flask migrate (allows to make changes to DB directly without deleting each time)
migrate = Migrate(app, db)

# Defines blueprints for routes based on users
app.register_blueprint(student, url_prefix="/api/student")
app.register_blueprint(instructor, url_prefix="/api/instructor")
app.register_blueprint(ta, url_prefix="/api/ta")
app.register_blueprint(admin, url_prefix="/api/admin")
app.register_blueprint(auth, url_prefix="/api/auth")
app.register_blueprint(rag, url_prefix="/api/rag")
app.register_blueprint(pdf, url_prefix="/api/pdf")
app.register_blueprint(chat, url_prefix="/api/chat")

# JWT initializing for authentication
app.config['JWT_SECRET_KEY'] = os.urandom(24)
jwt = JWTManager(app)

celery_app = celery_init_app(app)

from tasks import send_deadline_reminder, send_instructor_report
def setup_periodic_tasks(sender, **kwargs):

    sender.add_periodic_task(
        crontab(hour=17, minute=30),

        send_deadline_reminder.s(),
    )

    sender.add_periodic_task(
        crontab(hour=17, minute=32),
        send_instructor_report.s(),
    )

celery_app.on_after_configure.connect(setup_periodic_tasks)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

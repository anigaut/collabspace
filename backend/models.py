from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String())
    email = db.Column(db.String(), nullable=False, unique=True)
    password_hash = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), nullable=False)
    github_repo = db.Column(db.String(), nullable=True)  # only for students
    
    # Relationships
    messages_sent = db.relationship('Messages', foreign_keys='Messages.sender_id', backref='sender', lazy=True)
    messages_received = db.relationship('Messages', foreign_keys='Messages.receiver_id', backref='receiver', lazy=True)


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False)


class Conversations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    last_message = db.Column(db.Text, nullable=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

##########################################################################

class Milestones(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    date_issued = db.Column(db.Date(), nullable=False)
    deadline = db.Column(db.Date(), nullable=False)
    submissions = db.relationship("MilestoneSubmissions")


class MilestoneSubmissions(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    milestone_id = db.Column(
        db.Integer(), db.ForeignKey("milestones.id"), nullable=False
    )
    student_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)
    github_branch_link = db.Column(db.String(), nullable=False)  # This is a GitHub link
    marks = db.Column(db.Integer(), nullable=True)
    instructor_feedback = db.Column(
        db.String(), nullable=True, default="No feedback required"
    )
    plagiarism_score = db.Column(db.Float(), nullable=True)  # Store plagiarism score
    plagiarism_status = db.Column(db.String(), nullable=True)


# Other models here...


# class InstructorFeedback(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     instructor_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
#     student_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
#     milestone_id = db.Column(db.Integer(), db.ForeignKey('milestones.id'), nullable=False)
#     submission_id = db.Column(db.Integer(), db.ForeignKey('MilestoneSubmissions.id'), nullable=False)
#     feedback = db.Column(db.String(), nullable=False)


class StudentDoubts(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    student_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    doubt = db.Column(db.String(), nullable=False)
    responding_TA_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    response = db.Column(db.String(), nullable=False)


class ChatbotInteractions(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    query = db.Column(db.String(), nullable=False)
    response = db.Column(db.String(), nullable=False)

class MentorshipSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    ta_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  
    session_date = db.Column(db.DateTime, nullable=False)
    session_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(50), default="pending") 
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = db.relationship('Users', foreign_keys=[student_id])
    ta = db.relationship('Users', foreign_keys=[ta_id])


class VivaSlots(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Nullable for unbooked slots
    ta_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    slot_date = db.Column(db.DateTime, nullable=False)
    slot_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(50), default="available")  # available, booked
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = db.relationship('Users', foreign_keys=[student_id])
    ta = db.relationship('Users', foreign_keys=[ta_id])

# Requested by Raj
class ProjectData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(), nullable=False)
    enrollment_term = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

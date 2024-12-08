from flask import Blueprint, request, jsonify
from models import *
from routes.authentication import *
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt  # type: ignore

instructor = Blueprint("instructor", __name__)


@instructor.route("/student_progress/<int:student_id>", methods=["GET"])
def get_student_progress(student_id):
    """
    Fetch student's project progress for an instructor
    """
    try:
        # Check if student exists
        student = Users.query.filter_by(id=student_id, role="student").first()
        if not student:
            return jsonify({"error": "Student not found"}), 404

        # Fetch submissions for the student
        submissions = MilestoneSubmissions.query.filter_by(student_id=student_id).all()
        if not submissions:
            # No submissions found, send specific message
            return jsonify({
                "message": "No submissions yet"
            }), 200

        progress = []
        for submission in submissions:
            milestone = Milestones.query.get(submission.milestone_id)
            progress.append({
                "milestone_title": milestone.title,
                "milestone_description": milestone.description,
                "date_issued": milestone.date_issued.strftime("%Y-%m-%d"),
                "deadline": milestone.deadline.strftime("%Y-%m-%d"),
                "submission_github_link": submission.github_branch_link,
                "marks": submission.marks,
                "instructor_feedback": submission.instructor_feedback,
                "plagiarism_score": submission.plagiarism_score,
                "plagiarism_status": submission.plagiarism_status,
            })

        return jsonify({
            "student_id": student.id,
            "student_name": f"{student.first_name} {student.last_name}",
            "github_repo": student.github_repo,
            "progress": progress
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@instructor.route("/students", methods=["GET"])
# @jwt_required()  
def get_students():
    try:
        # Fetch all users with the role "student"
        students = Users.query.filter_by(role="student").all()
        students_data = [
            {
                "id": student.id,
                "first_name": student.first_name,
                "last_name": student.last_name,
                "email": student.email,
            }
            for student in students
        ]
        return jsonify({"students": students_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    


def validate_milestone_input(data):
    errors = []
    if not data.get("title"):
        errors.append("Title is required.")
    if not data.get("description"):
        errors.append("Description is required.")
    if not data.get("date_issued"):
        errors.append("Issue date is required.")
    if not data.get("deadline"):
        errors.append("Deadline is required.")
    return errors


# @instructor.route('/milestones/comments', methods=['POST'])
# def add_milestone_comment():
#     data = request.json
#     new_feedback = InstructorFeedback(
#         milestone_id=data['milestone_id'],
#         student_id=data['student_id'],
#         feedback=data['comment'],
#         created_at=datetime.utcnow()
#     )
#     db.session.add(new_feedback)
#     db.session.commit()
#     return jsonify({'message': 'Comment added successfully'}), 201


@instructor.route("/create_milestone", methods=["POST"])
# @jwt_required()
# @role_required("instructor")
def create_milestone():
    data = request.get_json()
    errors = validate_milestone_input(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        if not data.get("title") or not data["title"].strip():
            return jsonify({"error": "Milestone title cannot be empty"}), 400
        
        existing_milestone = Milestones.query.filter_by(title=data["title"]).first()
        if existing_milestone:
            return jsonify({"error": "A milestone with this title already exists"}), 400
        
        date_issued = datetime.strptime(data["date_issued"], "%Y-%m-%d")
        deadline = datetime.strptime(data["deadline"], "%Y-%m-%d")
        
        # Validate that date_issued is not in the past
        today = datetime.now().date()
        if date_issued.date() < today:
            return jsonify({"error": "date_issued cannot be yesterday or any earlier day"}), 400
        
        # Validate that date_issued is before the deadline
        if date_issued >= deadline:
            return jsonify({"error": "date_issued must be earlier than deadline"}), 400

        # Create and save the milestone
        new_milestone = Milestones(
            title=data["title"],
            description=data["description"],
            date_issued=date_issued,
            deadline=deadline
        )
        db.session.add(new_milestone)
        db.session.commit()
        return jsonify({"message": "Milestone created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# @instructor.route("/milestones", methods=["GET"])
# # @role_required("instructor") 
# def get_all_milestones():
#     try:
#         milestones = Milestones.query.all()
#         milestones_data = [
#             {
#                 "id": milestone.id,
#                 "title": milestone.title,
#                 "description": milestone.description,
#                 "date_issued": milestone.date_issued.strftime("%Y-%m-%d"),
#                 "deadline": milestone.deadline.strftime("%Y-%m-%d")
#             }
#             for milestone in milestones
#         ]
#         return jsonify({"milestones": milestones_data}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


@instructor.route("/update_milestone/<int:milestone_id>", methods=["POST"])
# @jwt_required()
# @role_required("instructor") 
def update_milestone(milestone_id):
    milestone = Milestones.query.get(milestone_id)
    if milestone is None:
        return jsonify({"error": "Milestone not found"}), 404

    data = request.get_json()
    
    # Validate title
    if "title" in data:
        if not data["title"].strip():
            return jsonify({"error": "Milestone title cannot be empty"}), 400
        
        # Check if milestone title already exists and it's not the same milestone being updated
        existing_milestone = Milestones.query.filter_by(title=data["title"]).first()
        if existing_milestone and existing_milestone.id != milestone.id:
            return jsonify({"error": "A milestone with this title already exists"}), 400

        milestone.title = data["title"].strip()

    # Update description
    if "description" in data:
        milestone.description = data["description"].strip()

    # Parse and validate dates
    if "date_issued" in data:
        date_issued = datetime.strptime(data["date_issued"], "%Y-%m-%d")
        today = datetime.now().date()
        if date_issued.date() < today:
            return jsonify({"error": "date_issued cannot be yesterday or any earlier day"}), 400
        milestone.date_issued = date_issued

    if "deadline" in data:
        deadline = datetime.strptime(data["deadline"], "%Y-%m-%d")
        milestone.deadline = deadline

    # Ensure that date_issued is before deadline (if both are set)
    if milestone.date_issued and milestone.deadline:
        if milestone.date_issued >= milestone.deadline:
            return jsonify({"error": "date_issued must be earlier than deadline"}), 400

    try:
        db.session.commit()
        return jsonify({"message": "Milestone updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@instructor.route("/delete_milestone/<int:milestone_id>", methods=["DELETE"])
# @jwt_required()
# @role_required("instructor")
def delete_milestone(milestone_id):
    milestone = Milestones.query.get(milestone_id)
    if milestone is None:
        return jsonify({"error": "Milestone not found"}), 404

    try:
        db.session.delete(milestone)
        db.session.commit()
        return jsonify({"message": "Milestone deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# pending
@instructor.route("/get_submission/<int:milestone_id>", methods=["GET"])
def get_all_submissions(milestone_id):
    """
    Fetches all submissions made by students for a particular milestone
    """
    submissions = MilestoneSubmissions.query.filter_by(milestone_id=milestone_id).all()

    if not submissions:
        return jsonify({
            "message": "No submissions were made yet"
        }), 400

    submissions_data = [
        {
            "id": submission.id,
            "milestone_id": submission.milestone_id,
            "student_id": submission.student_id,
            "github_branch_link": submission.github_branch_link,
            "marks": submission.marks,
            "instructor_feedback": submission.instructor_feedback,
            "plagiarism_status": submission.plagiarism_status,
            "plagiarism_score": submission.plagiarism_score
        }
        for submission in submissions
    ]

    return jsonify({
        "submissions_data": submissions_data
    }), 200


@instructor.route("/add_feedback/<int:milestone_submission_id>", methods=["POST"])
# @role_required("instructor")
def add_feedback(milestone_submission_id):
    """
    Add instructor feedback for a particular milestone submission
    """
    submission = MilestoneSubmissions.query.get(milestone_submission_id)
    if not submission:
        return jsonify({
            "message": "Submission doesn't exist"
        }), 404
    data = request.get_json()
    feedback = data.get("feedback")
    marks = data.get("marks")

    submission.instructor_feedback = feedback
    submission.marks = marks

    db.session.commit()

    return jsonify({
        "message": "Added feedback successfully"
    }), 200


@instructor.route("/edit_feedback/<int:milestone_submission_id>", methods=["POST"])
# @role_required("instructor")
def edit_feedback(milestone_submission_id):
    """
    Feature to edit feedback given for a particular milestone submission
    """
    data = request.get_json()
    submission = MilestoneSubmissions.query.get(milestone_submission_id)
    if not submission:
        return jsonify({
            "message": "Submission doesn't exist"
        }), 404

    if data.get("feedback"):
        submission.feedback = data.get("feedback")
    if data.get("marks"):
        submission.marks = data.get("marks")

    db.session.commit()

    return jsonify({
        "message": "Edited feedback successfully"
    }), 200

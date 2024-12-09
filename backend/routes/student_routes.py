from flask import Blueprint, request, jsonify
from sqlalchemy import true
from models import *
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt  # type: ignore

from routes.authentication import *

student = Blueprint("student", __name__)


@student.route('/api/projects/status/<int:student_id>', methods=['GET'])
def get_project_status(student_id):
    submissions = MilestoneSubmissions.query.filter_by(student_id=student_id).all()
    status_data = []

    for submission in submissions:
        milestone = Milestones.query.get(submission.milestone_id)
        status_data.append({
            'milestone_id': milestone.id,
            'title': milestone.title,
            'completion_status': 'completed' if submission.GitHub_repo_branch_link else 'pending',
            'deadline': milestone.deadline.isoformat()
        })

    return jsonify(milestone_progress=status_data)


@student.route("/link_github_repo", methods=["POST"])
# @jwt_required()
# @role_required("student")
def link_github_repo():
    # student_id = get_jwt_identity()
    data = request.get_json()
    student_id = data["student_id"]
    github_repo_link = data.get("github_repo_link")

    if not github_repo_link:
        return jsonify({"error": "GitHub repository link is required"}), 400

    student = Users.query.get(student_id)
    if student is None:
        return jsonify({"error": "Student not found"}), 404

    student.github_repo = github_repo_link
    try:
        db.session.commit()
        return jsonify({"message": "GitHub repository linked successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@student.route("/update_github_repo", methods=["PUT"])
# @jwt_required()
# @role_required("student")
def update_github_repo():
    # student_id = get_jwt_identity()
    data = request.get_json()
    student_id = data["student_id"]

    new_github_repo_link = data.get("github_repo_link")

    if not new_github_repo_link:
        return jsonify({"error": "New GitHub repository link is required"}), 400

    student = Users.query.get(student_id)
    if student is None:
        return jsonify({"error": "Student not found"}), 404

    student.github_repo = new_github_repo_link
    try:
        db.session.commit()
        return jsonify({"message": "GitHub repository updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@student.route("/delete_github_repo", methods=["POST"])
# @jwt_required()
# @role_required("student")
def delete_github_repo():
    # student_id = get_jwt_identity()

    data = request.get_json()
    student_id = data["student_id"]
    student = Users.query.get(student_id)

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    student.github_repo = ""
    try:
        db.session.commit()
        return jsonify({"message": "GitHub repository deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@student.route("/get_github_repo", methods=["GET"])
# @jwt_required()
# @role_required("student")
def get_github_repo():
    # student_id = get_jwt_identity()
    data = request.get_json()
    student_id = data["student_id"]
    student = Users.query.get(student_id)

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"github_repo_link": student.github_repo}), 200


# completion status -> if any submission made before deadline
@student.route("/milestones", methods=["GET"])
# @jwt_required()
# @role_required("student")
def get_all_milestones():
    try:
        milestones = Milestones.query.all()
        milestones_data = [
            {
                "id": milestone.id,
                "title": milestone.title,
                "description": milestone.description,
                "date_issued": milestone.date_issued.strftime("%Y-%m-%d"),
                "deadline": milestone.deadline.strftime("%Y-%m-%d")
            }
            for milestone in milestones
        ]
        return jsonify({"milestones": milestones_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@student.route('/book_viva_slot/<int:slot_id>', methods=['POST'])
# @jwt_required()  # Assuming JWT authentication to identify the student
def book_viva_slot(slot_id):
    try:
        # Get the current student ID from the JWT
        student_id = 1
        # student_id = get_jwt_identity()

        # Find the slot by ID
        viva_slot = VivaSlots.query.get(slot_id)

        if not viva_slot:
            return jsonify({"error": "Viva slot not found."}), 404
        
        if viva_slot.status != "available":
            return jsonify({"error": "This slot is already booked."}), 400
        
        # Update slot details
        viva_slot.student_id = student_id
        viva_slot.status = "booked"
        viva_slot.updated_at = datetime.utcnow()

        db.session.commit()

        return jsonify({"message": "Viva slot booked successfully."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@student.route('/book_mentorship_session/<int:session_id>', methods=['POST'])
def book_mentorship_session(session_id):
    try:
        student_id = 1  
        mentorship_session = MentorshipSession.query.get(session_id)

        if not mentorship_session:
            return jsonify({"error": "Mentorship session not found."}), 404
        
        if mentorship_session.status != "pending":
            return jsonify({"error": "This mentorship session is not available for booking."}), 400
        
        if mentorship_session.student_id and mentorship_session.student_id != student_id:
            return jsonify({"error": "You cannot book a session initiated by another student."}), 403

        mentorship_session.student_id = student_id
        mentorship_session.status = "booked"
        mentorship_session.updated_at = datetime.utcnow()

        db.session.commit()

        return jsonify({"message": "Mentorship session booked successfully."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@student.route("/submit_milestone/<int:milestone_id>/<int:student_id>", methods=["POST"])
def submit_milestone(milestone_id, student_id):
    """
    Allowed only once
    """
    if not Milestones.query.get(milestone_id):
        return jsonify({
            "message": "This milestone doesn't exist"
        }), 400

    data = request.get_json()
    branch_link = data.get("github_branch_link")

    new_submission = MilestoneSubmissions(
        milestone_id=milestone_id,
        # student_id=get_jwt_identity(),
        student_id=student_id,
        github_branch_link=branch_link
    )

    db.session.add(new_submission)
    db.session.commit()

    return jsonify({
        "message": "Submitted Successfully"
    }), 200


@student.route("/get_submission/<int:milestone_id>/<int:student_id>", methods=["GET"])
# @role_required("student")
def get_submission(milestone_id, student_id):
    # student_id = request.get_json().get("student_id")
    # student_id = 1
    submission = MilestoneSubmissions.query.filter_by(student_id=student_id, milestone_id=milestone_id).first()
    if not submission:
        return jsonify({
            "message": "No submission made yet"
        }), 400

    submission_details = {
        "id": submission.id,
        "student_id": submission.student_id,
        "milestone_id": submission.milestone_id,
        "github_branch_link": submission.github_branch_link,
        "instructor_feedback": submission.instructor_feedback,
        "marks": submission.marks
    }

    return jsonify({
        "submission_details": submission_details
    }), 200

from flask import Blueprint, request, jsonify
from models import *
from routes.authentication import *
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt  # type: ignore

instructor = Blueprint("instructor", __name__)


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


@instructor.route('/milestones/comments', methods=['POST'])
def add_milestone_comment():
    data = request.json
    new_feedback = InstructorFeedback(
        milestone_id=data['milestone_id'],
        student_id=data['student_id'],
        feedback=data['comment'],
        created_at=datetime.utcnow()
    )
    db.session.add(new_feedback)
    db.session.commit()
    return jsonify({'message': 'Comment added successfully'}), 201


@instructor.route("/create_milestone", methods=["POST"])
# @jwt_required()
# @role_required("instructor")
def create_milestone():
    data = request.get_json()
    errors = validate_milestone_input(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        new_milestone = Milestones(
            title=data["title"],
            description=data["description"],
            date_issued=datetime.strptime(data["date_issued"], "%Y-%m-%d"),
            deadline=datetime.strptime(data["deadline"], "%Y-%m-%d")
        )
        db.session.add(new_milestone)
        db.session.commit()
        return jsonify({"message": "Milestone created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@instructor.route("/milestones", methods=["GET"])
# @role_required("instructor") 
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


@instructor.route("/update_milestone/<int:milestone_id>", methods=["PUT"])
# @jwt_required()
# @role_required("instructor") 
def update_milestone(milestone_id):
    milestone = Milestones.query.get(milestone_id)
    if milestone is None:
        return jsonify({"error": "Milestone not found"}), 404

    data = request.get_json()
    milestone.title = data.get("title", milestone.title)
    milestone.description = data.get("description", milestone.description)
    if "date_issued" in data:
        milestone.date_issued = datetime.strptime(data["date_issued"], "%Y-%m-%d")
    if "deadline" in data:
        milestone.deadline = datetime.strptime(data["deadline"], "%Y-%m-%d")

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


@instructor.route("/get_submission/<int:milestone_id>", methods=["POST"])
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
            "instructor_feedback": submission.instructor_feedback
        }
        for submission in submissions
    ]

    return jsonify({
        "submissions_data": submissions_data
    }), 200


@instructor.route("/add_feedback/<int:milestone_submission_id>", methods=["POST"])
@role_required("instructor")
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


@instructor.route("/edit_feedback/<int:milestone_submission_id>", methods=["PUT"])
@role_required("instructor")
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

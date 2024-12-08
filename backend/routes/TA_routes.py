from flask import Blueprint, request, jsonify
from models import *
from datetime import datetime
import requests
from urllib.parse import urlparse
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from Levenshtein import distance as levenshtein_distance
from models import Users, MilestoneSubmissions
import requests
from dotenv import load_dotenv
import os

load_dotenv()  
 
from routes.authentication import *
ta = Blueprint("ta", __name__)

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env


@ta.route('/api/doubts', methods=['GET'])
def get_doubts():
    doubts = StudentDoubts.query.all()
    doubt_list = []
    for doubt in doubts:
        student = Users.query.get(doubt.student_id)
        doubt_list.append({
            'doubt_id': doubt.id,
            'student_name': f"{student.first_name} {student.last_name}",
            'doubt': doubt.doubt,
            'status': 'answered' if doubt.response else 'pending',
            'created_at': doubt.created_at.isoformat()
        })
    return jsonify(doubt_list)


@ta.route('/api/chat/ta', methods=['GET'])
def get_chat_history():
    data = request.get_json()
    student_id = data["student_id"]
    ta_id = data['ta_id']

    # student_id = request.args.get('student_id')
    # ta_id = request.args.get('ta_id')

    # chat_history = ChatbotInteractions.query.filter(
    #     (ChatbotInteractions.user_id == student_id) | (ChatbotInteractions.user_id == ta_id)
    # ).order_by(ChatbotInteractions.created_at).all()

    # messages = [
    #     {'query': interaction.query, 'response': interaction.response, 'timestamp': interaction.created_at.isoformat()}
    #     for interaction in chat_history
    # ]
    # if messages:
    #     return jsonify({'messages': messages})
        
    return jsonify({'message': "No chats found"})


@ta.route('/api/chat/ta', methods=['POST'])
def send_message():
    # data = request.json
    # new_message = ChatbotInteractions(
    #     user_id=data['ta_id'],
    #     query=data['message'],
    #     response=data['response'],
    #     created_at=datetime.utcnow()
    # )
    # db.session.add(new_message)
    # db.session.commit()
    return jsonify({'message': 'Message sent successfully'}), 201

@ta.route('/api/viva_slots', methods=['POST'])
def create_viva_slot():
    data = request.get_json()
    try:
        ta_id = data.get('ta_id')
        slot_date = data.get('slot_date')
        slot_time = data.get('slot_time')

        if not ta_id or not slot_date or not slot_time:
            return jsonify({"error": "Missing required fields (ta_id, slot_date, slot_time)."}), 400

        slot = VivaSlots(
            ta_id=ta_id,
            slot_date=datetime.strptime(slot_date, '%Y-%m-%d'),
            slot_time=datetime.strptime(slot_time, '%H:%M:%S').time(),
        )
        db.session.add(slot)
        db.session.commit()
        return jsonify({"message": "Viva slot created successfully."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@ta.route('/api/viva_slots', methods=['GET'])
def fetch_viva_slots():
    try:
        slots = VivaSlots.query.all()
        result = [
            {
                "id": slot.id,
                "ta_id": slot.ta_id,
                "student_id": slot.student_id,
                "slot_date": slot.slot_date.strftime('%Y-%m-%d'),
                "slot_time": slot.slot_time.strftime('%H:%M:%S'),
                "status": slot.status,
            }
            for slot in slots
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ta.route('/api/viva_slots/<int:slot_id>', methods=['POST'])
def update_viva_slot(slot_id):
    data = request.get_json()
    try:
        slot = VivaSlots.query.get(slot_id)
        if not slot:
            return jsonify({"error": "Viva slot not found."}), 404

        slot.slot_date = datetime.strptime(data.get('slot_date', slot.slot_date.strftime('%Y-%m-%d')), '%Y-%m-%d')
        slot.slot_time = datetime.strptime(data.get('slot_time', slot.slot_time.strftime('%H:%M:%S')), '%H:%M:%S').time()
        slot.status = data.get('status', slot.status)
        db.session.commit()
        return jsonify({"message": "Viva slot updated successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@ta.route('/api/viva_slots/<int:slot_id>', methods=['DELETE'])
def delete_viva_slot(slot_id):
    try:
        slot = VivaSlots.query.get(slot_id)
        if not slot:
            return jsonify({"error": "Viva slot not found."}), 404

        db.session.delete(slot)
        db.session.commit()
        return jsonify({"message": "Viva slot deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400           

# @ta.route('/mentorship_session/view', methods=['GET'])
# def view_mentorship_requests():
#     requests = MentorshipSessionRequests.query.filter_by(status="pending").all()
#     result = [{
#         "id": req.id,
#         "student_id": req.student_id,
#         "requested_date": req.requested_date.strftime("%Y-%m-%d"),
#         "requested_time": req.requested_time.strftime("%H:%M"),
#         "status": req.status
#     } for req in requests]
#     return jsonify({"requests": result}), 200

# @ta.route('/mentorship_session/accept/<int:request_id>', methods=['PUT'])
# def accept_mentorship_request(request_id):
#     session_request = MentorshipSessionRequests.query.get(request_id)

#     if not session_request:
#         return jsonify({"error": "Request not found"}), 404

#     session_request.status = "accepted"
#     db.session.commit()
#     return jsonify({"message": "Mentorship session accepted."}), 200

# @ta.route('/mentorship_session/delete/<int:request_id>', methods=['DELETE'])
# def delete_mentorship_request(request_id):
#     session_request = MentorshipSessionRequests.query.get(request_id)

#     if not session_request:
#         return jsonify({"error": "Request not found"}), 404

#     session_request.status = "deleted"
#     db.session.commit()
#     return jsonify({"message": "Mentorship session deleted."}), 200

##############plag##################################################################################


import requests
from urllib.parse import urlparse
import os

supported_extensions = {".py", ".java", ".c", ".cpp", ".js", ".ts", ".html", ".css",".txt",""}


def has_supported_extension(filename):
    _, ext = os.path.splitext(filename)
    return ext.lower() in supported_extensions


def fetch_github_code(repo_url):
    try:
        # Extract the username and repo name from the GitHub URL
        parsed_url = urlparse(repo_url)
        path_parts = parsed_url.path.strip("/").split("/")
        if len(path_parts) < 2:
            print("Invalid GitHub URL format.")
            return None  # Invalid URL format
        user, repo = path_parts[:2]

        # GitHub API to fetch the content of the repository files
        api_url = f"https://api.github.com/repos/{user}/{repo}/contents"
        headers = {
            "Accept": "application/vnd.github.v3.raw",
            "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
        }

        # Check if the token is loaded
        if not headers["Authorization"]:
            print(
                "GitHub token is not set. Please set the GITHUB_TOKEN environment variable."
            )
            return None

        response = requests.get(api_url, headers=headers)
        print(f"GET {api_url} - Status Code: {response.status_code}")

        if response.status_code == 200:
            contents = response.json()
            files_content = []
            total_files = 0
            supported_files = 0

            def fetch_contents(items):
                nonlocal total_files, supported_files
                for item in items:
                    total_files += 1
                    if item["type"] == "file":
                        print(f"Found file: {item['path']}")
                        if has_supported_extension(item["name"]):
                            supported_files += 1
                            print(f"Fetching supported file: {item['path']}")
                            file_response = requests.get(
                                item["download_url"], headers=headers
                            )
                            print(
                                f"GET {item['download_url']} - Status Code: {file_response.status_code}"
                            )
                            if file_response.status_code == 200:
                                files_content.append(file_response.text)
                            else:
                                print(
                                    f"Failed to fetch file {item['path']}: {file_response.status_code}"
                                )
                        else:
                            print(f"Ignored unsupported file: {item['path']}")
                    elif item["type"] == "dir":
                        print(f"Entering directory: {item['path']}")
                        subdir_api_url = item["url"]
                        subdir_response = requests.get(subdir_api_url, headers=headers)
                        print(
                            f"GET {subdir_api_url} - Status Code: {subdir_response.status_code}"
                        )
                        if subdir_response.status_code == 200:
                            subdir_contents = subdir_response.json()
                            fetch_contents(subdir_contents)  # Recursive call
                        else:
                            print(
                                f"Failed to fetch subdirectory {item['path']}: {subdir_response.status_code}"
                            )

            fetch_contents(contents)
            combined_code = "\n".join(files_content)
            print(f"Total files found: {total_files}")
            print(f"Supported files fetched: {supported_files}")
            print(f"Fetched total code length: {len(combined_code)} characters.")
            return combined_code
        elif response.status_code == 403:
            # Possibly rate limited or forbidden
            error_message = response.json().get("message", "Forbidden")
            print(
                f"Failed to fetch repo contents: {response.status_code} - {error_message}"
            )
            return None
        else:
            print(f"Failed to fetch repo contents: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching GitHub code: {e}")
        return None


# Levenshtein Distance-based Similarity
def levenshtein_similarity(str1, str2):
    # Normalize by string length for a percentage similarity
    lev_distance = levenshtein_distance(str1, str2)
    max_len = max(len(str1), len(str2))
    if max_len == 0:
        return 100  # Both strings are empty
    return (1 - lev_distance / max_len) * 100


# Cosine Similarity-based approach
def cosine_similarity_score(str1, str2):
    # Use CountVectorizer to convert text to a matrix of token counts
    vectorizer = CountVectorizer().fit_transform([str1, str2])
    vectors = vectorizer.toarray()
    numerator = np.dot(vectors[0], vectors[1])
    denominator = np.linalg.norm(vectors[0]) * np.linalg.norm(vectors[1])
    if denominator == 0:
        return 0
    cosine_score = numerator / denominator
    return cosine_score * 100  # Return as percentage


def compare_code(code1, code2):
    """
    Compare two pieces of code for similarity using Levenshtein distance and Cosine similarity.
    Returns a similarity score between 0 and 100.
    """
    if not code1 or not code2:
        print("One of the code snippets is empty.")
        return 0  # If either of the code snippets is empty, return 0% similarity

    # Compute similarity using both Levenshtein and Cosine Similarity
    lev_score = levenshtein_similarity(code1, code2)
    print(f"Levenshtein similarity: {lev_score}")
    cosine_score = cosine_similarity_score(code1, code2)
    print(f"Cosine similarity: {cosine_score}")

    # Combine the scores (weighted equally)
    final_score = (lev_score * 0.5) + (cosine_score * 0.5)
    print(f"Final similarity score: {final_score}")

    return final_score


@ta.route("/get_students", methods=["GET"])
def get_students():
    print("Fetching students from the database...")
    students = Users.query.filter_by(role="student").all()
    if not students:
        print("No students found in the database.")
    else:
        print(f"Found {len(students)} students.")
    student_list = [
        {
            "id": student.id,
            "first_name": student.first_name,
            "last_name": student.last_name,
        }
        for student in students
    ]
    return jsonify(student_list), 200


@ta.route("/check_plagiarism", methods=["POST"])
def check_plagiarism():
    print("Received plagiarism check request")
    data = request.get_json()
    print(f"Request data: {data}")

    if not data or "github_repo_link" not in data or "student_id" not in data:
        print("Missing required fields")
        return (
            jsonify({"error": "GitHub repository link and student ID are required"}),
            400,
        )

    new_repo_url = data["github_repo_link"]
    student_id = data["student_id"]

    print(f"Fetching code for repository: {new_repo_url}")
    new_repo_code = fetch_github_code(new_repo_url)

    if new_repo_code is None or new_repo_code.strip() == "":
        print("Failed to fetch new repository code or code is empty")
        return (
            jsonify(
                {"error": "Unable to fetch repository data or repository is empty."}
            ),
            500,
        )

    print(f"New repository code length: {len(new_repo_code)} characters")

    # Fetch all other student repository links from the database
    print(f"Fetching submissions excluding student ID: {student_id}")
    other_submissions = MilestoneSubmissions.query.filter(
        MilestoneSubmissions.student_id != student_id
    ).all()
    print(f"Found {len(other_submissions)} other submissions")

    plagiarism_results = []
    total_score = 0
    comparison_count = 0

    for submission in other_submissions:
        print(
            f"Processing submission ID: {submission.id} with repo link: {submission.github_branch_link}"
        )

        # **Check if the other submission has the same repo link**
        if submission.github_branch_link == new_repo_url:
            print("Identical repository found. Assigning 100% similarity.")
            score = 100.0
            status = "fail"
        else:
            existing_repo_code = fetch_github_code(submission.github_branch_link)
            if existing_repo_code is None or existing_repo_code.strip() == "":
                print("Failed to fetch existing repository code or code is empty")
                continue  # Skip if no valid code is found for the repository

            print(
                f"Existing repository code length: {len(existing_repo_code)} characters"
            )

            # Compare the new submission with the existing submission
            print("Comparing code...")
            score = compare_code(new_repo_code, existing_repo_code)
            print(f"Similarity score: {score}")
            status = "fail" if score >= 30 else "pass"

        total_score += score
        comparison_count += 1

        student = Users.query.get(submission.student_id)
        student_full_name = (
            f"{student.first_name} {student.last_name}" if student else "Unknown"
        )

        plagiarism_results.append(
            {
                "student_name": student_full_name,
                "repo_link": submission.github_branch_link,
                "score": score,
                "status": status,
            }
        )

        # **Update the submission with the plagiarism score and status**
        submission.plagiarism_score = score
        submission.plagiarism_status = status

    # Calculate overall score
    overall_score = (total_score / comparison_count) if comparison_count > 0 else 0
    print(f"Overall plagiarism score: {overall_score}")

    # **Commit the changes to the database**
    try:
        db.session.commit()
        print("Plagiarism scores updated in the database.")
    except Exception as e:
        db.session.rollback()
        print(f"Error saving plagiarism scores to the database: {e}")
        return (
            jsonify({"error": "Failed to save plagiarism scores to the database."}),
            500,
        )

    return (
        jsonify(
            {"overall_score": overall_score, "plagiarism_results": plagiarism_results}
        ),
        200,
    )

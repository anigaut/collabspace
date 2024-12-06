from datetime import timedelta
from functools import wraps
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, create_access_token, unset_jwt_cookies, \
    decode_token, get_jwt, verify_jwt_in_request  # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash

from models import *

auth = Blueprint("auth", __name__)


def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"] == role:
                return fn(*args, **kwargs)
            else:
                return jsonify({"message": "You Cannot Access This Page"}), 403

        return decorator

    return wrapper


@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    password = data["password"]
    password_hash = generate_password_hash(data["password"])
    role = data["role"]

    if Users.query.filter_by(email=email).first():
        return jsonify({"message": "A user with this email already exists. Please use a different one"}), 400

    new_user = Users(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=password_hash,
        role=role
    )

    # User details - to be stored in local storage
    user_info = {
        "user_id": new_user.id,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email,
        "role": new_user.role
    }

    access_token = create_access_token(identity=new_user.id,
                                       expires_delta=timedelta(days=10),
                                       additional_claims={"role": role})

    db.session.add(new_user)
    db.session.commit()

    # Will be sent back to frontend - remember to add access token and user info in local storage
    return jsonify({"message": "Registered Successfully",
                    "access_token": access_token,
                    "user_info": user_info}), 200


@auth.route("/login", methods=["GET", "POST"])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    user = Users.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": f"A {role} with this email does not exist"}), 400

    if not check_password_hash(user.password_hash, password):
        return jsonify({"message": "Incorrect Password"}), 400

    access_token = create_access_token(identity=user.id,
                                       expires_delta=timedelta(days=10),
                                       additional_claims={"role": user.role})

    user_info = {
        "user_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role": user.role
    }

    return jsonify({
        "message": "Logged in Successfully",
        "access_token": access_token,
        "admin_info": user_info
    }), 200


@auth.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"message": "Logged out Successfully"})
    unset_jwt_cookies(response)
    return response, 200


# Only for testing, remove comment in a separate branch if required.
# @auth.route("/delete_user/<int:user_id>", methods=["DELETE"])
# def delete_user(user_id):
#     user = Users.query.get(user_id)
#     if not user:
#         return jsonify({"msg": "This User Does Not Exist"}), 400
#
#     db.session.delete(user)
#     db.session.commit()
#
#     return jsonify({
#         "message": "Delete user successfully"
#     }), 200

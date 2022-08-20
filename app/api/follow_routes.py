from flask import request
from flask_login import current_user, login_required
from flask_wtf.csrf import validate_csrf
from app.models import User, db
from .user_routes import user_routes

@user_routes.route("/<int:id>/follow")
@login_required
def make_follow_request(id):
    followed = User.query.get(id)
    follower = User.query.get(current_user.id)
    followed_users = [user.id for user in follower.following]
    requested_follows = [user.id for user in follower.requests]
    if not followed:
        return { "errors": f"User {id} does not exist"}, 400
    if followed.id in followed_users:
        return { "errors": f"User {current_user.id} is already" +
                            f" following user {id}" }
    if followed.id in requested_follows:
        return { "errors": f"User {current_user.id} has already" +
                            f" sent a follow request to user {id}" }, 400
    if current_user.id == id:
        return { "errors": " You can't follow yourself, silly" }, 400
    csrf_token = request.cookies["csrf_token"]
    try:
        validate_csrf(csrf_token)
        followed.requested.append(follower)
        db.session.commit()
        return { "message": "Follow request sent!" }, 201
    except Exception as e:
        return { "errors": str(e) }

@user_routes.route("/<int:id>/rescind-request", methods=["DELETE"])
@login_required
def rescind_follow_request(id):
    followed = User.query.get(id)
    follower = User.query.get(current_user.id)
    followed_users = [user.id for user in follower.following]
    requested_follows = [user.id for user in follower.requests]
    if not followed:
        return { "errors": f"User {id} does not exist" }
    if followed.id not in requested_follows:
        return { "errors": f"User {current_user.id} does not have a" +
                            f" pending follow request with user {id}" }
    if followed.id in followed_users:
        return {
            "errors": f"User {current_user.id} is currently following" +
                        f" user {id}"
        }
    if current_user.id == id:
        return { "errors": "You can't rescind a follow request to yourself, silly!" }
    csrf_token = request.cookies["csrf_token"]
    try:
        validate_csrf(csrf_token)
        followed.requested.remove(follower)
        db.session.commit()
        return { "message": 
                    "Request successfully rescinded!"
                }
    except Exception as e:
        return { "errors": str(e) }

@user_routes.route("/<int:id>/confirm-follow", methods=["POST"])
@login_required
def confirm_follow(id):
    follower = User.query.get(id)
    followed = User.query.get(current_user.id)
    requested_follows = [user.id for user in follower.requests]
    followed_users = [user.id for user in follower.following]
    if not followed:
        return { "errors": f"User {id} does not exist" }
    if followed.id not in requested_follows:
        return { "errors": f"User {id} does not have a pending follow" +
                           f" request with user {current_user.id}" }
    if followed.id in followed_users:
        return {
            "errors": f"User {current_user.id} is currently following" +
                        f" user {id}"
        }
    if current_user.id == id:
        return { "errors": "You can't rescind a follow request to yourself, silly!" } 
    csrf_token = request.cookies["csrf_token"]
    try:
        validate_csrf(csrf_token)
        # this part needs to be finished
        pass
    except Exception as e:
        return { "errors": str(e) }
    followed.requested.remove(follower)
    followed.followers.append(follower)
    db.session.commit()
    return { "message": "Successfully added follower" }, 201
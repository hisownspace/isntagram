from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from app.forms import UpdateUser, DeleteUser
from flask_wtf.csrf import validate_csrf
from app.models import User, Image, db
from app.s3_helpers import allowed_file, get_unique_filename, remove_file_from_s3, upload_file_to_s3

user_routes = Blueprint('users', __name__)


@user_routes.route('/')
@login_required
def users():
    users = User.query.all()
    return {'users': [user.to_dict() for user in users]}


@user_routes.route('/<int:id>')
@login_required
def user(id):
    user = User.query.get(id)
    return user.to_dict()

@user_routes.route("/<int:id>/images")
def get_images(id):
    images = Image.query.filter_by(user_id = id)\
        .order_by(Image.created_at.desc()).all()
    return { "images": [image.to_dict() for image in images] }

@user_routes.route("/<int:id>", methods=["PUT"])
@login_required
def update_user(id):

    print("current_user", current_user)
    form = UpdateUser()

    print(form.data)
    if id != current_user.id:
        return { "error": "unauthorized resource" }
    
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        user = User.query.get(current_user.id)

        email = form.data["email"]
        image = form.data["image"]
        password = form.data["password"]
        username = form.data["username"]

        if email != "":
            user.email = email
        if image != None:
            if not allowed_file(image.filename):
                return { "errors": "file type not permitted" }
            image.filename = get_unique_filename(image.filename)
            upload = upload_file_to_s3(image)
            if "url" not in upload:
                return upload, 400
            url = upload["url"]
            image_id = user.image_url.rsplit('/')[-1]
            print("image_id================>", image_id)
            if image_id != "default-profile-pic.jpg":
                remove_file_from_s3(image_id)
            user.image_url = url
        if password != "":
            user.password = password
        if username != "":
            user.username = username

        db.session.commit()
        return { "user": user.to_dict() }

@user_routes.route("/<int:id>", methods=["DELETE"])
def delete_your_account(id):
    if id != current_user.id:
        return { "errors": "unauthorized resource" }
    form = DeleteUser()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        image_url = user.image_url
        image_key = image_url.rsplit("/")[-1]
        remove_file_from_s3(image_key)
        db.session.delete(user)
        db.session.commit()
        return { "message": "Delete successful!" }


@user_routes.route("/<int:id>/follow")
@login_required
def make_follow_request(id):
    followee = User.query.get(id)
    follower = User.query.get(current_user.id)
    followed_users = [user.id for user in follower.following]
    requested_follows = [user.id for user in follower.requests]
    if not followee:
        return { "errors": f"User {id} does not exist"}
    if followee.id in followed_users:
        return { "errors": f"User {current_user.id} is already" +
                            " following user {id}" }
    if followee.id in requested_follows:
        return { "errors": f"User {current_user.id} has already" +
                            " sent a follow request to user {id}" }
    csrf_token = request.cookies["csrf_token"]
    try:
        validate_csrf(csrf_token)
        followee.requested.append(follower)
        db.session.commit()
        return { "message": "Follow request sent!" }
    except Exception as e:
        return { "errors": str(e) }

@user_routes.route("/<int:id>/unfollow", methods=["DELETE"])
@login_required
def rescind_follow_request(id):
    followee = User.query.get(id)
    follower = User.query.get(current_user.id)
    followed_users = [user.id for user in follower.following]
    requested_follows = [user.id for user in follower.requests]
    if not followee:
        return { "errors": f"User {id} does not exist" }
    if followee.id not in requested_follows:
        return { "errors": f"User {current_user.id} does not have a" +
                            f" pending follow request with user {id}" }
    if followee.id in followed_users:
        return {
            "errors": f"User {current_user.id} is currently following" +
                        f" user {id}"
        }
    csrf_token = request.cookies["csrf_token"]
    try:
        validate_csrf(csrf_token)
        followee.requested.remove(follower)
        db.session.commit()
        return { "message": 
                    "Request successfully rescinded!"
                }
    except Exception as e:
        return { "errors": str(e) }
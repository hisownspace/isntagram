from flask import request, Blueprint
from flask_login import current_user, login_required
from app.forms.comment_form import DeleteComment
from app.models import Comment, db, Image, User
from app.api.image_routes import image_routes
from app.forms import CommentForm

comment_routes = Blueprint("comments", __name__)

@comment_routes.route("/<int:id>")
def get_comment(id):
    comment = Comment.query.get(id)
    return { "comment": comment.to_dict() }

@comment_routes.route("/<int:id>", methods=["PUT"])
@login_required
def update_comment(id):
    form = CommentForm()

    form["csrf_token"].data = request.cookies["csrf_token"]

    if form.validate_on_submit():
        comment = Comment.query.get(id)
        if comment.user_id != current_user.id:
            return { "error": "Unauthorized resource" }
        comment.content = form.data["content"]
        db.session.commit()
        return { "comment": comment.to_dict() }
    return { "errors": "Unknown error: Try again later." }
        
@comment_routes.route("/<int:id>", methods=["DELETE"])
@login_required
def delete_comment(id):
    form = DeleteComment()

    form["csrf_token"].data = request.cookies["csrf_token"]

    if form.validate_on_submit():
        comment = Comment.query.get(id)
        if current_user.id != comment.user.id:
            return { "errors": "Unauthorized resource" }
        db.session.delete(comment)
        db.session.commit()
        return { "message": "Delete Successful!" }
    return { "errors": "Unknown error. Try again later" }

# /api/images routes
@image_routes.route("/<int:id>/comments")
def get_comments(id):
    comments = [comment.to_dict() for comment in Image.query.get(id).comments]
    comments.sort(key=lambda elem: elem["created_at"], reverse=True)
    return { "comments": comments }

@image_routes.route("/<int:id>/comments", methods=["POST"])
@login_required
def post_comment(id):
    form = CommentForm()

    form["csrf_token"].data = request.cookies["csrf_token"]

    if form.validate_on_submit():
        image = Image.query.get(id)
        image_owner_id = image.user_id
        following = User.query\
            .get(current_user.id).following
        following_ids = [user.id for user in following]

        if image_owner_id not in following_ids and\
                    current_user.id != image.user_id:
            return { "errors": "Unauthorized resource" }

        params = {
            "user_id": current_user.id,
            "image_id": id,
            "content": form.data["content"]
        }

        comment = Comment(**params)
        db.session.add(comment)
        db.session.commit()
        return { "comment": comment.to_dict() }
    return { "errors": "Unknown error. Try again later."}

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from sqlalchemy import func

from models import CommunityPost, CommunityReply, User, db
from wrappers import login_required

taverns_bp = Blueprint("taverns", __name__, url_prefix="/taverns")


@taverns_bp.route("/")
@login_required
def taverns():
    # Get reply counts for each post using a subquery
    reply_counts = (
        db.session.query(
            CommunityReply.post_id, func.count(CommunityReply.id).label("reply_count")
        )
        .group_by(CommunityReply.post_id)
        .subquery()
    )

    # Query posts with joined user data and reply counts
    posts = (
        db.session.query(
            CommunityPost,
            User.username.label("creator_username"),
            func.coalesce(reply_counts.c.reply_count, 0).label("total_comments"),
        )
        .join(User, CommunityPost.creator_id == User.id)
        .outerjoin(reply_counts, CommunityPost.id == reply_counts.c.post_id)
        .all()
    )

    # Format the posts for template rendering
    formatted_posts = []
    for post, username, total_comments in posts:
        post_dict = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "category": post.category,
            "tags": post.tags.split(",") if post.tags else [],
            "total_comments": total_comments,
            "upvotes": post.upvotes,
            "downvotes": post.downvotes,
            "created_at": post.created_at,
            "creator_id": post.creator_id,
            "creator_username": username,
        }
        formatted_posts.append(post_dict)

    return render_template("taverns/taverns_index.html", posts=formatted_posts)


@taverns_bp.route("/create_post", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        # Get form data
        title = request.form.get("title")
        content = request.form.get("content")
        category = request.form.get("category")
        tags = request.form.get("tags")

        # Create new post
        new_post = CommunityPost(
            creator_id=session.get("user_id"),
            title=title,
            content=content,
            category=category,
            tags=tags,
        )

        try:
            db.session.add(new_post)
            db.session.commit()
            flash("Post published successfully!", "success")
            return redirect(url_for("taverns.taverns"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error creating post: {str(e)}", "danger")
            return redirect(url_for("taverns.create_post"))

    return render_template("taverns/taverns_post_crafter.html")


@taverns_bp.route("/post/<int:post_id>")
def view_post(post_id):
    try:
        # Get the post with creator info
        post = CommunityPost.query.get_or_404(post_id)

        # Get the creator's username
        creator = User.query.get(post.creator_id)
        post.creator_username = creator.username if creator else "Unknown User"

        # Get comments with user info
        comments = (
            db.session.query(CommunityReply, User.username)
            .join(User, CommunityReply.creator_id == User.id)
            .filter(CommunityReply.post_id == post_id)
            .all()
        )

        # Format comments
        formatted_comments = []
        for comment, username in comments:
            comment_dict = {
                "id": comment.id,
                "content": comment.content,
                "user_id": comment.creator_id,
                "username": username,
                "upvotes": comment.upvotes,
                "downvotes": comment.downvotes,
                "created_at": comment.created_at,
            }
            formatted_comments.append(comment_dict)

        return render_template(
            "taverns/taverns_view_post.html",
            post=post,
            comments=formatted_comments,
        )
    except Exception as e:
        print(f"Error in view_post: {e}")
        raise 500


@taverns_bp.route("/api/post/<int:post_id>/reply", methods=["POST"])
@login_required
def post_comment(post_id):
    try:
        content = request.form.get("comment")
        if not content or content.strip() == "":
            flash("Comment cannot be empty", "danger")
            return redirect(f"/taverns/post/{post_id}")

        new_reply = CommunityReply(
            post_id=post_id, creator_id=session.get("user_id"), content=content
        )

        db.session.add(new_reply)
        db.session.commit()
        flash("Comment submitted successfully!", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error submitting comment: {str(e)}", "danger")

    return redirect(f"/taverns/post/{post_id}")

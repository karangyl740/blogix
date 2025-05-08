from flask import Blueprint, request, jsonify
from extensions import db
from models.models import BlogPost

blog_bp = Blueprint("blog_bp", __name__)

@blog_bp.route("/blogs", methods=["GET"])
def get_blogs():
    blogs = BlogPost.query.all()
    return jsonify([b.to_dict() for b in blogs])

@blog_bp.route("/blogs", methods=["POST"])
def add_blog():
    data = request.get_json()
    blog = BlogPost(**data)
    db.session.add(blog)
    db.session.commit()
    return jsonify(blog.to_dict()), 201

@blog_bp.route("/blogs/<int:id>", methods=["PUT"])
def update_blog(id):
    data = request.get_json()
    blog = BlogPost.query.get_or_404(id)
    blog.title = data.get("title", blog.title)
    blog.content = data.get("content", blog.content)
    blog.author = data.get("author", blog.author)
    db.session.commit()
    return jsonify(blog.to_dict())

@blog_bp.route("/blogs/<int:id>", methods=["DELETE"])
def delete_blog(id):
    blog = BlogPost.query.get_or_404(id)
    db.session.delete(blog)
    db.session.commit()
    return jsonify({"message": "Blog deleted"})

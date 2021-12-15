from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db, login_manager, application, api, ma, application
from flask_login import UserMixin
from flask import Flask, request
from flask_restful import Api, Resource


#new section of code
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(application.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id' : self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(application.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    

#creating a schema based on Post model using marshmallow
class PostSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "content","user_id")
        model = Post

post_schema = PostSchema()
posts_schema = PostSchema(many=True)

#creating a new restful resource
class PostListResource(Resource):
    def get(self):
        posts = Post.query.all()
        return posts_schema.dump(posts)
    
    def post(self):
        new_post = Post(
            title=request.json['title'],
            content=request.json['content'],
            user_id=request.json['user_id']
        )
        db.session.add(new_post)
        db.session.commit()
        return post_schema.dump(new_post)

api.add_resource(PostListResource, '/posts')

class PostResource(Resource):
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return post_schema.dump(post)
    
    def patch(self, post_id):
        post = Post.query.get_or_404(post_id)

        if 'title' in request.json:
            post.title = request.json['title']
        if 'content' in request.json:
            post.content = request.json['content']

        db.session.commit()
        return post_schema.dump(post)

    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return '', 204

api.add_resource(PostResource, '/posts/<int:post_id>')



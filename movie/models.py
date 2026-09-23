from alembic.autogenerate.compare import server_defaults

from movie import db

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contact = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    poster_url = db.Column(db.String(255), nullable=True)
    trailer_url = db.Column(db.String(500), nullable=True)
    runtime = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.String(10), nullable=True)
    status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)
    director = db.Column(db.String(100),nullable=True)
    cast = db.Column(db.String(255),nullable=True)
    like_count = db.Column(db.Integer, default=0, nullable=False, server_default='0')

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id', ondelete='CASCADE'))
    movie = db.relationship(Movie, backref=db.backref('movies'))
    name = db.Column(db.String(100), nullable=False)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id', ondelete='CASCADE'), nullable=False)
    movie = db.relationship(Movie, backref=db.backref('reviews', cascade='all, delete-orphan'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship(User, backref=db.backref('reviews'))
    rating = db.Column(db.Float, nullable=False)          # 평점 (예: 0~10)
    content = db.Column(db.Text, nullable=True)            # 관람평 내용
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)

class Trailer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer,db.ForeignKey('movie.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    trailer_url = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)
    movie = db.relationship(Movie,backref=db.backref('trailers',cascade='all, delete-orphan'))

class Still(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id', ondelete='CASCADE'), nullable=False)
    movie = db.relationship(Movie, backref=db.backref('stills', cascade='all, delete-orphan'))
    image_url = db.Column(db.String(255), nullable=False)
    width = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)

class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_date = db.Column(db.DateTime, nullable=False)
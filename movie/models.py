from alembic.autogenerate.compare import server_defaults
from datetime import datetime
from movie import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contact = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.now)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    poster_url = db.Column(db.String(255), nullable=True)
    trailer_url = db.Column(db.String(500), nullable=True)
    runtime = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.String(10), nullable=True)
    status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.now)
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
    content = db.Column(db.Text, nullable=True)         
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.now)

class Trailer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer,db.ForeignKey('movie.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    trailer_url = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.now)
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

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.now)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=False)
    question = db.relationship(Question, backref=db.backref('answers',cascade='all, delete-orphan'))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.now)

class Theater(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    region = db.Column(db.String(100), nullable=False)

class Auditorium(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theater_id = db.Column(db.Integer, db.ForeignKey('theater.id', ondelete='CASCADE'), nullable=False)
    theater = db.relationship(Theater, backref=db.backref('auditoriums',cascade='all, delete-orphan'))
    name = db.Column(db.String(100), nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    seat_layout = db.Column(db.Text, nullable=False)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id', ondelete='CASCADE'), nullable=False)
    movie = db.relationship(Movie, backref=db.backref('schedules',cascade='all, delete-orphan'))
    auditorium_id = db.Column(db.Integer, db.ForeignKey('auditorium.id', ondelete='CASCADE'), nullable=False)
    auditorium = db.relationship(Auditorium, backref=db.backref('schedules',cascade='all, delete-orphan'))
    showtime = db.Column(db.DateTime, nullable=False)

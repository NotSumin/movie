from flask import Blueprint, render_template, redirect, url_for

from movie import db
from movie.models import Movie

# Blueprint: 라우팅 함수를 체계적으로 관리
bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    popular_movies = Movie.query.filter(Movie.status == "상영중").all()

    desc_movies = Movie.query.order_by(Movie.id.desc()).all()

    rand_movies = Movie.query.order_by(db.func.random()).all()

    asc_movies = Movie.query.order_by(Movie.id.asc()).all()

    return render_template(
        "index.html",
        popular_movies=popular_movies,
        desc_movies=desc_movies,
        rand_movies=rand_movies,
        asc_movies=asc_movies
    )

# 마이페이지 임시 라우트
@bp.route('/mypage')
def mypage():
    return render_template('mypage/mypage.html')

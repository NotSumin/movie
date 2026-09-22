from flask import Blueprint, render_template, redirect, url_for

from movie.models import Movie

# Blueprint: 라우팅 함수를 체계적으로 관리
bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    popular_movies = Movie.query.filter(
        Movie.status == "상영중"
    ).limit(5).all()

    # 2. 오직 부귀영화에서만!
    age_movies = Movie.query.filter(
        Movie.rating == "15세"
    ).limit(5).all()

    # 3. 감성을 채우는 예술
    long_movies = Movie.query.filter(
        Movie.runtime >= 140
    ).limit(5).all()

    # 4. 가볍게 즐기는 영화
    short_movies = Movie.query.filter(
        Movie.runtime < 120
    ).limit(5).all()

    return render_template(
        "index.html",
        popular_movies=popular_movies,
        age_movies=age_movies,
        long_movies=long_movies,
        short_movies=short_movies
    )
                           # question_list=question_list, page=page, kw=kw)
from flask import Blueprint, render_template, redirect, url_for

from movie import db
from movie.models import Movie

# Blueprint: 라우팅 함수를 체계적으로 관리
bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    # 기존 12편은 section 값이 없음(None), 새로 추가한 17편은 'exclusive' / 'art'
    popular_movies = Movie.query.filter(Movie.status == "상영중", Movie.section.is_(None)).limit(12).all()

    desc_movies = Movie.query.filter(Movie.section.is_(None)).order_by(Movie.id.desc()).limit(12).all()

    # "오직 부귀영화에서만!" -> 새 영화 9편 (매번 순서 랜덤)
    rand_movies = Movie.query.filter_by(section='exclusive') \
        .order_by(db.func.random()).limit(12).all()

    # "감성을 채우는 예술" -> 새 영화 8편
    asc_movies = Movie.query.filter_by(section='art') \
        .order_by(Movie.id.asc()).limit(12).all()

    return render_template(
        "index.html",
        popular_movies=popular_movies,
        desc_movies=desc_movies,
        rand_movies=rand_movies,
        asc_movies=asc_movies
    )

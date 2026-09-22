from flask import Blueprint, render_template

from movie.models import Movie, Review

bp = Blueprint('movie', __name__, url_prefix='/movie')


@bp.route('/detail/<int:movie_id>')
def detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    reviews = Review.query.filter_by(movie_id=movie_id) \
        .order_by(Review.created_at.desc()).all()
    review_count = len(reviews)
    avg_rating = round(sum(r.rating for r in reviews) / review_count, 1) if review_count else 0

    # TODO: 실제 추천 로직으로 교체 (지금은 같은 상태의 최신 영화 3개)
    recommended_movies = Movie.query.filter(Movie.id != movie_id) \
        .order_by(Movie.created_at.desc()).limit(3).all()

    return render_template(
        'main/movie_detail.html',
        movie=movie,
        reviews=reviews,
        review_count=review_count,
        avg_rating=avg_rating,
        recommended_movies=recommended_movies,
    )


@bp.route('/list')
def _list():
    movies = Movie.query.order_by(Movie.created_at.desc()).all()
    return render_template('main/movie_list.html', movies=movies)

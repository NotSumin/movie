from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, g, jsonify

from movie import db
from movie.models import Movie, Review, Trailer
from movie.forms import ReviewCreateForm
from movie.views.auth_views import login_required

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
    trailers = Trailer.query.filter_by(movie_id=movie_id) \
        .order_by(Trailer.id.asc()).all()

    return render_template(
        'movie/movie_detail.html',
        movie=movie,
        reviews=reviews,
        review_count=review_count,
        avg_rating=avg_rating,
        recommended_movies=recommended_movies,
        trailers=trailers,
    )


@bp.route('/<int:movie_id>/like', methods=['POST'])
def like(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    movie.like_count = (movie.like_count or 0) + 1
    db.session.commit()
    return jsonify({'like_count': movie.like_count})


@bp.route('/<int:movie_id>/review/new', methods=['GET', 'POST'])
@login_required
def review_new(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    form = ReviewCreateForm()

    if form.validate_on_submit():
        review = Review(
            movie_id=movie.id,
            user_id=g.user.id,
            rating=form.rating.data,
            content=form.content.data,
            created_at=datetime.now(),
        )
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('movie.detail', movie_id=movie.id) + '#tab-review')

    return render_template('movie/review_form.html', form=form, movie=movie)


@bp.route('/list')
def _list():
    movies = Movie.query.order_by(Movie.created_at.desc()).all()
    return render_template('movie/movie_list.html', movies=movies)


@bp.route('/trailer/<int:movie_id>')
def trailer(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    return render_template(
        'movie/movie_trailer.html',
        movie=movie
    )
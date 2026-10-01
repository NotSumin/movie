from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, g, jsonify

from movie import db
from movie.models import LikedMovie, Movie, Review, Trailer
from movie.forms import ReviewCreateForm
from movie.views.auth_views import login_required

bp = Blueprint('movie', __name__, url_prefix='/movie')


@bp.route('/detail/<int:movie_id>')
def detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if g.user:
        liked_movie = LikedMovie.query.filter_by(user_id=g.user.id, movie_id=movie_id).first()
        is_liked = True if liked_movie else False
    else:
        is_liked = False

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
        is_liked=is_liked,
        reviews=reviews,
        review_count=review_count,
        avg_rating=avg_rating,
        recommended_movies=recommended_movies,
        trailers=trailers,
    )


@bp.route('/<int:movie_id>/like', methods=['POST'])
@login_required
def like(movie_id):
    liked_movie = LikedMovie.query.filter_by(user_id=g.user.id, movie_id=movie_id).first()
    if not liked_movie:
        liked_movie = LikedMovie(
            user_id=g.user.id,
            movie_id=movie_id
        )
        db.session.add(liked_movie)
        db.session.commit()
    else:
        db.session.delete(liked_movie)
        db.session.commit()
    movie = Movie.query.get_or_404(movie_id)
    return jsonify({'like_count': len(movie.liked_movies)})


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

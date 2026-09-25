from flask import Blueprint, render_template, request
from datetime import datetime, timedelta

from movie.filter import korean_days
from movie.models import Theater

bp = Blueprint('booking', __name__, url_prefix='/booking')


@bp.route('/', methods=['GET', 'POST'])
def index():
    current_date=datetime.now()

    selected_region = request.args.get('selected_region', default='서울', type=str)
    selected_theater = request.args.get('selected_theater', default='', type=str)
    selected_date = request.args.get('selected_date', default=current_date.strftime("%Y-%m-%d"), type=str)
    selected_date_page = request.args.get('selected_date_page', default='0', type=str)

    regions_query = Theater.query.with_entities(Theater.region).distinct().all()
    regions = []
    for region in regions_query:
        regions.append(region[0])

    theaters = {}
    for region in regions:
        sub_theaters = []
        theaters_query = Theater.query.filter_by(region=region).all()
        for theater in theaters_query:
            sub_theaters.append({
                'id': theater.id,
                'name': theater.name
            })
        theaters[region] = sub_theaters
    
    datepicker = []
    months = []
    for i in range(5):
        week = []
        for j in range(7):
            date = {
                'month': '',
                'date': current_date.strftime("%d"),
                'day': korean_days(current_date.strftime("%A")),
                'full_date': current_date.strftime("%Y-%m-%d"),
                'page_no': i
            }

            if i == 0 and j == 0:
                date['day'] = '오늘'
            
            if current_date.strftime("%m") not in months:
                date['month'] = f'{current_date.strftime("%m")}월'
                months.append(current_date.strftime("%m"))

            week.append(date)
            current_date = current_date + timedelta(days=1)
        datepicker.append(week)

    return render_template(
        'booking/booking_main.html',
        regions=regions,
        selected_region=selected_region,
        selected_theater=selected_theater,
        theaters=theaters,
        selected_date=selected_date,
        selected_date_page=selected_date_page,
        datepicker=datepicker
    )

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
        'movie/movie_detail.html',
        movie=movie,
        reviews=reviews,
        review_count=review_count,
        avg_rating=avg_rating,
        recommended_movies=recommended_movies,
    )


@bp.route('/list')
def _list():
    movies = Movie.query.order_by(Movie.created_at.desc()).all()
    return render_template('movie/movie_list.html', movies=movies)

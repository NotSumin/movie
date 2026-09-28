from flask import Blueprint, render_template, request
from datetime import datetime, timedelta, time

from movie.filter import korean_days
from movie.models import Theater, Auditorium, Schedule

from sqlalchemy import func
bp = Blueprint('booking', __name__, url_prefix='/booking')


@bp.route('/', methods=['GET', 'POST'])
def index():
    current_date=datetime.now()

    selected_region = request.args.get('selected_region', default='서울', type=str)
    selected_theater = request.args.get('selected_theater', default='', type=str)
    selected_movie = request.args.get('selected_movie', default='', type=str)
    selected_date = request.args.get('selected_date', default=current_date.strftime("%Y-%m-%d"), type=str)
    selected_date_page = request.args.get('selected_date_page', default='0', type=str)

    try:
        datetime.strptime(selected_date, "%Y-%m-%d")
    except ValueError:
        selected_date = current_date.strftime("%Y-%m-%d")

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

    queried_theater = Theater.query.filter_by(name=selected_theater).first()
    queried_movies = {}
    queried_schedules = {}
    if queried_theater:
        queried_movies = {
            schedule.movie
            for auditorium in queried_theater.auditoriums
            for schedule in auditorium.schedules
            if schedule.movie is not None
        }
        if selected_movie != '':
            if selected_date == str(datetime.now().date()):
                start_time = datetime.now()
            else:
                start_time = datetime.strptime(selected_date, "%Y-%m-%d")
            end_time = datetime.combine(datetime.strptime(selected_date, "%Y-%m-%d"), time.max)
            queried_schedules = Schedule.query.join(
                Auditorium, Schedule.auditorium
            ).filter(
                Auditorium.theater_id == queried_theater.id,
                Schedule.movie_id == selected_movie,
                Schedule.showtime.between(start_time, end_time)
            ).all()

    movies = []
    for movie in queried_movies:
        movies.append({
            'id': str(movie.id),
            'title': movie.title,
            'poster_url': movie.poster_url,
            'rating': movie.rating,
            'runtime': movie.runtime,
            'created_at': movie.created_at.strftime("%Y-%m-%d"),
        })
    movies = sorted(movies, key=lambda x: x['title'])

    schedules = []
    for schedule in queried_schedules:
        schedules.append({
            'id': str(schedule.id),
            'auditorium': schedule.auditorium.name,
            'total_seats': schedule.auditorium.total_seats,
            'showtime': schedule.showtime.strftime("%H:%M")
        })
    schedules = sorted(schedules, key=lambda x: x['showtime'])

    return render_template(
        'booking/booking_main.html',
        regions=regions,
        selected_region=selected_region,
        selected_theater=selected_theater,
        selected_movie=selected_movie,
        selected_date=selected_date,
        selected_date_page=selected_date_page,
        datepicker=datepicker,
        theaters=theaters,
        movies=movies,
        schedules=schedules
    )


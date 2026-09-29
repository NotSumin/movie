import random
from datetime import datetime

from werkzeug.security import generate_password_hash

from movie import create_app, db
from movie.models import Movie, Review, User

app = create_app()

MIN_REVIEWS_PER_MOVIE = 5
MAX_REVIEWS_PER_MOVIE = 16

DUMMY_USERNAMES = [
    "movielover01", "popcorn_kim", "cinema_park", "movie_choi", "filmfan_lee",
    "watcher_jung", "reviewer_yoon", "moviebuff_han", "screen_seo", "ticket_jang",
    "movie_lim", "cine_song", "popcorn_bae", "movie_oh", "watcher_shin",
    "cinelover_kwon", "moviefan_hwang", "screenlover_ahn", "review_ko", "cine_moon",
]

REVIEW_TEMPLATES = [
    "{title} 정말 재미있게 봤어요!",
    "{title} 다시 봐도 좋네요.",
    "{title} 기대 이상이었습니다.",
    "{title}, 스토리가 인상 깊었어요.",
    "{title} 조금 아쉬운 부분도 있었지만 볼만했어요.",
    "{title} 연출이 훌륭했습니다.",
    "{title} 친구랑 같이 봤는데 만족스러웠어요.",
    "{title} 기대했던 것보다는 별로였어요.",
    "{title} 배우들 연기가 인상적이었어요.",
    "{title} 시간 가는 줄 모르고 봤어요.",
]

with app.app_context():
    dummy_users = []
    for username in DUMMY_USERNAMES:
        user = User.query.filter_by(username=username).first()
        if user is None:
            user = User(
                username=username,
                email=f"{username}@example.com",
                password=generate_password_hash("seed1234!"),
                created_at=datetime.now(),
            )
            db.session.add(user)
        dummy_users.append(user)
    db.session.flush()  # user.id 확보용

    dummy_user_ids = [u.id for u in dummy_users]
    deleted = Review.query.filter(Review.user_id.in_(dummy_user_ids)).delete(synchronize_session=False)

    total_added = 0
    for movie in Movie.query.all():
        review_count = random.randint(MIN_REVIEWS_PER_MOVIE, MAX_REVIEWS_PER_MOVIE)
        reviewers = random.sample(dummy_users, review_count)
        for user in reviewers:
            db.session.add(Review(
                movie_id=movie.id,
                user_id=user.id,
                rating=random.randint(1, 10),
                content=random.choice(REVIEW_TEMPLATES).format(title=movie.title),
                created_at=datetime.now(),
            ))
        total_added += review_count

    db.session.commit()
    print(f"기존 더미 리뷰 {deleted}개 삭제, {total_added}개 새로 입력 완료 (영화 {Movie.query.count()}편)")

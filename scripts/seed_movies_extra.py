from datetime import datetime

from movie import create_app, db
from movie.models import Movie, Genre

app = create_app()

PLACEHOLDER = "줄거리 준비 중입니다."

movies_data = [
    # ---------- 오직 부귀영화에서만! (exclusive) ----------
    {"title": "알파(ALPHA)", "section": "exclusive"},
    {"title": "트루먼의 사랑", "section": "exclusive"},
    {"title": "수련", "section": "exclusive"},
    {"title": "담요를 입은 사람", "section": "exclusive"},
    {"title": "퓨리어스", "section": "exclusive" },
    {"title": "퍼펙트슛", "section": "exclusive"},
    {"title": "철들 무렵", "section": "exclusive"},
    {"title": "드로스테 저편의 우리들", "section": "exclusive"},
    {"title": "사진의 얼굴", "section": "exclusive"},

    # ---------- 감성을 채우는 예술 (art) ----------
    {"title": "빈집의 연인들", "section": "art"},
    {"title": "지난 여름", "section": "art"},
    {"title": "싱 어게인", "section": "art"},
    {"title": "어떻게 해야 했을까?", "section": "art"},
    {"title": "델마", "section": "art"},
    {"title": "캐리어를 끄는 소녀", "section": "art"},
    {
        "title": "파리의 사생활",
        "section": "art",
        "description": "파리의 정신과 의사 릴리안이 오랫동안 담당해 온 환자의 죽음에 "
                       "의문을 품고 사건의 진실을 추적하는 미스터리 드라마.",
        "runtime": 103,
        "rating": "15세",
        "genres": ["미스터리", "드라마", "스릴러"],
    },
    {"title": "산양들", "section": "art"},
]

with app.app_context():
    added = 0
    for data in movies_data:
        if Movie.query.filter_by(title=data["title"]).first():
            print(f"[건너뜀] 이미 있음: {data['title']}")
            continue

        movie = Movie(
            title=data["title"],
            description=data.get("description", PLACEHOLDER),
            runtime=data.get("runtime", 90),
            rating=data.get("rating", "ALL"),
            status="상영중",
            section=data["section"],
            created_at=datetime.now(),
        )
        db.session.add(movie)
        db.session.flush()

        for g in data.get("genres", []):
            db.session.add(Genre(movie_id=movie.id, name=g))

        added += 1
        print(f"[추가] {data['title']} ({data['section']})")

    db.session.commit()
    print(f"완료: {added}편 추가")

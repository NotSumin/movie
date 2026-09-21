# update_posters.py
# 프로젝트 루트(config.py, seed_movies.py와 같은 위치)에 두고 실행:
#   python update_posters.py
#
# 아래 posters 딕셔너리에 title별로 실제 포스터 이미지 URL만 채워 넣으면 됨.
# 값이 빈 문자열("")인 영화는 건너뜀.

from movie import create_app, db
from movie.models import Movie

app = create_app()

posters = {
    "인턴": "https://cf.lottecinema.co.kr//Media/MovieFile/MovieImg/202609/24751_201_1.jpg",
    "부활남: 더 레드": "https://cf.lottecinema.co.kr//Media/MovieFile/MovieImg/202609/24724_201_1.jpg",
    "암살자(들)": "https://cf.lottecinema.co.kr//Media/MovieFile/MovieImg/202609/24623_201_1.jpg",
    "타짜: 벨제붑의 노래": "https://cf.lottecinema.co.kr//Media/MovieFile/MovieImg/202609/24654_201_1.jpg",
    "오디세이": "https://cf.lottecinema.co.kr//Media/MovieFile/MovieImg/202607/24128_201_1.jpg",
    "옵세션": "https://cf.lottecinema.co.kr//Media/MovieFile/MovieImg/202609/24868_201_1.jpg",
    "어벤져스: 엔드게임 (재개봉판)": "https://cf.lottecinema.co.kr//Media/MovieFile/MovieImg/202609/24982_201_1.jpg",
    "가능한 사랑": "https://cf.lottecinema.co.kr//Media/MovieFile/MovieImg/202609/24725_201_1.jpg",
    "레지던트 이블: 0번째 밤": "https://cf.lottecinema.co.kr//Media/MovieFile/MovieImg/202609/24466_201_1.jpg",
    "아버지의 집밥": "https://cf.lottecinema.co.kr//Media/MovieFile/MovieImg/202609/24872_201_1.jpg",
    "스파이더맨: 브랜드 뉴 데이": "https://cf.lottecinema.co.kr//Media/MovieFile/MovieImg/202607/24329_201_1.jpg",
    "극장판 치이카와: 인어 섬의 비밀": "https://cf.lottecinema.co.kr//Media/MovieFile/MovieImg/202609/24708_201_1.jpg",
}

with app.app_context():
    updated = 0
    not_found = []

    for title, url in posters.items():
        if not url:
            continue

        movie = Movie.query.filter_by(title=title).first()
        if movie is None:
            not_found.append(title)
            continue

        movie.poster_url = url
        updated += 1

    db.session.commit()

    print(f"{updated}편 poster_url 업데이트 완료")
    if not_found:
        print("DB에서 못 찾은 제목:", not_found)

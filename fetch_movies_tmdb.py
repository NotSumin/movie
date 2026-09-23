# fetch_movies_tmdb.py
# 프로젝트 루트(config.py, seed_movies.py와 같은 위치)에 두고 실행:
#
#   (Windows)  set TMDB_API_KEY=발급받은키
#              python fetch_movies_tmdb.py
#
#   (Mac/Linux) export TMDB_API_KEY=발급받은키
#               python fetch_movies_tmdb.py
#
# API 키를 코드에 직접 박지 않고 환경변수로 넘기는 방식입니다.
# (환경변수 설정을 매번 하기 귀찮으면, 아래 TMDB_API_KEY = "" 에
#  직접 키를 넣어도 동작은 합니다 — 단, 이 경우 절대 git에 커밋하지 마세요.)

import os
import requests

from movie import create_app, db
from movie.models import Movie, Genre

app = create_app()

TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "")
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# DB에 이미 등록된 title과, TMDB에서 검색할 때 쓸 검색어를 따로 분리했습니다.
# 재개봉판/한글 표기 때문에 검색이 안 되는 영화는 query만 영어 원제 등으로 바꿔주세요.
# tmdb_id를 직접 지정하면 검색(search_movie) 없이 그 ID로 바로 상세정보를 가져옵니다.
# 동명 영화(원작/리메이크 등)가 있어서 검색이 엉뚱한 걸 찾아올 때 사용하세요.
movie_queries = [
    {"db_title": "인턴", "query": "인턴", "year": 2026, "tmdb_id": 607833},  # 여기에 정확한 ID 넣기
    {"db_title": "부활남: 더 레드", "query": "부활남", "year": 2026},
    {"db_title": "암살자(들)", "query": "암살자들", "year": 2026},
    {"db_title": "타짜: 벨제붑의 노래", "query": "타짜 벨제붑의 노래", "year": 2026},
    {"db_title": "오디세이", "query": "The Odyssey", "year": 2026},
    {"db_title": "옵세션", "query": "Obsession", "year": 2026},
    {"db_title": "어벤져스: 엔드게임 (재개봉판)", "query": "Avengers: Endgame", "year": 2019},
    {"db_title": "가능한 사랑", "query": "가능한 사랑", "year": 2026},
    {"db_title": "레지던트 이블: 0번째 밤", "query": "Resident Evil", "year": 2026},
    {"db_title": "아버지의 집밥", "query": "아버지의 집밥", "year": 2026},
    {"db_title": "스파이더맨: 브랜드 뉴 데이", "query": "Spider-Man: Brand New Day", "year": 2026},
    {"db_title": "극장판 치이카와: 인어 섬의 비밀", "query": "치이카와", "year": 2026},
]


def search_movie(query, year=None):
    params = {
        "api_key": TMDB_API_KEY,
        "language": "ko-KR",
        "query": query,
    }
    if year:
        params["year"] = year

    res = requests.get(f"{BASE_URL}/search/movie", params=params, timeout=10)
    res.raise_for_status()
    results = res.json().get("results", [])
    return results[0] if results else None


def get_movie_detail(tmdb_id):
    res = requests.get(
        f"{BASE_URL}/movie/{tmdb_id}",
        params={"api_key": TMDB_API_KEY, "language": "ko-KR"},
        timeout=10,
    )
    res.raise_for_status()
    return res.json()


def get_kr_certification(tmdb_id):
    res = requests.get(
        f"{BASE_URL}/movie/{tmdb_id}/release_dates",
        params={"api_key": TMDB_API_KEY},
        timeout=10,
    )
    res.raise_for_status()
    for entry in res.json().get("results", []):
        if entry.get("iso_3166_1") == "KR":
            for rd in entry.get("release_dates", []):
                cert = rd.get("certification")
                if cert:
                    return cert
    return None


def get_credits(tmdb_id):
    res = requests.get(
        f"{BASE_URL}/movie/{tmdb_id}/credits",
        params={"api_key": TMDB_API_KEY, "language": "ko-KR"},
        timeout=10,
    )
    res.raise_for_status()
    data = res.json()

    directors = [c["name"] for c in data.get("crew", []) if c.get("job") == "Director"]
    director = ", ".join(directors) if directors else None

    # 출연진은 상위 5명(주연급)만
    cast_list = [c["name"] for c in data.get("cast", [])[:5]]
    cast = ", ".join(cast_list) if cast_list else None

    return director, cast


def main():
    print("스크립트 시작", flush=True)

    if not TMDB_API_KEY:
        print("TMDB_API_KEY가 설정 안 됐어요. 환경변수로 넣어주세요.", flush=True)
        return

    print(f"API 키 확인됨 (앞 6자리: {TMDB_API_KEY[:6]}...)", flush=True)

    with app.app_context():
        for item in movie_queries:
            db_title = item["db_title"]
            movie = Movie.query.filter_by(title=db_title).first()
            if movie is None:
                print(f"[건너뜀] DB에 '{db_title}' 없음 (seed_movies.py 먼저 실행했는지 확인)", flush=True)
                continue

            if item.get("tmdb_id"):
                found = {"id": item["tmdb_id"]}
            else:
                try:
                    found = search_movie(item["query"], item.get("year"))
                except requests.exceptions.RequestException as e:
                    print(f"[네트워크 에러] '{db_title}' 검색 중 오류: {e}", flush=True)
                    continue

                if found is None:
                    print(f"[검색 실패] '{db_title}' → query='{item['query']}'로 TMDB에서 못 찾음", flush=True)
                    continue

            try:
                detail = get_movie_detail(found["id"])
                cert = get_kr_certification(found["id"])
                director, cast = get_credits(found["id"])
            except requests.exceptions.RequestException as e:
                print(f"[네트워크 에러] '{db_title}' 상세정보 조회 중 오류: {e}", flush=True)
                continue

            if detail.get("overview"):
                movie.description = detail["overview"]
            if detail.get("runtime"):
                movie.runtime = detail["runtime"]
            if detail.get("poster_path"):
                movie.poster_url = IMAGE_BASE + detail["poster_path"]
            if cert:
                movie.rating = cert
            if director:
                movie.director = director
            if cast:
                movie.cast = cast

            # 기존 장르 지우고 TMDB 기준으로 다시 채움
            Genre.query.filter_by(movie_id=movie.id).delete()
            for g in detail.get("genres", []):
                db.session.add(Genre(movie_id=movie.id, name=g["name"]))

            print(f"[업데이트] {db_title} ← TMDB '{detail.get('title')}'", flush=True)

        db.session.commit()
        print("완료", flush=True)


if __name__ == "__main__":
    main()

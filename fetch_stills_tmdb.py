# fetch_stills_tmdb.py
# 프로젝트 루트에서 실행:
#   set TMDB_API_KEY=발급받은_키   (같은 터미널 탭에서)
#   python fetch_stills_tmdb.py
#
# fetch_movies_tmdb.py의 movie_queries를 그대로 재사용합니다.
# 동명 영화 등으로 잘못 매칭될 경우, fetch_movies_tmdb.py에서 확인한
# tmdb_id를 아래 movie_queries에도 똑같이 넣어주세요.

import os
import requests

from movie import create_app, db
from movie.models import Movie, Still

app = create_app()

TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "")
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w780"

MAX_STILLS_PER_MOVIE = 40  # 원하는 최대 장수 (TMDB에 그만큼 없으면 있는 만큼만)

# fetch_movies_tmdb.py의 movie_queries와 동일하게 맞춰주세요.
# (특히 tmdb_id 값 — 동명 영화 잘못 매칭 방지용)
movie_queries = [
    {"db_title": "인턴", "query": "인턴", "year": 2026, "tmdb_id": 607833},
    {"db_title": "부활남: 더 레드", "query": "부활남", "year": 2026, "tmdb_id": None},
    {"db_title": "암살자(들)", "query": "암살자들", "year": 2026, "tmdb_id": None},
    {"db_title": "타짜: 벨제붑의 노래", "query": "타짜 벨제붑의 노래", "year": 2026, "tmdb_id": None},
    {"db_title": "오디세이", "query": "The Odyssey", "year": 2026, "tmdb_id": None},
    {"db_title": "옵세션", "query": "Obsession", "year": 2026, "tmdb_id": None},
    {"db_title": "어벤져스: 엔드게임 (재개봉판)", "query": "Avengers: Endgame", "year": 2019, "tmdb_id": None},
    {"db_title": "가능한 사랑", "query": "가능한 사랑", "year": 2026, "tmdb_id": None},
    {"db_title": "레지던트 이블: 0번째 밤", "query": "Resident Evil", "year": 2026, "tmdb_id": None},
    {"db_title": "아버지의 집밥", "query": "아버지의 집밥", "year": 2026, "tmdb_id": None},
    {"db_title": "스파이더맨: 브랜드 뉴 데이", "query": "Spider-Man: Brand New Day", "year": 2026, "tmdb_id": None},
    {"db_title": "극장판 치이카와: 인어 섬의 비밀", "query": "치이카와", "year": 2026, "tmdb_id": None},
]


def search_movie(query, year=None):
    params = {"api_key": TMDB_API_KEY, "language": "ko-KR", "query": query}
    if year:
        params["year"] = year
    res = requests.get(f"{BASE_URL}/search/movie", params=params, timeout=10)
    res.raise_for_status()
    results = res.json().get("results", [])
    return results[0] if results else None


def get_backdrops(tmdb_id):
    res = requests.get(
        f"{BASE_URL}/movie/{tmdb_id}/images",
        params={"api_key": TMDB_API_KEY, "include_image_language": "ko,null,en"},
        timeout=10,
    )
    res.raise_for_status()
    backdrops = res.json().get("backdrops", [])
    # 화질/투표 좋은 순으로 정렬
    backdrops.sort(key=lambda b: b.get("vote_average", 0), reverse=True)
    return backdrops[:MAX_STILLS_PER_MOVIE]


def main():
    print("스크립트 시작", flush=True)
    if not TMDB_API_KEY:
        print("TMDB_API_KEY가 설정 안 됐어요.", flush=True)
        return

    with app.app_context():
        for item in movie_queries:
            db_title = item["db_title"]
            movie = Movie.query.filter_by(title=db_title).first()
            if movie is None:
                print(f"[건너뜀] DB에 '{db_title}' 없음", flush=True)
                continue

            try:
                if item.get("tmdb_id"):
                    tmdb_id = item["tmdb_id"]
                else:
                    found = search_movie(item["query"], item.get("year"))
                    if found is None:
                        print(f"[검색 실패] '{db_title}'", flush=True)
                        continue
                    tmdb_id = found["id"]

                backdrops = get_backdrops(tmdb_id)
            except requests.exceptions.RequestException as e:
                print(f"[네트워크 에러] '{db_title}': {e}", flush=True)
                continue

            if not backdrops:
                print(f"[스틸컷 없음] '{db_title}'", flush=True)
                continue

            # 기존 스틸컷 지우고 새로 채움
            Still.query.filter_by(movie_id=movie.id).delete()
            for b in backdrops:
                db.session.add(Still(
                    movie_id=movie.id,
                    image_url=IMAGE_BASE + b["file_path"],
                    width=b.get("width"),
                    height=b.get("height"),
                ))

            print(f"[업데이트] {db_title} ← 스틸컷 {len(backdrops)}장", flush=True)

        db.session.commit()
        print("완료", flush=True)


if __name__ == "__main__":
    main()
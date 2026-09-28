import os
import requests

from movie import create_app, db
from movie.models import Movie, Still

app = create_app()

TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "9f7d17c5b4295b8147ae936221aaa104")
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w780"

MAX_STILLS_PER_MOVIE = 40  # 원하는 최대 장수 (TMDB에 그만큼 없으면 있는 만큼만)

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

    {"db_title": "알파(ALPHA)", "query": "알파", "year": None, "tmdb_id": 1284460},
    {"db_title": "트루먼의 사랑", "query": "트루먼의 사랑", "year": None, "tmdb_id": 1384111},
    {"db_title": "수련", "query": "수련", "year": None, "tmdb_id": 1330701},
    {"db_title": "담요를 입은 사람", "query": "담요를 입은 사람", "year": None, "tmdb_id": 1251630},
    {"db_title": "퓨리어스", "query": "퓨리어스", "year": None, "tmdb_id": 1280738},
    {"db_title": "퍼펙트슛", "query": "퍼펙트슛", "year": None, "tmdb_id": 1356079},
    {"db_title": "철들 무렵", "query": "철들 무렵", "year": None, "tmdb_id": 1532365},
    {"db_title": "드로스테 저편의 우리들", "query": "드로스테 저편의 우리들", "year": None, "tmdb_id": 805627},
    {"db_title": "사진의 얼굴", "query": "사진의 얼굴", "year": None, "tmdb_id": 1522680},
    {"db_title": "빈집의 연인들", "query": "빈집의 연인들", "year": None, "tmdb_id": 1447630},
    {"db_title": "지난 여름", "query": "지난 여름", "year": None, "tmdb_id": 1172563},
    {"db_title": "싱 어게인", "query": "싱 어게인", "year": None, "tmdb_id": 1284016},
    {"db_title": "어떻게 해야 했을까?", "query": "어떻게 해야 했을까", "year": None, "tmdb_id": 1188968},
    {"db_title": "델마", "query": "델마", "year": None, "tmdb_id": 401898},
    {"db_title": "캐리어를 끄는 소녀", "query": "캐리어를 끄는 소녀", "year": None, "tmdb_id": 1425837},
    {"db_title": "파리의 사생활", "query": "파리의 사생활", "year": None, "tmdb_id": 1290432},
    {"db_title": "산양들", "query": "산양들", "year": None, "tmdb_id": 1453301},
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
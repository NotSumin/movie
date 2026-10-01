import os
import requests

from movie import create_app, db
from movie.models import Movie, Genre

app = create_app()

TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "9f7d17c5b4295b8147ae936221aaa104")
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

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


# ===== [번역 추가 1] 감독/배우 이름을 한글로 바꾸는 부분 =====
_name_cache = {}


def has_hangul(text):
    return any("\uac00" <= ch <= "\ud7a3" for ch in text)


def get_korean_name(person_id, fallback):
    """인물 상세의 이름/also_known_as 에서 한글 이름을 찾고, 없으면 원래(영문) 이름을 그대로 씁니다."""
    if person_id in _name_cache:
        return _name_cache[person_id]

    name = fallback
    try:
        res = requests.get(
            f"{BASE_URL}/person/{person_id}",
            params={"api_key": TMDB_API_KEY, "language": "ko-KR"},
            timeout=10,
        )
        res.raise_for_status()
        data = res.json()
        if has_hangul(data.get("name", "")):
            name = data["name"]
        else:
            for alias in data.get("also_known_as", []):
                if has_hangul(alias):
                    name = alias
                    break
    except requests.exceptions.RequestException:
        pass  # 조회에 실패하면 영문 이름을 그대로 유지

    _name_cache[person_id] = name
    return name


def get_credits(tmdb_id):
    res = requests.get(
        f"{BASE_URL}/movie/{tmdb_id}/credits",
        params={"api_key": TMDB_API_KEY, "language": "ko-KR"},
        timeout=10,
    )
    res.raise_for_status()
    data = res.json()

    directors = [
        get_korean_name(c["id"], c["name"])
        for c in data.get("crew", []) if c.get("job") == "Director"
    ]
    director = ", ".join(directors) if directors else None

    # 출연진은 상위 5명(주연급)만
    cast_list = [get_korean_name(c["id"], c["name"]) for c in data.get("cast", [])[:5]]
    cast = ", ".join(cast_list) if cast_list else None

    return director, cast
# ===== [번역 추가 1] 끝 =====


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
            else:
                # ===== [번역 추가 2] 한국어 줄거리가 없는 영화를 알려주는 부분 =====
                print(f"[줄거리 한국어 없음] {db_title} → 직접 입력하거나 번역이 필요해요", flush=True)
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
import os
import re

from movie import create_app, db
from movie.models import Movie, Still

app = create_app()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STILL_DIR = os.path.join(BASE_DIR, "../movie", "static", "img", "stillcut")
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".webp")

FOLDERS = { "델마": "delma",
            "알파(ALPHA)":"alpha",
            "트루먼의 사랑":"truman",
            "수련":"waterlilies",
            "담요를 입은 사람":"damyo",
            "퓨리어스":"furi",
            "퍼펙트슛":"per",
            "철들 무렵":"comingofage",
            "드로스테 저편의 우리들":"droste",
            "사진의 얼굴":"photo",
            "빈집의 연인들":"emptyhouse",
            "지난 여름":"summer",
            "싱 어게인":"sing",
            "어떻게 해야 했을까?":"how",
            "캐리어를 끄는 소녀":"girl",
            "파리의 사생활":'paris',
            "산양들":"sheep",
            }
URLS = {}

def natural_key(name):
    # 1.jpg, 2.jpg, 10.jpg 가 1, 2, 10 순서가 되게 정렬
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", name)]


def collect_urls():
    result = {}

    for title, folder in FOLDERS.items():
        path = os.path.join(STILL_DIR, folder)
        if not os.path.isdir(path):
            print(f"[폴더 없음] {title}: {path}")
            continue
        files = sorted(
            (f for f in os.listdir(path) if f.lower().endswith(IMAGE_EXTS)),
            key=natural_key,
        )
        result.setdefault(title, []).extend(
            f"/static/img/stillcut/{folder}/{f}" for f in files
        )
    return result

with app.app_context():
    added = 0
    skipped = 0
    not_found = []

    for title, urls in collect_urls().items():
        movie = Movie.query.filter_by(title=title).first()
        if movie is None:
            not_found.append(title)
            continue

        for url in urls:
            if Still.query.filter_by(movie_id=movie.id, image_url=url).first():
                skipped += 1
                continue
            db.session.add(Still(movie_id=movie.id, image_url=url))
            added += 1

    db.session.commit()

    print(f"스틸컷 {added}장 추가, {skipped}장은 이미 있어서 건너뜀")
    if not_found:
        print("DB에서 못 찾은 제목:", not_found)

from movie import create_app, db
from movie.models import Movie

app = create_app()

trailers = {
    "인턴": "https://www.youtube.com/embed/dtpyrKDJPRg",
    "부활남: 더 레드": "https://www.youtube.com/embed/IHFZE-S0J-E",
    "암살자(들)": "https://www.youtube.com/embed/RnGxpZ75zFU",
    "타짜: 벨제붑의 노래": "https://www.youtube.com/embed/aMOrloU5Bho",
    "오디세이": "https://www.youtube.com/embed/RHLJSQVs2Jk",
    "옵세션": "https://www.youtube.com/embed/KDSwCAE0Bh0",
    "어벤져스: 엔드게임 (재개봉판)": "https://www.youtube.com/embed/Ko2NWhXI9e8",
    "가능한 사랑": "https://www.youtube.com/embed/W1kDOqqWNiw",
    "레지던트 이블: 0번째 밤": "https://www.youtube.com/embed/R5z9DrWOGYs",
    "아버지의 집밥": "https://www.youtube.com/embed/b0TaUIH8yVE",
    "스파이더맨: 브랜드 뉴 데이": "https://www.youtube.com/embed/KRarob7gwC4",
    "극장판 치이카와: 인어 섬의 비밀": "https://www.youtube.com/embed/-DjykB2XImc",
    "알파(ALPHA)" : "https://www.youtube.com/embed/XV7kJ2p3jP4",
    "지난 여름": "https://www.youtube.com/embed/b3V__qgmPZ4",
    "싱 어게인": "https://www.youtube.com/embed/y9MuMnjytnU",
    "어떻게 해야 했을까?": "https://www.youtube.com/embed/nXHxFr5sOrE",
    "델마": "https://www.youtube.com/embed/OgOlV0_TUSs",
    "캐리어를 끄는 소녀": "https://www.youtube.com/embed/qdN24QKH6iA",
    "파리의 사생활": "https://www.youtube.com/embed/isDFOF2rQTI",
    "산양들": "https://www.youtube.com/embed/tMFkzLBGdK8",
    "빈집의 연인들": "https://www.youtube.com/embed/TbVT92nf-hU",
    "트루먼의 사랑": "https://www.youtube.com/embed/sGiwZMI-rFk",
    "퓨리어스": "https://www.youtube.com/embed/9h002wksb-o",
    "담요를 입은 사람": "https://www.youtube.com/embed/Q1-Isdmh16U",
    "철들 무렵": "https://www.youtube.com/embed/hOAx_uhxLjM",
    "퍼펙트슛": "https://www.youtube.com/embed/0PQPhfwOfFo",
    "수련": "https://www.youtube.com/embed/I5hSlnU33uI",
    "사진의 얼굴": "https://www.youtube.com/embed/HWCYwErxE1k",
    "드로스테 저편의 우리들": "https://www.youtube.com/embed/n0peUcB4xhY",
}

with app.app_context():
    updated = 0
    not_found = []

    for title, url in trailers.items():
        if not url:
            continue

        movie = Movie.query.filter_by(title=title).first()

        if movie is None:
            not_found.append(title)
            continue

        movie.trailer_url = url
        updated += 1

    db.session.commit()

    print(f"{updated}편 trailer_url 업데이트 완료")

    if not_found:
        print("DB에서 못 찾은 제목:", not_found)
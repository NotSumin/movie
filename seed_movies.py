# seed_movies.py
# 프로젝트 루트(movie 폴더와 같은 위치)에 두고 실행: python seed_movies.py
#
# poster_url은 저작권 있는 이미지라 비워뒀습니다.
# 네이버 영화 / CGV / 롯데시네마 공식 페이지에서 포스터 이미지 링크를 복사해 채워주세요.
#
# 러닝타임에 '(추정)' 표시된 항목은 이 스크립트 작성 시점(2026-09-21) 기준
# 공식 발표가 확인되지 않아 대략적인 값을 넣은 것입니다. 정확한 값은
# 네이버 영화 등에서 확인 후 수정해주세요.

from datetime import datetime

from movie import create_app, db
from movie.models import Movie, Genre

app = create_app()

movies_data = [
    {
        "title": "인턴",
        "description": "런칭 3년 만에 패션계의 다크호스로 급부상한 CEO 선우의 회사에 "
                        "37년 차 경력의 실버 인턴 기호가 입사하면서 벌어지는 세대 초월 오피스 라이프.",
        "poster_url": "",
        "runtime": 118,  # (추정)
        "rating": "12세",  # (추정)
        "status": "상영중",
        "genres": ["코미디", "드라마"],
    },
    {
        "title": "부활남: 더 레드",
        "description": "근거 없는 자신감이 유일한 스펙인 취준생 석환이 죽은 뒤 72시간이면 "
                        "부활하는 능력을 갖고 있다는 걸 알게 된 후 의문의 추격을 당하며 펼쳐지는 이야기.",
        "poster_url": "",
        "runtime": 110,  # (추정)
        "rating": "15세",  # (추정)
        "status": "상영중",
        "genres": ["액션"],
    },
    {
        "title": "암살자(들)",
        "description": "1974년 8월 15일, 대한민국을 충격에 빠뜨린 영부인 저격 사건의 "
                        "의혹과 배후를 추적하는 기자들과 형사의 이야기를 그린 미스터리 추적극.",
        "poster_url": "",
        "runtime": 132,  # (추정)
        "rating": "15세",  # (추정)
        "status": "상영중",
        "genres": ["미스터리", "드라마"],
    },
    {
        "title": "타짜: 벨제붑의 노래",
        "description": "온라인 카지노 사업으로 세상을 다 가진 줄 알았던 장태영과, "
                        "그의 모든 것을 빼앗은 절친 박태영이 글로벌 도박판에서 다시 만나 "
                        "복수의 한판을 벌이는 타짜 시리즈의 마지막 이야기.",
        "poster_url": "",
        "runtime": 140,  # (추정)
        "rating": "15세",  # (추정)
        "status": "상영중",
        "genres": ["범죄", "드라마"],
    },
    {
        "title": "오디세이",
        "description": "트로이 전쟁을 승리로 이끈 영웅이자 지혜의 왕 오디세우스가 "
                        "전쟁 이후 아내 페넬로페가 있는 고국으로 돌아가기까지 10년에 걸쳐 "
                        "겪는 미지의 세계 속 여정을 그린 크리스토퍼 놀란 감독의 대서사시.",
        "poster_url": "",
        "runtime": 170,  # (추정)
        "rating": "12세",  # (추정)
        "status": "상영중",
        "genres": ["액션", "어드벤처"],
    },
    {
        "title": "옵세션",
        "description": "무엇이든 이루어 주는 스틱 '원 위시 윌로우'에 소원을 빈 이후 "
                        "연인이 된 두 남녀의 끔찍한 사랑에 관한 이야기. 집착이라는 감정을 "
                        "호러의 소재로 활용한 작품.",
        "poster_url": "",
        "runtime": 108,
        "rating": "청소년관람불가",
        "status": "상영중",
        "genres": ["공포", "로맨스"],
    },
    {
        "title": "어벤져스: 엔드게임 (재개봉판)",
        "description": "인피니티 워 이후 폐허가 된 우주, 살아남은 동료들의 도움을 받아 "
                        "다시 모인 어벤져스가 타노스의 행동을 되돌리고 균형을 되찾기 위해 "
                        "마지막 한 판을 벌인다.",
        "poster_url": "",
        "runtime": 185,
        "rating": "12세",  # (추정)
        "status": "상영중",
        "genres": ["액션", "SF"],
    },
    {
        "title": "가능한 사랑",
        "description": "해고노동자와 그의 아내, 그리고 다큐멘터리 감독과 그녀의 남편, "
                        "두 부부가 다큐멘터리 제작을 위해 만나 서로 다른 삶과 숨은 욕망을 "
                        "마주하는 이창동 감독 8년 만의 신작.",
        "poster_url": "",
        "runtime": 120,  # (추정)
        "rating": "15세",  # (추정)
        "status": "상영중",
        "genres": ["드라마"],
    },
    {
        "title": "레지던트 이블: 0번째 밤",
        "description": "의료 택배 기사 브라이언은 긴급 배달을 위해 심야에 라쿤 시티 "
                        "종합병원으로 향하던 중 정체불명의 존재들에게 쫓기며 필사의 생존 "
                        "사투를 벌인다. 게임 '바이오하자드' 원작의 독립적 리부트작.",
        "poster_url": "",
        "runtime": 94,
        "rating": "15세",  # (추정)
        "status": "상영중",
        "genres": ["공포"],
    },
    {
        "title": "아버지의 집밥",
        "description": "40년간 삼시세끼 집밥만 찾던 아버지 하응이 '요리백지증'에 걸린 "
                        "아내 순애를 대신해 생애 처음 부엌에 들어서며 벌어지는 이야기.",
        "poster_url": "",
        "runtime": 80,  # (추정, 세로형 숏폼 극장 합본판)
        "rating": "전체관람가",  # (추정)
        "status": "상영중",
        "genres": ["드라마", "가족"],
    },
    {
        "title": "스파이더맨: 브랜드 뉴 데이",
        "description": "'노 웨이 홈' 이후 모두의 기억에서 사라진 피터 파커 앞에 그의 "
                        "정체를 아는 의문의 적이 나타나면서 벌어지는 이야기. DNA 변이로 "
                        "통제하기 어려운 힘을 얻게 된 피터 파커가 새로운 위협에 맞선다.",
        "poster_url": "",
        "runtime": 144,
        "rating": "12세",
        "status": "상영중",
        "genres": ["액션", "SF"],
    },
    {
        "title": "극장판 치이카와: 인어 섬의 비밀",
        "description": "평소 받던 노동 급여의 100배에 달하는 매력적인 보수의 유혹에 끌려 "
                        "미지의 섬으로 떠난 치이카와와 친구들이 그곳에 감춰진 수상하고 기괴한 "
                        "비밀을 파헤치고 거대한 사건에 맞서는 이야기를 그린 애니메이션 극장판.",
        "poster_url": "",
        "runtime": 90,  # (추정)
        "rating": "전체관람가",  # (추정)
        "status": "상영중",
        "genres": ["애니메이션", "가족"],
    },
]

with app.app_context():
    for data in movies_data:
        genres = data.pop("genres", [])
        movie = Movie(**data, created_at=datetime.now())
        db.session.add(movie)
        db.session.flush()  # movie.id 확보용

        for g in genres:
            db.session.add(Genre(movie_id=movie.id, name=g))

    db.session.commit()
    print(f"{len(movies_data)}편 등록 완료")

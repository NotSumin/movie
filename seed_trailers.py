from datetime import datetime

from movie import db, create_app
from movie.models import Trailer

app = create_app()

trailers = [
    # 인턴
    Trailer(
        movie_id=2,
        title='1차 예고편',
        image_url='/static/img/movie2/1.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202609/24751_301_1.mp4',
        created_at=datetime.now()
    ),
    Trailer(
        movie_id=2,
        title='2차 예고편',
        image_url='/static/img/movie2/2.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202609/24751_301_2.mp4',
        created_at=datetime.now()
    ),

    # 부활남
    Trailer(
        movie_id=3,
        title='티저 예고편',
        image_url='/static/img/movie3/1.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202609/24724_301_1.mp4',
        created_at=datetime.now()
    ),
    Trailer(
        movie_id=3,
        title='Comming Soon 영상',
        image_url='/static/img/movie3/2.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202609/24724_301_2.mp4',
        created_at=datetime.now()
    ),
    Trailer(
        movie_id=3,
        title='메인 예고편',
        image_url='/static/img/movie3/3.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202609/24724_301_3.mp4',
        created_at=datetime.now()
    ),
    Trailer(
        movie_id=3,
        title='빨간맛 케미 캐릭터 영상',
        image_url='/static/img/movie3/4.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202609/24724_301_4.mp4',
        created_at=datetime.now()
    ),

    # 암살자
    Trailer(
        movie_id=4,
        title='티저 예고편',
        image_url='/static/img/movie4/1.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202609/24623_301_1.mp4',
        created_at=datetime.now()
    ),
    Trailer(
        movie_id=4,
        title='메인 예고편',
        image_url='/static/img/movie4/2.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202609/24623_301_2.mp4',
        created_at=datetime.now()
    ),
    Trailer(
        movie_id=4,
        title='메이킹 필름',
        image_url='/static/img/movie4/3.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202609/24623_301_3.mp4',
        created_at=datetime.now()
    ),
    Trailer(
        movie_id=4,
        title='추적자(들) 예고편',
        image_url='/static/img/movie4/4.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202609/24623_301_4.mp4',
        created_at=datetime.now()
    ),
    Trailer(
        movie_id=4,
        title='리뷰 예고편',
        image_url='/static/img/movie4/5.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202609/24623_301_5.mp4',
        created_at=datetime.now()
    ),

    # 타짜
    Trailer(
        movie_id=5,
        title='라이벌 예고편',
        image_url='/static/img/movie5/1.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202609/24654_301_1.mp4',
        created_at=datetime.now()
    ),
    Trailer(
        movie_id=5,
        title='제작기 영상',
        image_url='/static/img/movie5/2.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202609/24654_301_2.mp4',
        created_at=datetime.now()
    ),
    Trailer(
        movie_id=5,
        title='메인 예고편',
        image_url='/static/img/movie5/3.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202609/24654_301_3.mp4',
        created_at=datetime.now()
    ),
    Trailer(
        movie_id=5,
        title='20주년 피날레 축전영상',
        image_url='/static/img/movie5/4.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202609/24654_301_4.mp4',
        created_at=datetime.now()
    ),
    Trailer(
        movie_id=5,
        title='국립 MV 영상',
        image_url='/static/img/movie5/5.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202609/24654_301_5.mp4',
        created_at=datetime.now()
    ),

    # 옵세션
    Trailer(
        movie_id=7,
        title='니키니키니키니키 예고편',
        image_url='/static/img/movie7/1.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202609/24868_301_1.mp4',
        created_at=datetime.now()
    ),

    # 어벤져스
    Trailer(
        movie_id=8,
        title='리어셈블 예고편',
        image_url='/static/img/movie8/1.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202609/24982_301_1.mp4',
        created_at=datetime.now()
    ),
    Trailer(
        movie_id=8,
        title='인피니티 비전 예고편',
        image_url='/static/img/movie8/2.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202609/24982_301_2.mp4',
        created_at=datetime.now()
    ),

    # 가능한 사랑
    Trailer(
        movie_id=9,
        title='1차 예고편',
        image_url='/static/img/movie9/1.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202609/24725_301_1.mp4',
        created_at=datetime.now()
    ),

    # 레지던트 이블
    Trailer(
        movie_id=10,
        title='티저 예고편',
        image_url='/static/img/movie10/1.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202609/24466_301_1.mp4',
        created_at=datetime.now()
    ),
    Trailer(
        movie_id=10,
        title='메인 예고편',
        image_url='/static/img/movie10/1.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202609/24466_301_2.mp4',
        created_at=datetime.now()
    ),
    Trailer(
        movie_id=10,
        title='점프 스트리트 클립',
        image_url='/static/img/movie10/1.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202609/24466_301_3.mp4',
        created_at=datetime.now()
    ),

    # 아버지의 집밥
    Trailer(
        movie_id=11,
        title='예고편',
        image_url='/static/img/movie11/1.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202609/24466_301_1.mp4',
        created_at=datetime.now()
    ),

    # 스파이더맨
    Trailer(
        movie_id=12,
        title='티저 예고편',
        image_url='/static/img/movie12/1.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202607/24329_301_1.mp4',
        created_at=datetime.now()
    ),
    Trailer(
        movie_id=12,
        title='브랜드 뉴 데이 영상',
        image_url='/static/img/movie12/2.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202607/24329_301_2.mp4',
        created_at=datetime.now()
    ),
    Trailer(
        movie_id=12,
        title='30초 예고편',
        image_url='/static/img/movie12/3.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202607/24329_301_3.mp4',
        created_at=datetime.now()
    ),
    Trailer(
        movie_id=12,
        title='메인 예고편',
        image_url='/static/img/movie12/4.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202607/24329_301_4.mp4',
        created_at=datetime.now()
    ),
    Trailer(
        movie_id=12,
        title='파이널 예고편',
        image_url='/static/img/movie12/5.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202607/24329_301_5.mp4',
        created_at=datetime.now()
    ),

    # 치이카와
    Trailer(
        movie_id=13,
        title='티저 예고편',
        image_url='/static/img/movie13/1.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202609/24708_301_1.mp4',
        created_at=datetime.now()
    ),
    Trailer(
        movie_id=13,
        title='메인 예고편',
        image_url='/static/img/movie13/2.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202609/24708_301_2.mp4',
        created_at=datetime.now()
    ),
    Trailer(
        movie_id=13,
        title='더빙 예고편',
        image_url='/static/img/movie13/3.jpg',
        trailer_url='https://cf.lottecinema.co.kr//Media/MovieFile/MovieMedia/202609/24708_301_3.mp4',
        created_at=datetime.now()
    ),
]
with app.app_context():
    db.session.add_all(trailers)
    db.session.commit()

print('트레일러 데이터 입력 완료!')
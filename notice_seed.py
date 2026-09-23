from datetime import datetime

from movie import db, create_app
from movie.models import Notice

app = create_app()

with app.app_context():

    notices = [
        Notice(
            title='영화관 이용 안내',
            content='쾌적한 영화 관람을 위해 상영관 내 관람 에티켓을 지켜주시기 바랍니다.',
            create_date=datetime(2026, 9, 10)
        ),
        Notice(
            title='추석 연휴 영화관 운영 안내',
            content='추석 연휴 기간에도 정상적으로 영화관을 운영합니다. 일부 상영시간이 변경될 수 있으니 예매 전 확인해 주세요.',
            create_date=datetime(2026, 9, 5)
        ),
        Notice(
            title='개인정보 처리방침 변경 안내',
            content='개인정보 처리방침이 일부 변경되었습니다. 자세한 내용은 관련 페이지에서 확인하실 수 있습니다.',
            create_date=datetime(2026, 8, 20)
        ),
        Notice(
            title='모바일 예매 서비스 점검 안내',
            content='보다 안정적인 서비스를 제공하기 위해 모바일 예매 시스템 점검이 진행될 예정입니다.',
            create_date=datetime(2026, 8, 15)
        ),
        Notice(
            title='영화 예매 시스템 점검 안내',
            content='예매 시스템 안정화를 위한 정기 점검이 진행됩니다. 점검 시간 동안 일부 서비스 이용이 제한될 수 있습니다.',
            create_date=datetime(2026, 8, 10)
        ),
        Notice(
            title='주차장 이용 안내',
            content='영화 관람 고객께서는 영화관 이용 시 주차 할인 혜택을 받으실 수 있습니다. 주차 등록 방법을 확인해 주세요.',
            create_date=datetime(2026, 8, 3)
        ),
        Notice(
            title='신규 영화 예매 오픈 안내',
            content='새롭게 개봉하는 영화의 예매가 시작되었습니다. 상영 영화와 시간을 확인한 후 예매해 주세요.',
            create_date=datetime(2026, 7, 25)
        ),
        Notice(
            title='영화 관람 등급 안내',
            content='영화 관람 시 영화별 관람 등급을 반드시 확인해 주세요. 관람 등급에 따라 입장이 제한될 수 있습니다.',
            create_date=datetime(2026, 7, 18)
        ),
        Notice(
            title='예매 취소 및 환불 안내',
            content='예매 취소 및 환불은 영화별 취소 가능 시간에 따라 처리됩니다. 예매 내역에서 확인해 주세요.',
            create_date=datetime(2026, 7, 10)
        ),
        Notice(
            title='분실물 보관 안내',
            content='영화관 내에서 물건을 분실하신 경우 고객센터 또는 안내 데스크로 문의해 주시기 바랍니다.',
            create_date=datetime(2026, 6, 18)
        ),
        Notice(
            title='Q&A 게시판 이용 안내',
            content='서비스 이용에 대한 문의사항은 Q&A 게시판을 통해 등록해 주세요. 확인 후 답변드리겠습니다.',
            create_date=datetime(2026, 6, 5)
        ),
        Notice(
            title='회원 서비스 이용 안내',
            content='회원 가입 후 영화 예매, 예매 내역 조회 및 예매 취소 등의 서비스를 이용하실 수 있습니다.',
            create_date=datetime(2026, 5, 25)
        )
    ]

    db.session.add_all(notices)
    db.session.commit()

    print('공지사항 12개가 등록되었습니다.')

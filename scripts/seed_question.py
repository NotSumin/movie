from datetime import datetime

from sqlalchemy.sql.functions import user

from movie import create_app, db
from movie.models import Question, User

def insert_test_data(n=45):
    """테스트용 질문 데이터 n개 생성"""
    app = create_app()
    with app.app_context():  # Flask 컨텍스트 필요
        for i in range(n):
            q = Question(
                user_id=1,
                kind='영화관문의',
                title='테스트 데이터 입니다:[%03d]' % i,
                content='내용없음',
                created_at=datetime.now()
            )
            db.session.add(q)
        db.session.commit()
        print(f"{n}개의 테스트 데이터가 생성되었습니다.")

if __name__ == "__main__":
    insert_test_data()

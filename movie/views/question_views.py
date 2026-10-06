import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, g, flash, current_app
from werkzeug.utils import secure_filename

from movie import db
from movie.forms import AnswerForm, QuestionForm
from movie.models import Question
from movie.views.auth_views import login_required

bp = Blueprint('question', __name__, url_prefix='/question')


# 1. 질문 작성
@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = QuestionForm()

    if request.method == 'POST' and form.validate_on_submit():
        image_files = form.image.data
        image_paths = []

        today = datetime.now().strftime('%Y%m%d')
        upload_folder = os.path.join(current_app.root_path, 'static/photo', today)
        os.makedirs(upload_folder, exist_ok=True)

        if image_files:
            for image_file in image_files:
                # 파일이 실제로 비어있지 않은지 확인
                if image_file and image_file.filename != '':
                    filename = datetime.now().strftime("%H%M%S%f") + secure_filename(image_file.filename)
                    file_path = os.path.join(upload_folder, filename)
                    image_file.save(file_path)

                    # DB용 상대 경로 리스트에 추가
                    image_paths.append(f'photo/{today}/{filename}')
        joined_image_paths = ",".join(image_paths) if image_paths else None

        # 👉 Question 객체 생성 시 writer_name 저장
        question = Question(
            kind=form.kind.data,
            title=form.title.data,
            content=form.content.data,
            created_at=datetime.now(),
            user=g.user,
            image_path=joined_image_paths
        )

        db.session.add(question)
        db.session.commit()
        return redirect(url_for('question._list'))

    return render_template('question/question_form.html', form=form)


# 2. 질문 목록
@bp.route('/list')
def _list():
    page = request.args.get('page', default=1, type=int)
    question_list = db.session.query(Question).order_by(Question.created_at.desc())
    pagination = db.paginate(question_list, page=page, per_page=10)

    return render_template('question/question_list.html', question_list=pagination)


# 3. 질문 상세
@bp.route('/detail/<int:question_id>')
def detail(question_id):
    form = AnswerForm()
    question = db.get_or_404(Question, question_id)
    return render_template('question/question_detail.html', question=question, form=form)


# 4. 질문 수정
@bp.route('/modify/<int:question_id>', methods=['GET', 'POST'])
@login_required
def modify(question_id):
    question = db.get_or_404(Question, question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))

    form = QuestionForm()

    if request.method == 'POST' and form.validate_on_submit():
        image_files = form.image.data
        image_paths = []

        today = datetime.now().strftime('%Y%m%d')
        upload_folder = os.path.join(current_app.root_path, 'static/photo', today)
        os.makedirs(upload_folder, exist_ok=True)

        if image_files:
            for image_file in image_files:
                # 파일이 실제로 비어있지 않은지 확인
                if image_file and image_file.filename != '':
                    filename = datetime.now().strftime("%H%M%S%f") + secure_filename(image_file.filename)
                    file_path = os.path.join(upload_folder, filename)
                    image_file.save(file_path)

                    # DB용 상대 경로 리스트에 추가
                    image_paths.append(f'photo/{today}/{filename}')

        joined_image_paths = ",".join(image_paths) if image_paths else None
        question.image_path = joined_image_paths

        # 👉 수정 시 writer_name 업데이트
        question.kind = form.kind.data
        question.title = form.title.data
        question.content = form.content.data
        question.updated_at = datetime.now()

        db.session.commit()
        return redirect(url_for('question.detail', question_id=question_id))

    return render_template('question/question_form.html', question=question, form=form)


# 5. 질문 삭제
@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = db.get_or_404(Question, question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))
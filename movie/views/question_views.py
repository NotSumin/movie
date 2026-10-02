import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, g, flash, current_app
from werkzeug.utils import secure_filename

from movie import db
from movie.forms import AnswerForm
from movie.models import Question
from movie.views.auth_views import login_required

bp = Blueprint('question', __name__, url_prefix='/question')


# 1. 질문 작성
@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        kind = request.form.get('kind')
        title = request.form.get('title') or request.form.get('subject')
        content = request.form.get('content')

        if not title or not content:
            flash('제목, 내용은 필수 입력 항목입니다.')
            return render_template('question/question_form.html')

        image_file = request.files.get('image')
        image_path = None

        if image_file and image_file.filename != '':
            print("img file ")
            today = datetime.now().strftime('%Y%m%d')
            root_path = str(current_app.root_path or '')
            upload_folder = os.path.join(root_path, 'static/img', today)
            os.makedirs(upload_folder, exist_ok=True)

            filename = secure_filename(image_file.filename)
            file_path = os.path.join(upload_folder, filename)
            image_file.save(file_path)

            image_path = f'img/{today}/{filename}'

        # 👉 Question 객체 생성 시 writer_name 저장
        question = Question(
            kind=kind,
            title=title,
            content=content,
            created_at=datetime.now(),
            user=g.user,
            image_path=image_path
        )

        db.session.add(question)
        db.session.commit()
        return redirect(url_for('question._list'))

    return render_template('question/question_form.html')


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

    if request.method == 'POST':
        kind = request.form.get('kind')
        title = request.form.get('title') or request.form.get('subject')
        content = request.form.get('content')

        if not title or not content:
            flash('제목, 내용은 필수 입력 항목입니다.')
            return render_template('question/question_form.html', question=question)

        image_file = request.files.get('image')
        print(image_file)
        if image_file:
            print("img file ")
            today = datetime.now().strftime('%Y%m%d')
            root_path = str(current_app.root_path or '')
            upload_folder = os.path.join(root_path, 'static/photo', today)
            os.makedirs(upload_folder, exist_ok=True)

            filename = secure_filename(image_file.filename)
            file_path = os.path.join(upload_folder, filename)
            image_file.save(file_path)
            question.image_path = f'photo/{today}/{filename}'

        # 👉 수정 시 writer_name 업데이트
        question.kind = kind
        question.title = title
        question.content = content
        question.updated_at = datetime.now()

        db.session.commit()
        return redirect(url_for('question.detail', question_id=question_id))

    return render_template('question/question_form.html', question=question)


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
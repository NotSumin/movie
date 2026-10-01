from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for,g, flash

from movie import db
from movie.forms import QuestionForm, AnswerForm
from movie.models import Question
from movie.views.auth_views import login_required

# Blueprint: 라우팅 함수를 체계적으로 관리
bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method=='POST':
        question = Question(user_id=g.user.id, kind=request.form['kind'], title=request.form['title'], content=request.form['content'], created_at=datetime.now())
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html')

@bp.route('/list')
def _list():
    page = request.args.get('page', default=1, type=int) # 페이지
    question_list = Question.query.order_by(Question.created_at.desc())
    question_list = question_list.paginate(page=page, per_page=10)  # 한페이지에 보여야할 게시물
    return render_template('question/question_list.html', question_list=question_list)

@bp.route('/detail/<int:question_id>')
def detail(question_id):
    form = AnswerForm()  # 질문 상세 템플릿에 폼 추가
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form)

@bp.route('/modify/<int:question_id>', methods=['GET', 'POST'])
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:
        # GET 요청 시 기존 게시글 데이터로 폼을 채움
        form = QuestionForm(obj=question)

    return render_template('question/question_form.html', form=form)


@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))

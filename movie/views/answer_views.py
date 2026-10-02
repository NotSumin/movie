from datetime import datetime
from flask import Blueprint, request, redirect, url_for, render_template, g, flash

from movie import db
from movie.forms import AnswerForm
from movie.models import Question, Answer
from movie.views.auth_views import login_required

bp = Blueprint('answer', __name__, url_prefix='/answer')


# 1. 답변 등록
@bp.route('/create/<int:question_id>', methods=['POST'])
@login_required
def create(question_id):
    form = AnswerForm()
    question = db.session.get(Question, question_id) or Question.query.get_or_404(question_id)

    if form.validate_on_submit():
        content = form.content.data
        answer = Answer(question=question, content=content, created_at=datetime.now(), user=g.user)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('question.detail', question_id=question_id))

    return render_template('question/question_detail.html', question=question, form=form)


# 2. 답변 수정
@bp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=answer.question.id))

    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.updated_at = datetime.now()  # 수정 일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=answer.question.id))
    else:
        form = AnswerForm(obj=answer)

    # 맨 끝에 answer=answer 가 들어갔는지 꼭 확인하세요!
    return render_template('answer/answer_form.html', form=form, answer=answer)


# 3. 답변 삭제
@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer = db.session.get(Answer, answer_id) or Answer.query.get_or_404(answer_id)
    question_id = answer.question.id
    if g.user != answer.user:
        flash('삭제권한이 없습니다')
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))
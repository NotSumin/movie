from datetime import datetime

from flask import Blueprint, request, redirect, url_for, render_template, g

from movie import db
from movie.forms import AnswerForm
from movie.models import Question, Answer
from movie.views.auth_views import login_required

bp = Blueprint('answer', __name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>', methods=['POST'])
@login_required
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        content = form.content.data
        answer = Answer(question=question, content=content, created_at=datetime.now(), user=g.user)

    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))
    return render_template('question/question_detail.html', question=question, form=form)






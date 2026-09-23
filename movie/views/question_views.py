from flask import Blueprint, render_template, redirect, url_for

from movie.forms import QuestionForm
from movie.models import Question

# Blueprint: 라우팅 함수를 체계적으로 관리
bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list')
def _list():
    form = QuestionForm()
    question_list = Question.query.order_by(Question.created_at.desc())
    return render_template('question/question_list.html', question_list=question_list, form=form)

@bp.route('/detail/<int:question_id>')
def index(question_id):
    question_list =Question.query.order_by(Question.created_at.desc()).all()
    return render_template('question/question_list.html', question_list=question_list)
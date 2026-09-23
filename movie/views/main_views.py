from flask import Blueprint, render_template, redirect, url_for

# Blueprint: 라우팅 함수를 체계적으로 관리
bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('index.html')
                           # question_list=question_list, page=page, kw=kw)
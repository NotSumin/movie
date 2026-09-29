from flask import Blueprint, render_template
from movie.views.auth_views import login_required

bp = Blueprint('mypage', __name__, url_prefix='/mypage')

@bp.route('/')
@login_required
def mypage():
    return render_template('mypage/mypage.html')
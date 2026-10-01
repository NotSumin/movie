import functools

from datetime import datetime, timedelta

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash

from movie import db
from movie.forms import UserCreateForm, UserLoginForm
from movie.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username = form.username.data,
                password = generate_password_hash(form.password1.data),
                email = form.email.data,
                contact = form.contact.data,
                created_at = datetime.now())
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')

    return render_template('auth/signup.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None  # flash메시지용 error변수
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = '존재하지 않는 사용자입니다.'
        elif user.status != 'active':
            error = '탈퇴 처리 중인 계정입니다.'
        elif not check_password_hash(user.password, form.password.data):
            error = '비밀번호가 올바르지 않습니다.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            _next = request.args.get('next', '')  # next 파라미터 전달
            if _next:
                return redirect(_next)
            else:
                return redirect(url_for('main.index'))
        else:
            flash(error)
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

# 라우팅 함수보다 먼저 실행
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

# 데코레이터 함수: 원래 함수에 추가기능 부여
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.login', next= _next))
        return view(*args, **kwargs)
    return wrapped_view

@bp.route('/withdraw', methods=['POST'])
@login_required
def withdraw():
    user = g.user
    user.status = 'withdraw_pending'
    user.withdrawal_requested_at = datetime.now()
    db.session.commit()
    session.clear()
    flash('회원탈퇴 신청이 완료되었습니다.')
    return redirect(url_for('main.index'))

def delete_expired_users():
    expiration_date = datetime.now() - timedelta(days=7)
    users = User.query.filter(
        User.status == 'withdraw_pending',
        User.withdrawal_requested_at <= expiration_date
    ).all()
    for user in users:
        db.session.delete(user)
    if users:
        db.session.commit()

@bp.before_app_request
def cleanup_withdrawn_users():
    delete_expired_users()
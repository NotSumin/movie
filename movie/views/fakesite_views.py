from flask import Blueprint, render_template

bp = Blueprint('fakesite', __name__, url_prefix='/fakesite')


@bp.route('/instagram')
def instagram():
    return render_template('fakesite/instagram.html')


@bp.route('/facebook')
def facebook():
    return render_template('fakesite/facebook.html')


@bp.route('/youtube')
def youtube():
    return render_template('fakesite/youtube.html')

from flask import Blueprint, render_template, request
from sqlalchemy import or_

from movie.models import Notice, User


bp = Blueprint('notice', __name__, url_prefix='/notice')


# 공지사항 목록
@bp.route('/list/')
def notice_list():
    page = request.args.get('page', default=1, type=int)  # 페이지
    kw = request.args.get('kw', default='', type=str)  # 검색키워드 추가
    notice_list = Notice.query.order_by(Notice.create_date.desc())
    if kw:
        notice_list = notice_list.filter(
            or_(
                Notice.title.ilike(f'%{kw}%'),
                Notice.content.ilike(f'%{kw}%')
            )
        )
    notice_list = notice_list.paginate(page=page,per_page=10)

    return render_template('notice/notice_list.html',notice_list=notice_list, page=page, kw=kw)


# 공지사항 상세
@bp.route('/detail/<int:notice_id>/')
def notice_detail(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    # 다음글 : 현재 글보다 id가 작은 것 중 가장 가까운 글
    next_notice = Notice.query.filter( Notice.id < notice.id ).order_by(Notice.id.desc()).first()
    # 이전글 : 현재 글보다 id가 큰 것 중 가장 가까운 글
    prev_notice = Notice.query.filter( Notice.id > notice.id).order_by( Notice.id.asc()).first()

    return render_template(
        'notice/notice_detail.html',
        notice=notice,
        next_notice=next_notice,
        prev_notice=prev_notice
    )

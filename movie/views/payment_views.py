import base64
import uuid

import requests
from flask import Blueprint, render_template, request, g, jsonify

from movie import db
from movie.models import Schedule

bp = Blueprint('payment', __name__, url_prefix='/payment')

TICKET_PRICE = 13000  # 1인당 임시 고정 단가 (가격 정책 테이블 없음)
FIXED_BG_CARD_NUMBER = '1234-5678-9101'  # 연습용 고정 카드번호 (모든 계정 동일)
FIXED_BG_POINT_PASSWORD = '1234'  # 연습용 고정 BG.POINT 비밀번호 (모든 계정 동일, 신규 가입자 포함)

# 토스페이먼츠 공식 문서/샘플에 공개된 API 개별 연동(v1, requestPayment) 테스트 키
# (가입 없이 테스트 가능, 실제 결제 발생 안 함)
# 참고: https://github.com/tosspayments/tosspayments-sample-v1/blob/main/payment/payment-direct-window/node
TOSS_CLIENT_KEY = 'test_ck_D5GePWvyJnrK0W0k6q8gLzN97Eoq'
TOSS_SECRET_KEY = 'test_sk_zXLkKEypNArWmo50nX3lmeaxYG5R'
TOSS_CONFIRM_URL = 'https://api.tosspayments.com/v1/payments/confirm'


def _build_payment_context():
    schedule_id = request.args.get('schedule_id', type=int)
    seats_param = request.args.get('seats', default='', type=str)
    seats = [s for s in seats_param.split(',') if s]
    audience_count = request.args.get('count', default=len(seats) or 1, type=int)

    schedule = Schedule.query.get_or_404(schedule_id) if schedule_id else None
    amount = TICKET_PRICE * audience_count
    order_name = f'{schedule.movie.title} ({audience_count}매)' if schedule else '영화 예매'

    return {
        'schedule': schedule,
        'seats': seats,
        'audience_count': audience_count,
        'amount': amount,
        'point_balance': g.user.point if g.user else 0,
        'fixed_card_number': FIXED_BG_CARD_NUMBER,
        'order_id': uuid.uuid4().hex,
        'order_name': order_name,
    }


@bp.route('/', methods=['GET'])
def index():
    return render_template(
        'payment/payment_main.html',
        toss_client_key=TOSS_CLIENT_KEY,
        **_build_payment_context(),
    )


@bp.route('/verify-password', methods=['POST'])
def verify_password():
    if not g.user:
        return jsonify({'valid': False}), 401

    password = request.form.get('password', '')
    valid = password == FIXED_BG_POINT_PASSWORD
    return jsonify({'valid': valid})


@bp.route('/deduct-points', methods=['POST'])
def deduct_points():
    if not g.user:
        return jsonify({'success': False}), 401

    points = request.form.get('points', default=0, type=int)
    if points < 0 or points > g.user.point:
        return jsonify({'success': False, 'point_balance': g.user.point}), 400

    g.user.point -= points
    db.session.commit()
    return jsonify({'success': True, 'point_balance': g.user.point})


@bp.route('/toss/success')
def toss_success():
    payment_key = request.args.get('paymentKey')
    order_id = request.args.get('orderId')
    amount = request.args.get('amount', type=int)
    applied_points = request.args.get('appliedPoints', default=0, type=int)

    auth = base64.b64encode(f'{TOSS_SECRET_KEY}:'.encode()).decode()
    res = requests.post(
        TOSS_CONFIRM_URL,
        json={'paymentKey': payment_key, 'orderId': order_id, 'amount': amount},
        headers={
            'Authorization': f'Basic {auth}',
            'Content-Type': 'application/json',
        },
    )

    if res.status_code == 200:
        if g.user and 0 < applied_points <= g.user.point:
            g.user.point -= applied_points
            db.session.commit()
        return render_template('payment/payment_complete.html', success=True, payment=res.json())

    return render_template('payment/payment_complete.html', success=False, error=res.json())


@bp.route('/toss/fail')
def toss_fail():
    error = {
        'code': request.args.get('code'),
        'message': request.args.get('message'),
    }
    return render_template('payment/payment_complete.html', success=False, error=error)

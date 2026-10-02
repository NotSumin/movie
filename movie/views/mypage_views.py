from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, g
from movie import db
from movie.filter import korean_days
from movie.models import Reservation, Purchase
from movie.views.auth_views import login_required
from movie.views.payment_views import COUPON_COUNT_FIELDS

bp = Blueprint('mypage', __name__, url_prefix='/mypage')

@bp.route('/')
@login_required
def mypage():
    reservations = Reservation.query.filter_by(user_id=g.user.id).order_by(Reservation.paid_at.desc()).all()
    canceled_reservations = Reservation.query.filter(
        Reservation.user_id == g.user.id,
        Reservation.canceled_at.isnot(None),
    ).order_by(Reservation.canceled_at.desc()).all()
    purchases = Purchase.query.filter_by(user_id=g.user.id).order_by(Purchase.purchased_at.desc()).all()
    return render_template(
        'mypage/mypage.html',
        reservations=reservations,
        canceled_reservations=canceled_reservations,
        purchases=purchases,
        korean_days=korean_days
    )


@bp.route('/reservations/<int:reservation_id>/cancel', methods=['POST'])
@login_required
def cancel_reservation(reservation_id):
    reservation = Reservation.query.filter_by(id=reservation_id, user_id=g.user.id).first_or_404()
    if not reservation.canceled_at:
        reservation.canceled_at = datetime.now()

        if reservation.applied_points > 0:
            g.user.point += reservation.applied_points

        coupon_field = COUPON_COUNT_FIELDS.get(reservation.coupon_type)
        if coupon_field:
            setattr(g.user, coupon_field, getattr(g.user, coupon_field) + 1)

        db.session.commit()
    return redirect(url_for('mypage.mypage'))


@bp.route('/purchases/<int:purchase_id>/cancel', methods=['POST'])
@login_required
def cancel_purchase(purchase_id):
    purchase = Purchase.query.filter_by(id=purchase_id, user_id=g.user.id).first_or_404()
    if not purchase.canceled_at:
        purchase.canceled_at = datetime.now()
        db.session.commit()
    return redirect(url_for('mypage.mypage'))

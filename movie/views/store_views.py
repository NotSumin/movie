import base64
import uuid
from datetime import datetime

import requests
from flask import Blueprint, render_template, request, redirect, url_for, session, g

from movie import db
from movie.models import Purchase, PurchaseItem
from movie.views.auth_views import login_required
from movie.views.payment_views import TOSS_CLIENT_KEY, TOSS_SECRET_KEY, TOSS_CONFIRM_URL

bp = Blueprint('store', __name__, url_prefix='/store')

# 연습용 하드코딩 데이터. 추후 실제 구매 기능을 붙일 때는
# 이 목록을 DB 모델(Goods/Snack/Ticket 등) 조회로 교체하면 된다.
GOODS_PLACEHOLDER = 'https://placehold.co/300x300?text=COMING+SOON'

CATEGORIES = [
    {
        'icon': '🎬',
        'title': '영화 굿즈',
        'desc': '영화를 사랑하는 당신을 위한 <br> 다양한 굿즈를 만나보세요.',
        'image': 'stroe_1.png',
        'anchor': 'goods',
    },
    {
        'icon': '🎟️',
        'title': '관람권 & 이용권',
        'desc': '영화를 더 특별하게 즐길 수 있는<br>다양한 관람권과 이용권을 확인해보세요.',
        'image': 'stroe_2.png',
        'anchor': 'ticket',
    },
    {
        'icon': '🎁',
        'title': '선물 & 컬렉션',
        'desc': '소중한 사람에게,<br> 특별한 순간을 선물해보세요.',
        'image': 'stroe_3.png',
        'anchor': 'gift',
    },
]

PRODUCT_SECTIONS = [
    {
        'icon': '🍿',
        'title': '스낵 상품',
        'desc': '영화와 함께 즐기는 매점 인기 스낵이에요.',
        'anchor': 'snack',
        'products': [
            {'name': '콤보세트 (팝콘+콜라)', 'price': 12000, 'image': '/static/img/combo.png'},
            {'name': '카라멜 팝콘', 'price': 9000, 'image': '/static/img/popcorn_ca.png'},
            {'name': '팝콘', 'price': 8000, 'image': '/static/img/popcorn.png'},
            {'name': '탄산음료', 'price': 4500, 'image': '/static/img/coke.png'},
        ],
    },
    {
        'icon': '🎬',
        'title': '영화 굿즈',
        'desc': '영화를 사랑하는 당신을 위한 다양한 굿즈를 만나보세요.',
        'anchor': 'goods',
        'products': [
            {'name': '치이카와 굿즈 스페셜', 'image': '/static/img/goods.png'},
            {'name': '치이카와 인형 키링', 'price': 24000, 'image': '/static/img/key_1.png'},
            {'name': '치이카와 인형 키링', 'price': 24000, 'image': '/static/img/key_2.png'},
            {'name': '치이카와 키링', 'price': 18000, 'image': '/static/img/key_3.png'},
        ],
    },
    {
        'icon': '🎟️',
        'title': '관람권 & 이용권',
        'desc': '영화를 더 특별하게 즐길 수 있는 다양한 관람권과 이용권을 확인해보세요.',
        'anchor': 'ticket',
        'products': [
            {'name': 'BG.POINT 50,000원권', 'price': 48000, 'image': '/static/img/movie_ticket_b.png'},
            {'name': 'BG.POINT 30,000원권', 'price': 28000, 'image': '/static/img/movie_ticket_r.png'},
            {'name': '영화 티켓북', 'price': 22000, 'image': '/static/img/ticketbook.png'},
            {'name': '제품 준비중', 'image': GOODS_PLACEHOLDER},
        ],
    },
    {
        'icon': '🎁',
        'title': '선물 & 컬렉션',
        'desc': '소중한 사람에게, 특별한 순간을 선물해보세요.',
        'anchor': 'gift',
        'products': [
            {'name': '부귀영화 머그잔', 'price': 12000, 'image': '/static/img/mug.png'},
            {'name': '부귀영화 글래스', 'price': 13000, 'image': '/static/img/glass.png'},
            {'name': '부귀영화 코스터', 'price': 8000, 'image': '/static/img/coaster.png'},
            {'name': '부귀영화 텀블러', 'price': 28000, 'image': '/static/img/tumb.png'},
        ],
    },
]


@bp.route('/')
def index():
    return render_template(
        'store/store.html',
        categories=CATEGORIES,
        product_sections=PRODUCT_SECTIONS,
    )


def _find_product(product_id):
    anchor, _, index = product_id.rpartition('-')
    if not index.isdigit():
        return None
    section = next((s for s in PRODUCT_SECTIONS if s['anchor'] == anchor), None)
    if not section:
        return None
    products = section['products']
    index = int(index)
    if index < 0 or index >= len(products):
        return None
    return products[index]


def _cart_total(cart):
    return sum(item['price'] * item['qty'] for item in cart)


def _save_purchase(cart, order_id, payment):
    purchase = Purchase(
        user_id=g.user.id,
        order_id=order_id,
        total_amount=payment['totalAmount'],
        method=payment.get('method'),
    )
    db.session.add(purchase)
    db.session.flush()

    for item in cart:
        db.session.add(PurchaseItem(
            purchase_id=purchase.id,
            name=item['name'],
            price=item['price'],
            qty=item['qty'],
            image=item['image'],
        ))

    db.session.commit()


@bp.route('/cart/add', methods=['POST'])
@login_required
def cart_add():
    product_id = request.form.get('product_id', '')
    product = _find_product(product_id)
    if product and product.get('price'):
        cart = session.get('cart', [])
        for item in cart:
            if item['id'] == product_id:
                item['qty'] += 1
                break
        else:
            cart.append({
                'id': product_id,
                'name': product['name'],
                'price': product['price'],
                'image': product['image'],
                'qty': 1,
            })
        session['cart'] = cart
    return redirect(request.referrer or url_for('store.index'))


@bp.route('/cart/update', methods=['POST'])
@login_required
def cart_update():
    product_id = request.form.get('product_id', '')
    action = request.form.get('action', '')
    cart = session.get('cart', [])

    if action == 'remove':
        cart = [item for item in cart if item['id'] != product_id]
    else:
        for item in cart:
            if item['id'] == product_id:
                if action == 'inc':
                    item['qty'] += 1
                elif action == 'dec':
                    item['qty'] -= 1
                    if item['qty'] <= 0:
                        cart.remove(item)
                break

    session['cart'] = cart
    return redirect(url_for('store.cart'))


@bp.route('/cart')
@login_required
def cart():
    cart = session.get('cart', [])
    return render_template('store/cart.html', cart=cart, total=_cart_total(cart))


@bp.route('/checkout')
@login_required
def checkout():
    cart = session.get('cart', [])
    if not cart:
        return redirect(url_for('store.cart'))

    order_name = cart[0]['name'] if len(cart) == 1 else f"{cart[0]['name']} 외 {len(cart) - 1}건"

    return render_template(
        'store/checkout.html',
        cart=cart,
        total=_cart_total(cart),
        toss_client_key=TOSS_CLIENT_KEY,
        customer_key=f'user-{g.user.id}',
        order_id=uuid.uuid4().hex,
        order_name=order_name,
    )


@bp.route('/checkout/success')
@login_required
def checkout_success():
    payment_key = request.args.get('paymentKey')
    order_id = request.args.get('orderId')
    amount = request.args.get('amount', type=int)

    auth = base64.b64encode(f'{TOSS_SECRET_KEY}:'.encode()).decode()
    res = requests.post(
        TOSS_CONFIRM_URL,
        json={'paymentKey': payment_key, 'orderId': order_id, 'amount': amount},
        headers={
            'Authorization': f'Basic {auth}',
            'Content-Type': 'application/json',
        },
    )

    cart = session.get('cart', [])

    if res.status_code == 200:
        payment = res.json()
        payment['approvedAt'] = datetime.fromisoformat(payment['approvedAt']).strftime('%Y-%m-%d %H:%M')
        _save_purchase(cart, order_id, payment)
        session.pop('cart', None)
        return render_template('store/checkout_complete.html', success=True, payment=payment, cart=cart)

    return render_template('store/checkout_complete.html', success=False, error=res.json())


@bp.route('/checkout/fail')
@login_required
def checkout_fail():
    error = {
        'code': request.args.get('code'),
        'message': request.args.get('message'),
    }
    return render_template('store/checkout_complete.html', success=False, error=error)

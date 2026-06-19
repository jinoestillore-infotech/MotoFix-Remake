from flask import render_template, request, session, redirect, url_for, flash
from app.models.cart import Cart
from app.models.part import Part
from app.models.order import Order
from app.services.checkout_service import CheckoutService

class CheckoutController:
    """Controller guiding both Direct Buy and Shopping Cart Checkout workflows"""

    @staticmethod
    def show_checkout_page():
        """Renders payment details page sorting Direct Buy vs Cart items"""
        user_id = session.get('user_id')
        buy_now_id = request.args.get('buy_now_id')
        buy_now_qty = request.args.get('buy_now_qty', 1, type=int)

        items_to_review = []
        is_direct_buy = False
        direct_part_id = None

        if buy_now_id:
            # Flow 1: Direct Buy / Buy Now
            part = Part.find_by_id(int(buy_now_id))
            if part:
                is_direct_buy = True
                direct_part_id = part['id']
                items_to_review.append({
                    'name': part['name'],
                    'sku': part['sku'],
                    'price': part['price'],
                    'quantity': buy_now_qty,
                    'image_filename': part['image_filename']
                })
            else:
                flash("Selected part is no longer available.", "danger")
                return redirect(url_for('dashboard.client_index'))
        else:
            # Flow 2: Cart Checkout
            cart_items = Cart.get_by_user_id(user_id)
            if not cart_items:
                flash("Your shopping cart is empty.", "warning")
                return redirect(url_for('cart.view'))
            
            for item in cart_items:
                items_to_review.append({
                    'name': item['name'],
                    'sku': item['sku'],
                    'price': item['price'],
                    'quantity': item['quantity'],
                    'image_filename': item['image_filename']
                })

        # Calculate total price sum
        total_amount = sum(float(i['price']) * int(i['quantity']) for i in items_to_review)

        # Prepopulate customer fields
        customer_details = {
            'first_name': session.get('first_name', ''),
            'last_name': session.get('last_name', ''),
            'phone': session.get('phone', '') # empty string if not registered
        }

        return render_template(
            'client-page/checkout.html',
            items=items_to_review,
            total_amount=total_amount,
            customer=customer_details,
            is_direct_buy=is_direct_buy,
            direct_part_id=direct_part_id,
            direct_qty=buy_now_qty
        )

    @staticmethod
    def place_order():
        """Processes form checkout submittals"""
        user_id = session.get('user_id')
        full_name = request.form.get('full_name', '').strip()
        phone = request.form.get('phone', '').strip()
        fulfillment_method = request.form.get('fulfillment_method', 'pickup')
        address = request.form.get('address', '').strip()
        payment_method = request.form.get('payment_method', 'cod')
        notes = request.form.get('notes', '').strip()

        # Check buy-now indicators
        buy_now_id = request.form.get('buy_now_id')
        buy_now_qty = request.form.get('buy_now_qty')

        part_id = int(buy_now_id) if buy_now_id else None
        qty = int(buy_now_qty) if buy_now_qty else None

        result = CheckoutService.process_checkout(
            user_id=user_id,
            full_name=full_name,
            phone=phone,
            fulfillment_method=fulfillment_method,
            address=address,
            payment_method=payment_method,
            notes=notes,
            buy_now_part_id=part_id,
            buy_now_qty=qty
        )

        if result['success']:
            flash(result['message'], "success")
            return redirect(url_for('checkout.success', order_id=result['order_id']))
        else:
            flash(result['message'], "danger")
            # Build back parameters if failed to redirect gracefully
            if buy_now_id:
                return redirect(url_for('checkout.view', buy_now_id=buy_now_id, buy_now_qty=buy_now_qty))
            return redirect(url_for('checkout.view'))

    @staticmethod
    def show_success_page(order_id):
        """Displays visual confirmation invoice details"""
        order = Order.find_by_id(order_id)
        if not order or order['user_id'] != session.get('user_id'):
            flash("Unauthorized access to order invoice.", "danger")
            return redirect(url_for('dashboard.client_index'))

        items = Order.get_order_items(order_id)
        return render_template('client-page/order_success.html', order=order, items=items)
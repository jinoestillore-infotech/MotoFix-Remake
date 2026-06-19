from flask import render_template, request, session, jsonify
from app.services.cart_service import CartService
from app.models.cart import Cart

class CartController:
    """Controller navigating all requests regarding shopping carts"""

    @staticmethod
    def view_cart():
        """Renders standard cart interface list"""
        user_id = session.get('user_id')
        cart_items = Cart.get_by_user_id(user_id)
        return render_template('client-page/cart.html', cart_items=cart_items)

    @staticmethod
    def add_to_cart_api():
        """POST JSON API endpoint for adding items to a cart pool"""
        user_id = session.get('user_id')
        data = request.get_json() or {}
        part_id = data.get('part_id')
        quantity = int(data.get('quantity', 1))

        if not part_id:
            return jsonify({"success": False, "message": "Missing Part ID."}), 400

        result = CartService.add_to_cart(user_id, part_id, quantity)
        return jsonify(result)

    @staticmethod
    def update_quantity_api():
        """POST JSON API updating active cart item quantities"""
        user_id = session.get('user_id')
        data = request.get_json() or {}
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))

        if not item_id:
            return jsonify({"success": False, "message": "Missing Item ID."}), 400

        result = CartService.update_item_quantity(item_id, user_id, quantity)
        return jsonify(result)

    @staticmethod
    def remove_item_api():
        """POST JSON API deleting item from active cart"""
        user_id = session.get('user_id')
        data = request.get_json() or {}
        item_id = data.get('item_id')

        if not item_id:
            return jsonify({"success": False, "message": "Missing Item ID."}), 400

        result = CartService.remove_item(item_id, user_id)
        return jsonify(result)

    @staticmethod
    def get_cart_count_api():
        """GET JSON API returning live sum of products in user cart"""
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"cart_count": 0})
        count = Cart.get_total_count(user_id)
        return jsonify({"cart_count": count})
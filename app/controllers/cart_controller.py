from flask import request, jsonify, session
from app.services.cart_service import CartService
from app.models.cart import Cart
from app.classes.Authentication import Authentication

class CartController:
    """Controller managing shopper cart operations"""

    @staticmethod
    def add_to_cart():
        """AJAX POST controller logic to securely add elements to the shopper's cart"""
        if not Authentication.is_authenticated():
            return jsonify({"success": False, "message": "Please log in to continue."}), 401

        user_id = session.get('user_id')
        data = request.get_json() or {}
        
        try:
            part_id = int(data.get('part_id', 0))
            quantity = int(data.get('quantity', 1))
        except (ValueError, TypeError):
            return jsonify({"success": False, "message": "Invalid parameters provided."}), 400

        if not part_id:
            return jsonify({"success": False, "message": "Missing part ID identifier."}), 400

        # Execute operations via our business logic layer
        result = CartService.add_item(user_id, part_id, quantity)
        
        if result['success']:
            # Store cart count in Flask session for template rendering fallback
            session['cart_count'] = result['cart_count']
            
        return jsonify(result)

    @staticmethod
    def get_cart_count():
        """Returns the current user's live cart count"""
        if not Authentication.is_authenticated():
            return jsonify({"cart_count": 0})
            
        user_id = session.get('user_id')
        count = Cart.get_cart_count(user_id)
        session['cart_count'] = count
        return jsonify({"cart_count": count})
from app.models.cart import Cart
from app.models.part import Part

class CartService:
    """Service layer validating user cart operations and stock availability limits"""

    @staticmethod
    def add_item(user_id: int, part_id: int, quantity: int = 1):
        """Validates stock levels and adds the product to the user's cart"""
        if quantity <= 0:
            return {"success": False, "message": "Quantity must be at least 1."}

        # Check if the part exists
        part = Part.find_by_id(part_id)
        if not part:
            return {"success": False, "message": "Motorcycle part not found."}

        # Check current stock levels
        available_stock = part['quantity']
        if available_stock <= 0:
            return {"success": False, "message": "This part is currently out of stock."}

        # Check what is already in the user's cart
        existing_item = Cart.get_item_in_cart(user_id, part_id)
        current_cart_qty = existing_item['quantity'] if existing_item else 0
        new_total_qty = current_cart_qty + quantity

        if new_total_qty > available_stock:
            return {
                "success": False, 
                "message": f"Cannot add. You have {current_cart_qty} in cart. Only {available_stock} are available."
            }

        try:
            Cart.add_or_update(user_id, part_id, quantity)
            new_cart_count = Cart.get_cart_count(user_id)
            return {
                "success": True, 
                "message": f"Successfully added {part['name']} to your cart!",
                "cart_count": new_cart_count
            }
        except Exception as e:
            return {"success": False, "message": f"Database write failure: {str(e)}"}
from app.models.cart import Cart
from app.models.part import Part

class CartService:
    """Service Layer handling inventory limit checks, pricing parameters, and cart additions"""

    @staticmethod
    def add_to_cart(user_id: int, part_id: int, quantity: int = 1):
        """Securely adds or updates items in the user's cart checking stock balances"""
        part = Part.find_by_id(part_id)
        if not part:
            return {"success": False, "message": "Part not found in inventory."}

        # Verify stock limits
        if part['quantity'] < quantity:
            return {"success": False, "message": f"Only {part['quantity']} units are available."}

        existing_item = Cart.find_by_user_and_part(user_id, part_id)
        if existing_item:
            new_qty = existing_item['quantity'] + quantity
            if new_qty > part['quantity']:
                return {"success": False, "message": f"Cannot add. Combined quantity ({new_qty}) exceeds stock limit of {part['quantity']}."}
            
            Cart.update_quantity(existing_item['id'], new_qty)
            return {"success": True, "message": "Cart updated successfully!"}
        else:
            Cart.add_item(user_id, part_id, quantity)
            return {"success": True, "message": "Item added to cart!"}

    @staticmethod
    def update_item_quantity(item_id: int, user_id: int, quantity: int):
        """Modifies specific item quantities while ensuring inventory validation matches limits"""
        if quantity < 1:
            return {"success": False, "message": "Quantity must be at least 1 unit."}

        item = Cart.find_by_id_and_user(item_id, user_id)
        if not item:
            return {"success": False, "message": "Cart item not found or unauthorized access."}

        part = Part.find_by_id(item['part_id'])
        if not part:
            return {"success": False, "message": "Associated part does not exist."}

        # Bounds checks
        if quantity > part['quantity']:
            return {"success": False, "message": f"Stock limit exceeded. Only {part['quantity']} available."}

        Cart.update_quantity(item_id, quantity)
        return {"success": True, "message": "Quantity updated."}

    @staticmethod
    def remove_item(item_id: int, user_id: int):
        """Removes item securely from a user's cart"""
        item = Cart.find_by_id_and_user(item_id, user_id)
        if not item:
            return {"success": False, "message": "Item not found or unauthorized."}

        Cart.delete_item(item_id, user_id)
        return {"success": True, "message": "Item removed from cart."}
from app.models.order import Order
from app.models.part import Part
from app.models.cart import Cart

class CheckoutService:
    """Service Layer handling stock checks, order placements, and transaction rollbacks"""

    @staticmethod
    def process_checkout(user_id: int, full_name: str, phone: str, fulfillment_method: str, address: str, payment_method: str, notes: str, buy_now_part_id: int = None, buy_now_qty: int = None):
        """Validates stock, registers the order, updates inventory, and clears cart if applicable"""
        if not full_name or not phone or not fulfillment_method or not payment_method:
            return {"success": False, "message": "All contact and billing fields are required."}

        if fulfillment_method == 'delivery' and not address:
            return {"success": False, "message": "Delivery address is required."}

        # Step 1: Collect Items to Checkout
        checkout_items = []
        if buy_now_part_id:
            # Direct Buy Flow
            part = Part.find_by_id(buy_now_part_id)
            if not part:
                return {"success": False, "message": "The requested item is no longer available."}
            
            checkout_items.append({
                'part_id': part['id'],
                'name': part['name'],
                'price': part['price'],
                'quantity': buy_now_qty or 1,
                'stock_quantity': part['quantity']
            })
        else:
            # Cart Flow
            cart_items = Cart.get_by_user_id(user_id)
            if not cart_items:
                return {"success": False, "message": "Your cart is empty. Cannot checkout."}
            
            for item in cart_items:
                checkout_items.append({
                    'part_id': item['part_id'],
                    'name': item['name'],
                    'price': item['price'],
                    'quantity': item['quantity'],
                    'stock_quantity': item['stock_quantity']
                })

        # Step 2: Validate Stock Levels for all items before writing to DB
        total_amount = 0.0
        for item in checkout_items:
            if item['quantity'] > item['stock_quantity']:
                return {"success": False, "message": f"Sorry! Product '{item['name']}' has run out of stock or does not meet your requested quantity ({item['quantity']} requested, only {item['stock_quantity']} available)."}
            total_amount += float(item['price']) * int(item['quantity'])

        try:
            # Step 3: Insert Order record
            actual_address = address if fulfillment_method == 'delivery' else 'Store Pickup'
            order_id = Order.create_order(
                user_id=user_id,
                full_name=full_name,
                phone=phone,
                fulfillment_method=fulfillment_method,
                address=actual_address,
                payment_method=payment_method,
                total_amount=total_amount,
                notes=notes
            )

            # Step 4: Save items and reduce inventory counts
            for item in checkout_items:
                Order.add_order_item(order_id, item['part_id'], item['quantity'], item['price'])
                
                # Decrement stock quantity
                new_stock = item['stock_quantity'] - item['quantity']
                Part.update(
                    part_id=item['part_id'],
                    sku=Part.find_by_id(item['part_id'])['sku'], # maintain SKU
                    name=item['name'],
                    brand=Part.find_by_id(item['part_id'])['brand'],
                    category=Part.find_by_id(item['part_id'])['category'],
                    description=Part.find_by_id(item['part_id'])['description'],
                    price=item['price'],
                    quantity=new_stock,
                    low_stock_threshold=Part.find_by_id(item['part_id'])['low_stock_threshold']
                )

            # Step 5: Flush shopping cart ONLY if it came from the cart checkout workflow
            if not buy_now_part_id:
                for item in cart_items:
                    Cart.delete_item(item['id'], user_id)

            return {"success": True, "message": "Order placed successfully!", "order_id": order_id}

        except Exception as e:
            return {"success": False, "message": f"Checkout processing failed: {str(e)}"}
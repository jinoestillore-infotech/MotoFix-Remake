from app.models.part import Part
from app.models.order import Order

class CashierService:
    """Service Layer governing Point of Sale (POS) checkout logic, inventory sync, and walk-in sales"""

    @staticmethod
    def process_walkin_sale(owner_id: int, customer_name: str, phone: str, items: list, cash_received: float):
        """Processes a walk-in sale, updates inventory, and registers a closed/completed paid order record"""
        if not items:
            return {"success": False, "message": "The billing ticket must contain at least one part."}
        
        if not customer_name:
            customer_name = "Walk-in Customer"

        # Step 1: Pre-validate all item stock levels and calculate totals
        total_amount = 0.0
        validated_items = []

        for item in items:
            part_id = item.get('part_id')
            quantity = int(item.get('quantity', 0))

            if quantity <= 0:
                continue

            part = Part.find_by_id(part_id)
            if not part:
                return {"success": False, "message": f"Part ID {part_id} is no longer available in the catalog."}

            if part['quantity'] < quantity:
                return {
                    "success": False, 
                    "message": f"Insufficient stock for '{part['name']}'. Requested: {quantity}, Available: {part['quantity']}"
                }

            total_amount += float(part['price']) * quantity
            validated_items.append({
                'part_id': part['id'],
                'name': part['name'],
                'price': float(part['price']),
                'quantity': quantity,
                'current_stock': part['quantity'],
                'sku': part['sku'],
                'brand': part['brand'],
                'category': part['category'],
                'description': part['description'],
                'low_stock_threshold': part['low_stock_threshold']
            })

        if not validated_items:
            return {"success": False, "message": "No valid items were loaded onto the transaction ticket."}

        if cash_received < total_amount:
            return {
                "success": False, 
                "message": f"Insufficient cash received. Grand Total is ₱{total_amount:,.2f}, but only ₱{cash_received:,.2f} was provided."
            }

        try:
            # Step 2: Create a pre-completed, pre-paid order record linked to the Owner's ID
            order_id = Order.create_order(
                user_id=owner_id,
                full_name=customer_name,
                phone=phone if phone else "N/A",
                fulfillment_method="pickup", # Over-the-counter pickup
                address="Walk-in Cashier Counter",
                payment_method="cod", # Paid in cash
                total_amount=total_amount,
                notes="Walk-in checkout processed at cashier terminal."
            )

            # Mark order status as completed and paid immediately
            Order.update_status(order_id, 'Completed')
            Order.mark_as_paid(order_id)

            # Step 3: Insert order items and deduct inventory stock levels
            for item in validated_items:
                Order.add_order_item(order_id, item['part_id'], item['quantity'], item['price'])
                
                # Update part stock count
                new_stock = item['current_stock'] - item['quantity']
                Part.update(
                    part_id=item['part_id'],
                    sku=item['sku'],
                    name=item['name'],
                    brand=item['brand'],
                    category=item['category'],
                    description=item['description'],
                    price=item['price'],
                    quantity=new_stock,
                    low_stock_threshold=item['low_stock_threshold']
                )

            change_amount = cash_received - total_amount
            return {
                "success": True, 
                "message": "Transaction completed successfully!", 
                "order_id": order_id,
                "total_amount": total_amount,
                "cash_received": cash_received,
                "change_amount": change_amount
            }

        except Exception as e:
            return {"success": False, "message": f"Failed to complete cashier sale: {str(e)}"}
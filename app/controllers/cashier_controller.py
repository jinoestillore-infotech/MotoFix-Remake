# project/app/controllers/cashier_controller.py
from flask import render_template, request, session, redirect, url_for, flash, jsonify
from app.models.part import Part
from app.services.cashier_service import CashierService

class CashierController:
    """Controller guiding Point of Sale (POS) Cashier interface workflows and active draft sessions"""

    @staticmethod
    def show_cashier_panel():
        """Renders the Walk-in Cashier terminal populated by server-side Jinja ticket state"""
        ticket = session.get('cashier_ticket', {})
        
        # Calculate subtotal using safe type conversions
        subtotal = 0.0
        for item in ticket.values():
            try:
                subtotal += float(item.get('price', 0)) * int(item.get('quantity', 0))
            except (ValueError, TypeError):
                continue
                
        categories = ['Engine', 'Brakes', 'Suspension', 'Tires & Wheels', 'Electrical', 'Body & Frame', 'Fluids & Lubes', 'Accessories']
        
        # Pop receipt info on render so it only prints once and is immediately cleared from storage
        receipt = session.pop('last_checkout_receipt', None)

        # Convert dictionary values to a list to guarantee safe Jinja iteration
        ticket_items = list(ticket.values())

        return render_template(
            'owner-page/cashier.html', 
            ticket=ticket,
            ticket_items=ticket_items, 
            subtotal=subtotal, 
            categories=categories,
            receipt=receipt
        )

    @staticmethod
    def add_to_ticket(part_id):
        """Python Route: Adds an item to the cashier's active session ticket draft"""
        part = Part.find_by_id(part_id)
        if not part:
            return jsonify({"success": False, "message": "Part not found in database."}), 404

        if part['quantity'] <= 0:
            return jsonify({"success": False, "message": "Cannot add. Part is out of stock."}), 400

        ticket = session.get('cashier_ticket', {})
        part_id_str = str(part_id)

        if part_id_str in ticket:
            if ticket[part_id_str]['quantity'] + 1 > part['quantity']:
                return jsonify({"success": False, "message": f"Only {part['quantity']} units available in stock."}), 400
            ticket[part_id_str]['quantity'] += 1
        else:
            ticket[part_id_str] = {
                'part_id': part['id'],
                'name': part['name'],
                'sku': part['sku'],
                'price': float(part['price']),
                'quantity': 1,
                'stock_quantity': part['quantity']
            }

        session['cashier_ticket'] = ticket
        session.modified = True
        return jsonify({"success": True})

    @staticmethod
    def update_ticket_qty(part_id, delta):
        """Python Route: Increments or decrements active ticket quantities securely"""
        try:
            delta_int = int(delta)
        except (ValueError, TypeError):
            return jsonify({"success": False, "message": "Invalid quantity increment parameter."}), 400

        ticket = session.get('cashier_ticket', {})
        part_id_str = str(part_id)

        if part_id_str in ticket:
            new_qty = ticket[part_id_str]['quantity'] + delta_int
            if new_qty <= 0:
                ticket.pop(part_id_str)
            else:
                part = Part.find_by_id(part_id)
                if part and new_qty > part['quantity']:
                    return jsonify({"success": False, "message": f"Only {part['quantity']} units available in stock."}), 400
                ticket[part_id_str]['quantity'] = new_qty

            session['cashier_ticket'] = ticket
            session.modified = True
            return jsonify({"success": True})

        return jsonify({"success": False, "message": "Item not found in current ticket."}), 404

    @staticmethod
    def clear_ticket():
        """Python Route: Resets and flushes the current draft ticket session"""
        session['cashier_ticket'] = {}
        session.modified = True
        flash("POS ticket has been reset successfully.", "info")
        return redirect(url_for('cashier.view_terminal'))

    @staticmethod
    def process_checkout_api():
        """POST form route submitting walk-in POS transactions directly from session details"""
        owner_id = session.get('user_id')
        customer_name = request.form.get('customer_name', 'Walk-in Customer').strip()
        phone = request.form.get('phone', '').strip()
        
        try:
            cash_received = float(request.form.get('cash_received', 0))
        except (ValueError, TypeError):
            flash("Please enter a valid cash amount.", "danger")
            return redirect(url_for('cashier.view_terminal'))

        ticket = session.get('cashier_ticket', {})
        items = list(ticket.values())

        if not items:
            flash("Active ticket queue is empty. Cannot process sale.", "warning")
            return redirect(url_for('cashier.view_terminal'))

        result = CashierService.process_walkin_sale(
            owner_id=owner_id,
            customer_name=customer_name,
            phone=phone,
            items=items,
            cash_received=cash_received
        )

        if result['success']:
            # Store completed receipt data securely inside dictionary list parameters
            session['last_checkout_receipt'] = {
                'order_id': result['order_id'],
                'customer_name': customer_name,
                'total_amount': result['total_amount'],
                'cash_received': result['cash_received'],
                'change_amount': result['change_amount'],
                'items': items
            }
            session['cashier_ticket'] = {}
            session.modified = True
            flash("Walk-in sale completed successfully!", "success")
        else:
            flash(result['message'], "danger")

        return redirect(url_for('cashier.view_terminal'))

    @staticmethod
    def search_parts_api():
        """AJAX API endpoint allowing real-time cashier queries across SKU codes, brands, and categories"""
        query = request.args.get('q', '').strip().lower()
        category = request.args.get('category', 'all')
        
        all_parts = Part.find_all()
        filtered = []

        for part in all_parts:
            matches_search = not query or (
                query in part['name'].lower() or
                query in part['sku'].lower() or
                query in part['brand'].lower() or
                (part['description'] and query in part['description'].lower())
            )

            matches_category = category == 'all' or part['category'] == category

            if matches_search and matches_category:
                part_dict = dict(part)
                part_dict['price'] = float(part['price'])
                filtered.append(part_dict)

        return jsonify({"success": True, "parts": filtered})
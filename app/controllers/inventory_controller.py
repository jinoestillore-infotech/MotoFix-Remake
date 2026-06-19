from flask import render_template, request, redirect, url_for, flash
from app.services.inventory_service import InventoryService
from app.models.part import Part

class InventoryController:
    """Handles HTTP requests concerning the parts catalog management"""

    @staticmethod
    def view_inventory():
        """Renders parts workspace dashboard catalog"""
        parts = Part.find_all()
        return render_template('owner-page/inventory.html', parts=parts)

    @staticmethod
    def create_part():
        """Handles post parameters to add a part"""
        name = request.form.get('name', '')
        sku = request.form.get('sku', '')
        description = request.form.get('description', '')
        price = request.form.get('price', '0')
        quantity = request.form.get('quantity', '0')
        low_stock_threshold = request.form.get('low_stock_threshold', '5')

        result = InventoryService.add_part(
            name=name,
            sku=sku,
            description=description,
            price=price,
            quantity=quantity,
            low_stock_threshold=low_stock_threshold
        )

        if result['success']:
            flash(result['message'], "success")
        else:
            flash(result['message'], "danger")

        return redirect(url_for('inventory.view'))

    @staticmethod
    def edit_part(part_id: int):
        """Processes request metadata overrides on a specific part ID"""
        name = request.form.get('name', '')
        sku = request.form.get('sku', '')
        description = request.form.get('description', '')
        price = request.form.get('price', '0')
        quantity = request.form.get('quantity', '0')
        low_stock_threshold = request.form.get('low_stock_threshold', '5')

        result = InventoryService.update_part(
            part_id=part_id,
            name=name,
            sku=sku,
            description=description,
            price=price,
            quantity=quantity,
            low_stock_threshold=low_stock_threshold
        )

        if result['success']:
            flash(result['message'], "success")
        else:
            flash(result['message'], "danger")

        return redirect(url_for('inventory.view'))

    @staticmethod
    def remove_part(part_id: int):
        """Processes parameter routing commands to delete a catalog item"""
        result = InventoryService.delete_part(part_id)
        if result['success']:
            flash(result['message'], "success")
        else:
            flash(result['message'], "danger")
            
        return redirect(url_for('inventory.view'))
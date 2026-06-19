# project/app/controllers/inventory_controller.py
import os
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app.services.inventory_service import InventoryService
from app.models.part import Part

# Allowed image extensions config
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class InventoryController:
    """Controller directing flow of the parts inventory system including file uploads"""

    @staticmethod
    def show_parts_list():
        """Renders parts interface with listings filter attributes"""
        parts = Part.find_all()
        # Define default categories for consistent drop-down selections in forms
        categories = ['Engine', 'Brakes', 'Suspension', 'Tires & Wheels', 'Electrical', 'Body & Frame', 'Fluids & Lubes', 'Accessories']
        return render_template('owner-page/inventory.html', parts=parts, categories=categories)

    @staticmethod
    def add_part():
        """Handles POST request to save new part with secure file upload"""
        sku = request.form.get('sku', '').strip()
        name = request.form.get('name', '').strip()
        brand = request.form.get('brand', '').strip()
        category = request.form.get('category', '').strip()
        description = request.form.get('description', '').strip()
        price = request.form.get('price', '').strip()
        quantity = request.form.get('quantity', '').strip()
        low_stock_threshold = request.form.get('low_stock_threshold', '').strip()
        
        # Handling file upload
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Ensure local path exists
                upload_folder = os.path.join('app', 'static', 'uploads', 'parts')
                os.makedirs(upload_folder, exist_ok=True)
                
                # Prepend SKU to make image name unique
                unique_filename = f"{sku}_{filename}"
                file.save(os.path.join(upload_folder, unique_filename))
                image_filename = unique_filename

        result = InventoryService.add_part(
            sku=sku,
            name=name,
            brand=brand,
            category=category,
            description=description,
            price=price,
            quantity=quantity,
            low_stock_threshold=low_stock_threshold,
            image_filename=image_filename
        )

        if result['success']:
            flash(result['message'], "success")
        else:
            flash(result['message'], "danger")
        return redirect(url_for('inventory.view'))

    @staticmethod
    def edit_part(part_id):
        """Processes editing of inventory item data"""
        sku = request.form.get('sku', '').strip()
        name = request.form.get('name', '').strip()
        brand = request.form.get('brand', '').strip()
        category = request.form.get('category', '').strip()
        description = request.form.get('description', '').strip()
        price = request.form.get('price', '').strip()
        quantity = request.form.get('quantity', '').strip()
        low_stock_threshold = request.form.get('low_stock_threshold', '').strip()

        # Handle updating file upload optionally
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_folder = os.path.join('app', 'static', 'uploads', 'parts')
                os.makedirs(upload_folder, exist_ok=True)
                
                unique_filename = f"{sku}_{filename}"
                file.save(os.path.join(upload_folder, unique_filename))
                image_filename = unique_filename

        result = InventoryService.update_part(
            part_id=part_id,
            sku=sku,
            name=name,
            brand=brand,
            category=category,
            description=description,
            price=price,
            quantity=quantity,
            low_stock_threshold=low_stock_threshold,
            image_filename=image_filename
        )

        if result['success']:
            flash(result['message'], "success")
        else:
            flash(result['message'], "danger")
        return redirect(url_for('inventory.view'))

    @staticmethod
    def delete_part(part_id):
        """Removes the part from catalog entirely"""
        try:
            # Optional: You can delete the image file from file system here if desired
            Part.delete(part_id)
            flash("Part deleted successfully from inventory.", "success")
        except Exception as e:
            flash(f"Delete failed: {str(e)}", "danger")
        return redirect(url_for('inventory.view'))
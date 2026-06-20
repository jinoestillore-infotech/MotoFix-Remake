from flask import Blueprint
from app.controllers.inventory_controller import InventoryController
from app.classes.Authentication import Authentication

# Create inventory blueprint
inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/owner/inventory', methods=['GET'])
@Authentication.role_required('Owner', 'Mechanic') # Both Owners and Mechanics can view parts
def view():
    """Renders the inventory dashboard"""
    return InventoryController.show_parts_list()

@inventory_bp.route('/owner/inventory/add', methods=['POST'])
@Authentication.role_required('Owner') # Only Owners can modify parts list
def add():
    """Handles adding a new part"""
    return InventoryController.add_part()

@inventory_bp.route('/owner/inventory/edit/<int:part_id>', methods=['POST'])
@Authentication.role_required('Owner')
def edit(part_id):
    """Handles editing an existing part"""
    return InventoryController.edit_part(part_id)

@inventory_bp.route('/owner/inventory/delete/<int:part_id>', methods=['POST'])
@Authentication.role_required('Owner')
def delete(part_id):
    """Handles deleting a part"""
    return InventoryController.delete_part(part_id)
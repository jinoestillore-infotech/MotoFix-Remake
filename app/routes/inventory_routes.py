from flask import Blueprint
from app.controllers.inventory_controller import InventoryController
from app.classes.Authentication import Authentication

# Create inventory blueprint
inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/owner/inventory', methods=['GET'])
@Authentication.role_required('Owner', 'Mechanic') # Both Owners and Mechanics can view parts
def view():
    return InventoryController.view_inventory()

@inventory_bp.route('/owner/inventory/add', methods=['POST'])
@Authentication.role_required('Owner') # Only Owners can modify parts list
def add():
    return InventoryController.create_part()

@inventory_bp.route('/owner/inventory/edit/<int:part_id>', methods=['POST'])
@Authentication.role_required('Owner')
def edit(part_id):
    return InventoryController.edit_part(part_id)

@inventory_bp.route('/owner/inventory/delete/<int:part_id>', methods=['POST'])
@Authentication.role_required('Owner')
def delete(part_id):
    return InventoryController.remove_part(part_id)
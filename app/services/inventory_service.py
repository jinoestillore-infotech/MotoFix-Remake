from app.models.part import Part
import re

class InventoryService:
    """Service Business Logic managing parts updates and unique checks"""

    @staticmethod
    def add_part(name: str, sku: str, description: str, price: str, quantity: str, low_stock_threshold: str):
        """Validates parameters and issues part generation"""
        name = name.strip()
        sku = sku.strip().upper()
        description = description.strip()

        if not name or not sku:
            return {"success": False, "message": "Part Name and SKU are mandatory requirements."}

        # Check SKU alphanumeric constraint (letters, numbers, hyphens allowed)
        if not re.match(r"^[A-Z0-9\-]+$", sku):
            return {"success": False, "message": "SKU must contain only uppercase alphanumeric characters and hyphens."}

        # Value boundary checks
        try:
            val_price = float(price)
            val_qty = int(quantity)
            val_threshold = int(low_stock_threshold)

            if val_price < 0 or val_qty < 0 or val_threshold < 0:
                return {"success": False, "message": "Numerical attributes must not hold negative metrics."}
        except ValueError:
            return {"success": False, "message": "Please input clean numerical rates for price and count limits."}

        # Unique SKU constraint validation
        existing_part = Part.find_by_sku(sku)
        if existing_part:
            return {"success": False, "message": f"SKU '{sku}' already exists. Catalog SKUs must be unique."}

        try:
            new_id = Part.create(name, sku, description, val_price, val_qty, val_threshold)
            return {"success": True, "message": "Part successfully onboarded to catalog!", "part_id": new_id}
        except Exception as e:
            return {"success": False, "message": f"Error registering item: {str(e)}"}

    @staticmethod
    def update_part(part_id: int, name: str, sku: str, description: str, price: str, quantity: str, low_stock_threshold: str):
        """Validates updates and rewrites item parameters"""
        name = name.strip()
        sku = sku.strip().upper()
        description = description.strip()

        if not name or not sku:
            return {"success": False, "message": "Name and SKU cannot be submitted empty."}

        try:
            val_price = float(price)
            val_qty = int(quantity)
            val_threshold = int(low_stock_threshold)

            if val_price < 0 or val_qty < 0 or val_threshold < 0:
                return {"success": False, "message": "Values cannot be negative values."}
        except ValueError:
            return {"success": False, "message": "Price and stock quantities must be valid numbers."}

        # Check if new SKU clashes with another item
        sku_part = Part.find_by_sku(sku)
        if sku_part and sku_part['id'] != part_id:
            return {"success": False, "message": f"SKU '{sku}' is already taken by another part inventory item."}

        try:
            Part.update(part_id, name, sku, description, val_price, val_qty, val_threshold)
            return {"success": True, "message": "Inventory part details successfully updated!"}
        except Exception as e:
            return {"success": False, "message": f"Failed updating database reference: {str(e)}"}

    @staticmethod
    def delete_part(part_id: int):
        """Safe wrapper to handle catalog deletion logic"""
        existing = Part.find_by_id(part_id)
        if not existing:
            return {"success": False, "message": "Target inventory item could not be retrieved."}
        
        try:
            Part.delete(part_id)
            return {"success": True, "message": "Part removed from catalog."}
        except Exception as e:
            return {"success": False, "message": f"Database cascading error: {str(e)}"}
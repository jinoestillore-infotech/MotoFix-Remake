from app.models.part import Part
import re

class InventoryService:
    """Service layer validating inventory rules, brand categories, and price parameters"""

    @staticmethod
    def add_part(sku: str, name: str, brand: str, category: str, description: str, price: str, quantity: str, low_stock_threshold: str, image_filename: str = None):
        """Validates and creates a new parts catalog entry"""
        # Required validations
        if not sku or not name or not brand or not category or not price or not quantity:
            return {"success": False, "message": "SKU, Name, Brand, Category, Price, and Quantity are mandatory fields."}

        # Format checks
        if not re.match(r"^[A-Za-z0-9\-]+$", sku):
            return {"success": False, "message": "SKU must contain only alphanumeric characters and hyphens."}

        # Duplicate SKU verification
        if Part.find_by_sku(sku):
            return {"success": False, "message": f"Part SKU '{sku}' is already registered in the inventory."}

        try:
            # Numerical boundaries checking
            price_val = float(price)
            qty_val = int(quantity)
            threshold_val = int(low_stock_threshold) if low_stock_threshold else 5

            if price_val <= 0:
                return {"success": False, "message": "Price must be a positive number greater than zero."}
            if qty_val < 0 or threshold_val < 0:
                return {"success": False, "message": "Stock quantities cannot be negative."}

            Part.create(
                sku=sku,
                name=name,
                brand=brand,
                category=category,
                description=description,
                price=price_val,
                quantity=qty_val,
                low_stock_threshold=threshold_val,
                image_filename=image_filename
            )
            return {"success": True, "message": "Part successfully registered to inventory!"}

        except ValueError:
            return {"success": False, "message": "Price must be a number, and quantities must be whole integers."}
        except Exception as e:
            return {"success": False, "message": f"Database failure: {str(e)}"}

    @staticmethod
    def update_part(part_id: int, sku: str, name: str, brand: str, category: str, description: str, price: str, quantity: str, low_stock_threshold: str, image_filename: str = None):
        """Validates and updates an existing catalog item"""
        if not sku or not name or not brand or not category or not price or not quantity:
            return {"success": False, "message": "SKU, Name, Brand, Category, Price, and Quantity are mandatory fields."}

        if not re.match(r"^[A-Za-z0-9\-]+$", sku):
            return {"success": False, "message": "SKU format is invalid (alphanumeric and hyphens only)."}

        # SKU conflict check on other records
        existing_with_sku = Part.find_by_sku(sku)
        if existing_with_sku and existing_with_sku['id'] != int(part_id):
            return {"success": False, "message": f"Part SKU '{sku}' is already assigned to another catalog entry."}

        try:
            price_val = float(price)
            qty_val = int(quantity)
            threshold_val = int(low_stock_threshold) if low_stock_threshold else 5

            if price_val <= 0:
                return {"success": False, "message": "Price must be a positive number."}
            if qty_val < 0 or threshold_val < 0:
                return {"success": False, "message": "Quantities cannot be negative."}

            Part.update(
                part_id=part_id,
                sku=sku,
                name=name,
                brand=brand,
                category=category,
                description=description,
                price=price_val,
                quantity=qty_val,
                low_stock_threshold=threshold_val,
                image_filename=image_filename
            )
            return {"success": True, "message": "Inventory details updated successfully!"}

        except ValueError:
            return {"success": False, "message": "Invalid numeric parameter formats entered."}
        except Exception as e:
            return {"success": False, "message": f"Database failure: {str(e)}"}
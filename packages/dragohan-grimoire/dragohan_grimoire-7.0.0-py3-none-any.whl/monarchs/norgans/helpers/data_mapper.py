"""
💀 DATA MAPPER HELPER 💀

Global helper for mapping column names across all N-Organs.

Handles Google Sheets variations:
- "Phone Number " (with trailing space) → "phone"
- "Customer Name " → "name"
- "Veg %" → preference ("VEG" or "NON-VEG")
- "IsVegetarian" → category
"""

class DataMapper:
    """
    Maps various column name formats to standard names

    Supports:
    - Google Sheets exports (trailing spaces)
    - CSV files (snake_case or camelCase)
    - N8N outputs (various formats)
    """

    # Column mappings for customer data
    CUSTOMER_MAPPINGS = {
        "Phone Number ": "phone",
        "phone_number": "phone",
        "Phone": "phone",
        "Mobile": "phone",
        "mobile_number": "phone",

        "Customer Name ": "name",
        "customer_name": "name",
        "Name": "name",
        "CustomerName": "name",

        "Last Order Date": "last_order_date",
        "last_order_date": "last_order_date",
        "LastOrderDate": "last_order_date",

        "Days since last order ": "days_inactive",
        "days_inactive": "days_inactive",
        "DaysSinceLastOrder": "days_inactive",
        "days_since_last_order": "days_inactive",

        "Last Order Item ": "last_order_items",
        "last_order_items": "last_order_items",
        "LastOrderItems": "last_order_items",
        "last_order_item": "last_order_items",

        "Veg %": "veg_percentage",
        "veg_percentage": "veg_percentage",
        "VegPercentage": "veg_percentage",
        "vegetarian_percentage": "veg_percentage",

        "Total Orders": "total_orders",
        "total_orders": "total_orders",
        "TotalOrders": "total_orders"
    }

    # Column mappings for menu data
    MENU_MAPPINGS = {
        "Item": "name",
        "item_name": "name",
        "ItemName": "name",
        "dish": "name",
        "Dish": "name",
        "name": "name",
        "Name": "name",

        "Category": "category",
        "category": "category",

        "IsVegetarian": "is_vegetarian",
        "is_vegetarian": "is_vegetarian",
        "Vegetarian": "is_vegetarian",
        "vegetarian": "is_vegetarian",

        "Description": "description",
        "description": "description",
        "desc": "description",

        "Price": "price",
        "price": "price",

        "Item ID": "item_id",
        "item_id": "item_id",
        "ItemId": "item_id"
    }

    def map_customer(self, data: dict) -> dict:
        """
        Map customer data to standard format

        Args:
            data: Raw customer dict (Google Sheets row, etc)

        Returns:
            Mapped customer dict with standard keys
        """
        mapped = {}

        for key, value in data.items():
            # Try direct mapping first
            standard_key = self.CUSTOMER_MAPPINGS.get(key)

            # Fallback: lowercase with underscores
            if not standard_key:
                standard_key = key.lower().strip().replace(" ", "_")

            mapped[standard_key] = value

        # Convert veg_percentage to preference
        if "veg_percentage" in mapped:
            try:
                veg_pct = float(mapped["veg_percentage"])
                mapped["preference"] = "VEG" if veg_pct >= 0.9 else "NON-VEG"
            except (ValueError, TypeError):
                mapped["preference"] = "NON-VEG"  # Default

        # Convert last_order_items to list if string
        if "last_order_items" in mapped:
            if isinstance(mapped["last_order_items"], str):
                mapped["last_order_items"] = [mapped["last_order_items"]]
            elif not isinstance(mapped["last_order_items"], list):
                mapped["last_order_items"] = [str(mapped["last_order_items"])]

        # Ensure total_orders is int
        if "total_orders" in mapped:
            try:
                mapped["total_orders"] = int(mapped["total_orders"])
            except (ValueError, TypeError):
                mapped["total_orders"] = 1  # Default

        return mapped

    def map_menu_item(self, data: dict) -> dict:
        """
        Map menu item to standard format

        Args:
            data: Raw menu dict (Google Sheets row, etc)

        Returns:
            Mapped menu dict with standard keys
        """
        mapped = {}

        for key, value in data.items():
            # Try direct mapping first
            standard_key = self.MENU_MAPPINGS.get(key)

            # Fallback: lowercase with underscores
            if not standard_key:
                standard_key = key.lower().strip().replace(" ", "_")

            mapped[standard_key] = value

        # Convert is_vegetarian to category
        if "is_vegetarian" in mapped:
            veg_value = str(mapped["is_vegetarian"]).strip().lower()
            if veg_value in ("yes", "true", "1", "veg", "vegetarian"):
                mapped["category"] = "VEG"
            else:
                mapped["category"] = "NON-VEG"

        # Add is_available default (always True unless specified)
        if "is_available" not in mapped:
            mapped["is_available"] = True

        return mapped

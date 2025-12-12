"""
💀 N-ORGAN GLOBAL HELPERS 💀

Reusable utilities for all N-Organs:
- Phone validation (detects landlines, invalid)
- Column mapping (auto-map Google Sheets columns)
- File operations (save fallbacks, outputs)

Usage:
    helpers = NOrganHelpers()
    processed = helpers.process_customers(customers)
    helpers.writer.save_landlines(landlines, run_id)
"""

from .phone_validator import PhoneValidator
from .data_mapper import DataMapper
from .file_writer import FileWriter

class NOrganHelpers:
    """
    Unified helper interface for all N-Organs

    Provides:
    - self.phone: PhoneValidator instance
    - self.mapper: DataMapper instance
    - self.writer: FileWriter instance
    """

    def __init__(self):
        self.phone = PhoneValidator()
        self.mapper = DataMapper()
        self.writer = FileWriter()

    def process_customers(self, customers: list) -> dict:
        """
        Process raw customer data with validation and mapping

        Args:
            customers: List of customer dicts (any format)

        Returns:
            {
                "valid": [...],      # Valid customers (ready to process)
                "landlines": [...],  # Landline numbers (save to fallback)
                "invalid": [...]     # Invalid data (save to fallback)
            }
        """
        valid = []
        landlines = []
        invalid = []

        for customer in customers:
            # Map columns to standard format
            mapped = self.mapper.map_customer(customer)

            # Validate phone
            status, cleaned_phone, reason = self.phone.validate(
                mapped.get("phone", "")
            )

            if status == "valid":
                # Valid customer
                mapped["phone"] = cleaned_phone

                # Generate customer_id if missing
                if "customer_id" not in mapped or not mapped["customer_id"]:
                    mapped["customer_id"] = f"C{cleaned_phone}"

                valid.append(mapped)

            elif status == "landline":
                # Landline number - save to fallback
                landlines.append({
                    "name": mapped.get("name", "Unknown"),
                    "phone": cleaned_phone,
                    "reason": reason
                })

            else:
                # Invalid data - save to fallback
                invalid.append({
                    **mapped,
                    "reason": reason
                })

        return {
            "valid": valid,
            "landlines": landlines,
            "invalid": invalid
        }

    def process_menu(self, menu: list) -> list:
        """
        Process raw menu data with mapping

        Args:
            menu: List of menu item dicts (any format)

        Returns:
            List of mapped menu items
        """
        processed = []

        for item in menu:
            # Map columns to standard format
            mapped = self.mapper.map_menu_item(item)

            # Generate item_id if missing
            if "item_id" not in mapped or not mapped["item_id"]:
                mapped["item_id"] = f"M{len(processed) + 1}"

            processed.append(mapped)

        return processed

    def save_fallbacks(self, landlines: list, invalid: list, run_id: str) -> dict:
        """
        Save fallback files (landlines + invalid)

        Args:
            landlines: List of landline dicts
            invalid: List of invalid data dicts
            run_id: Run identifier

        Returns:
            {
                "landlines": "path/to/file.csv" or None,
                "invalid": "path/to/file.csv" or None
            }
        """
        return {
            "landlines": self.writer.save_landlines(landlines, run_id),
            "invalid": self.writer.save_invalid(invalid, run_id)
        }

    def save_outputs(self, messages: list, run_id: str, metadata: dict = None) -> dict:
        """
        Save output files (CSV + JSON)

        Args:
            messages: List of message dicts
            run_id: Run identifier
            metadata: Optional metadata

        Returns:
            {
                "csv": "path/to/file.csv",
                "json": "path/to/file.json"
            }
        """
        return {
            "csv": self.writer.save_messages_csv(messages, run_id),
            "json": self.writer.save_messages_json(messages, run_id, metadata)
        }


__all__ = [
    "NOrganHelpers",
    "PhoneValidator",
    "DataMapper",
    "FileWriter"
]

"""
💀 PHONE VALIDATOR HELPER 💀

Global helper for validating phone numbers across all N-Organs.

Categories:
- "valid": Mobile number (10 digits, starts with 6-9) → +91XXXXXXXXXX
- "landline": Landline (starts with 080, 011, etc) → saved to fallback
- "invalid": Malformed, empty, or non-numeric → saved to fallback
"""

class PhoneValidator:
    """
    Validates phone numbers and categorizes them

    Usage:
        validator = PhoneValidator()
        status, cleaned, reason = validator.validate("9876543210")

        if status == "valid":
            # Process customer
        elif status == "landline":
            # Save to landline fallback
        else:
            # Save to invalid fallback
    """

    LANDLINE_PREFIXES = ("080", "011", "022", "033", "040", "044", "079", "020")

    def validate(self, phone: str) -> tuple:
        """
        Validate and categorize phone number

        Args:
            phone: Raw phone number (any format)

        Returns:
            (status, cleaned_number, reason)

            status: "valid" | "landline" | "invalid"
            cleaned_number: Cleaned phone (with +91 if valid)
            reason: Why it's invalid/landline (None if valid)
        """

        # Handle None or empty
        if not phone or not str(phone).strip():
            return ("invalid", "", "empty")

        # Clean input (remove spaces, dashes, +91 prefix)
        cleaned = str(phone).replace(" ", "").replace("-", "").replace("+91", "").replace("(", "").replace(")", "")

        # Check if all digits
        if not cleaned.isdigit():
            return ("invalid", cleaned, "non-numeric")

        # Check if landline
        if any(cleaned.startswith(prefix) for prefix in self.LANDLINE_PREFIXES):
            return ("landline", cleaned, "landline_prefix")

        # Check if valid mobile (10 digits, starts with 6-9)
        if len(cleaned) == 10 and cleaned[0] in "6789":
            return ("valid", "91" + cleaned, None)

        # Invalid length or format
        return ("invalid", cleaned, f"invalid_format_length_{len(cleaned)}")

"""
💀 FILE WRITER HELPER 💀

Global helper for saving files across all N-Organs.

Creates:
- ./fallbacks/{run_id}_landlines.csv (landline numbers)
- ./fallbacks/{run_id}_invalid.csv (invalid data)
- ./outputs/{run_id}_messages.csv (human-readable)
- ./outputs/{run_id}_messages.json (machine-readable)
"""

import csv
import json
from pathlib import Path
from datetime import datetime

class FileWriter:
    """
    Saves data to CSV and JSON files

    Automatically creates:
    - fallbacks/ directory for error data
    - outputs/ directory for success data
    """

    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.fallback_dir = self.base_dir / "fallbacks"
        self.output_dir = self.base_dir / "outputs"

        # Create directories if they don't exist
        self.fallback_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_landlines(self, landlines: list, run_id: str) -> str:
        """
        Save landline numbers to CSV

        Args:
            landlines: List of dicts with "name", "phone", "reason"
            run_id: Run identifier

        Returns:
            Path to saved file (or None if no landlines)
        """
        if not landlines:
            return None

        path = self.fallback_dir / f"{run_id}_landlines.csv"

        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["name", "phone", "reason"])
            writer.writeheader()
            writer.writerows(landlines)

        return str(path)

    def save_invalid(self, invalid: list, run_id: str) -> str:
        """
        Save invalid data to CSV

        Args:
            invalid: List of dicts with customer data + "reason"
            run_id: Run identifier

        Returns:
            Path to saved file (or None if no invalid data)
        """
        if not invalid:
            return None

        path = self.fallback_dir / f"{run_id}_invalid.csv"

        # Get all unique keys from all dicts
        all_keys = set()
        for item in invalid:
            all_keys.update(item.keys())

        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=sorted(all_keys))
            writer.writeheader()
            writer.writerows(invalid)

        return str(path)

    def save_messages_csv(self, messages: list, run_id: str) -> str:
        """
        Save messages to CSV (human-readable)

        Args:
            messages: List of message dicts from N-Organ
            run_id: Run identifier

        Returns:
            Path to saved file
        """
        path = self.output_dir / f"{run_id}_messages.csv"

        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Header
            writer.writerow([
                "Timestamp",
                "Customer ID",
                "Customer Name",
                "Phone",
                "Message Body (Preview)",
                "Recommended Items",
                "Confidence",
                "Status"
            ])

            # Rows
            for msg in messages:
                # Extract customer name from body (first line)
                body = msg.get("body", "")
                customer_name = "Unknown"
                if body:
                    first_line = body.split('\n')[0]
                    # Remove "Hi " or "Hey " prefix
                    customer_name = first_line.replace("Hi ", "").replace("Hey ", "").replace("!", "").strip()

                writer.writerow([
                    datetime.now().isoformat(),
                    msg.get("customer_id", ""),
                    customer_name,
                    msg.get("to", ""),
                    (body[:150] + "...") if len(body) > 150 else body,  # Preview
                    ", ".join(msg.get("recommended_items", [])),
                    msg.get("confidence", ""),
                    "success" if body else "failed"
                ])

        return str(path)

    def save_messages_json(self, messages: list, run_id: str, metadata: dict = None) -> str:
        """
        Save messages to JSON (machine-readable)

        Args:
            messages: List of message dicts from N-Organ
            run_id: Run identifier
            metadata: Optional metadata from N-Organ response

        Returns:
            Path to saved file
        """
        path = self.output_dir / f"{run_id}_messages.json"

        data = {
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "total_messages": len(messages),
            "messages": messages,
            "metadata": metadata or {}
        }

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return str(path)

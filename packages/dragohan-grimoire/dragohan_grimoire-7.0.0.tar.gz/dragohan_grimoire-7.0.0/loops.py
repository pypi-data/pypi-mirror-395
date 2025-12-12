# Enhanced loops.py - Smart Universal Loop Library
"""
DragoHan's Enhanced Loop Mastery Library
Now handles ANY data structure - nested lists, dictionaries, mixed types, etc.

Enhanced Features:
- Deep nested structure traversal
- Auto-flattening of complex data
- Mixed data type handling
- Preserves original intelligent behavior
"""

from typing import Any, List, Union
import re


# Action functions for the new syntax
def save(format_str: str = "", data: Any = None):
    """
    Action creator for saving/creating files and folders.
    
    Uses the existing simple_file.save() function intelligently.
    
    Args:
        format_str: Format string (usually f"" for direct use)
        data: Data to save OR list of paths to create
    
    Examples:
        save(f"", folders)  # Create structure from folders list
        save("content", "file.txt")  # Save content to file
    """
    def action_func():
        return action_func
    action_func.__name__ = "save"
    if isinstance(data, list):
        action_func._params = {"items": data, "format": format_str}
    else:
        action_func._params = {"item": data, "format": format_str, "content": format_str}
    return action_func


def create(items: Any = "folders"):
    """Action creator for creating items.
    Accepts either:
    - a single string spec (e.g., "Question_1.py", "notes/", "file.py|notes/")
    - a list of string specs (e.g., folders list)
    """
    def action_func():
        return action_func
    action_func.__name__ = "create"
    if isinstance(items, list):
        action_func._params = {"items": items}
    else:
        action_func._params = {"item": items}
    return action_func


def delete(item_type: str = "files"):
    """Action creator for deleting items"""
    def action_func():
        return action_func
    action_func.__name__ = "delete"
    action_func._params = {"item": item_type}
    return action_func


def move(source: str, dest: str):
    """Action creator for moving items"""
    def action_func():
        return action_func
    action_func.__name__ = "move"
    action_func._params = {"source": source, "dest": dest}
    return action_func


def copy(source: str, dest: str):
    """Action creator for moving items"""
    def action_func():
        return action_func
    action_func.__name__ = "copy"
    action_func._params = {"source": source, "dest": dest}
    return action_func


class LoopOn:
    """
    Enhanced Universal loop extractor - handles ANY data structure
    """
    
    def __call__(self, times: int = None, action: Any = None, in_dir: str = None, 
                 data: Any = None, key: str = None, where: str = None, limit: int = None) -> List:
        """
        Enhanced Universal loop operator - FOUR MODES:
        
        MODE 1: Extract values (original) - now with deep traversal
            loopon(data, "key", where="filter")
        
        MODE 2: Extract from nested structures (NEW!)
            loopon(data, "key")  # Handles nested lists automatically
        
        MODE 3: Perform actions (NEW!)
            loopon(times=50, action=create("folders"), in_dir="base")
        
        MODE 4: Smart flatten and extract (NEW!)
            loopon(data, "base_stat")  # Auto-flattens complex nested data
        
        Args:
            times: Number of iterations OR len(data) for dynamic count
            action: Action to perform (create(), delete(), move(), copy())
            in_dir: Base directory for file operations
            data: List of items for extraction OR action items
            key: Key to extract (MODES 1,2,4)
            where: Filter condition (MODES 1,2,4)
            limit: Result limit (MODES 1,2,4)
        
        Returns:
            List of results (extracted values OR action results)
        """
        # MODE 3: Action mode
        if action is not None:
            return self._action_mode(data, times, action, in_dir)
        
        # MODES 1,2,4: Enhanced extraction mode with smart nesting handling
        return self._smart_extraction_mode(data, key, where, limit)
    
    def _smart_extraction_mode(self, data: Any, key: str, where: str = None, limit: int = None) -> List:
        """
        ENHANCED extraction mode with deep nested structure handling
        """
        # Handle MageJSON objects
        if hasattr(data, 'raw'):
            data = data.raw
        
        # NEW: Auto-detect and handle ANY data structure
        if data is None:
            return []
        
        # Smart flattening and extraction
        flattened_items = self._flatten_for_extraction(data)
        
        # Original extraction logic on flattened data
        values = []
        for item in flattened_items:
            if not isinstance(item, dict) or item.get('error'):
                continue
            
            extracted = self._extract_value(item, key)
            
            if extracted is not None:
                # Handle multiple values per item (e.g., dual-types)
                if isinstance(extracted, list):
                    values.extend(extracted)
                else:
                    values.append(extracted)
        
        # Apply filter if specified
        if where:
            values = self._filter_values(values, where)
        
        # Apply limit if specified
        if limit:
            values = values[:limit]
        
        return values
    
    def _flatten_for_extraction(self, data: Any, depth: int = 0) -> List:
        """
        NEW: Smart flattening for extraction - handles ANY data structure
        
        Examples:
        - [dict1, dict2] → [dict1, dict2]  # Original behavior
        - [[dict1, dict2], [dict3, dict4]] → [dict1, dict2, dict3, dict4]  # Nested lists
        - [{nested: [dict1, dict2]}] → [dict1, dict2]  # Nested dictionaries
        - Mixed structures → properly extracted dictionaries
        """
        if depth > 100:  # Prevent infinite recursion
            return []
        
        # If it's already a list of dicts, return as-is
        if isinstance(data, list) and data and isinstance(data[0], dict):
            return data
        
        # If it's a single dict, return in list
        if isinstance(data, dict):
            return [data]
        
        # If it's a list, process each item
        if isinstance(data, list):
            results = []
            for item in data:
                flattened = self._flatten_for_extraction(item, depth + 1)
                if isinstance(flattened, list):
                    results.extend(flattened)
                else:
                    results.append(flattened)
            return results
        
        # If it's a dict with lists inside, process the lists
        if isinstance(data, dict):
            results = []
            for value in data.values():
                if isinstance(value, list):
                    flattened = self._flatten_for_extraction(value, depth + 1)
                    if isinstance(flattened, list):
                        results.extend(flattened)
                    else:
                        results.append(flattened)
            return results
        
        # For other types, return empty list
        return []
    
    def _action_mode(self, data: Any, times: int, action: Any, in_dir: str) -> List:
        """
        ACTION MODE - Perform operations on items
        
        Smart actions:
        - create("folders"): Create directories/files
        - delete("files"): Remove files/folders
        - move("source", "dest"): Move/rename items
        - copy("source", "dest"): Copy items
        """
        from simple_file import exists, save, load
        
        results = []
        
        # Extract action type and parameters
        if hasattr(action, '__call__'):
            # It's a function like create("folders")
            action_type = action.__name__
            action_params = getattr(action, '_params', {})
        elif isinstance(action, str):
            # Simple string action
            action_type = action
            action_params = {}
        else:
            return ["Invalid action format"]
        
        # Determine items to operate on (precedence: explicit data > action items > times filler > single param)
        if isinstance(data, list):
            items = data
        elif 'items' in action_params and isinstance(action_params['items'], list):
            items = action_params['items']
        elif times is not None:
            if callable(times):
                times = times(data) if data else 1
            items = [action_params.get('item', '')] * int(times)
        else:
            items = [action_params.get('item', '')]
        
        for item in items:
            if action_type == "save":
                result = self._smart_save(item, in_dir, action_params)
            elif action_type == "create":
                result = self._smart_create(item, in_dir, action_params)
            elif action_type == "delete":
                result = self._smart_delete(item, in_dir)
            elif action_type == "move":
                result = self._smart_move(item, in_dir)
            elif action_type == "copy":
                result = self._smart_copy(item, in_dir)
            else:
                result = f"Unknown action: {action_type}"
            
            results.append(result)
        
        return results
    
    def _smart_save(self, item: Any, in_dir: str = None, action_params: dict = {}) -> str:
        """
        SMART SAVE - Intelligent file/folder creation using simple_file.save()
        
        SMART LOGIC for patterns like "Question_1.py/notes":
        1. Detect: file.ext/subfolder pattern
        2. Create: Question_1/ directory
        3. Inside: Question_1.py file + notes/ directory
        
        Examples:
        - "Question_1.py/notes" → Question_1/Question_1.py + Question_1/notes/
        - "file.py" → file.py (simple file)
        - "folder/" → folder/ (simple directory)
        """
        from simple_file import save as sf_save, exists
        from pathlib import Path
        import os
        
        if not item or item == '':
            return "Empty item"
        
        # Build full base path (handles nested like "Advanced question/data")
        base_path = in_dir if in_dir else ""
        
        # Ensure base path exists first - use Path.mkdir() for directories
        if base_path and not exists(base_path):
            Path(base_path).mkdir(parents=True, exist_ok=True)
        
        # SMART DETECTION: file.ext/subfolder pattern
        # Example: "Question_1.py/notes" means create Question_1/ with Question_1.py and notes/ inside
        if '/' in item and not item.endswith('/'):
            parts = item.split('/')
            
            # Check if first part is a file (has extension)
            first_part = parts[0]
            if '.' in first_part:
                # Extract filename without extension for folder name
                file_name = first_part
                folder_name = os.path.splitext(file_name)[0]
                
                # Build paths
                main_folder = f"{base_path}/{folder_name}" if base_path else folder_name
                file_path = f"{main_folder}/{file_name}"
                
                results = []
                
                # Create main folder
                if not exists(main_folder):
                    Path(main_folder).mkdir(parents=True, exist_ok=True)
                    results.append(f"Created: {main_folder}/")
                
                # Create the file inside
                if not exists(file_path):
                    # Determine file content based on extension
                    ext = os.path.splitext(file_name)[1].lower()
                    if ext == '.py':
                        content = f"# {file_name}\n\n"
                    elif ext == '.json':
                        content = "{}"
                    elif ext == '.md':
                        content = f"# {folder_name}\n\n"
                    else:
                        content = ""
                    
                    sf_save(file_path, content)
                    results.append(f"Created: {file_path}")
                
                # Create remaining subfolders
                for i in range(1, len(parts)):
                    subfolder = parts[i]
                    if not subfolder.endswith('/'):
                        subfolder += '/'
                    
                    subfolder_path = f"{main_folder}/{subfolder}"
                    if not exists(subfolder_path):
                        Path(subfolder_path).mkdir(parents=True, exist_ok=True)
                        results.append(f"Created: {subfolder_path}")
                
                return " | ".join(results)
        
        # Simple case: just a file or folder
        full_path = f"{base_path}/{item}" if base_path else item
        
        if exists(full_path):
            return f"Already exists: {full_path}"
        
        # Determine what to create
        if item.endswith('/'):
            # Directory
            Path(full_path).mkdir(parents=True, exist_ok=True)
            return f"Created directory: {full_path}"
        elif '.' in os.path.basename(item):
            # File with extension
            ext = os.path.splitext(item)[1].lower()
            if ext == '.py':
                content = f"# {os.path.basename(item)}\n\n"
            elif ext == '.json':
                content = "{}"
            elif ext == '.md':
                content = f"# {os.path.splitext(os.path.basename(item))[0]}\n\n"
            else:
                content = ""
            
            sf_save(full_path, content)
            return f"Created file: {full_path}"
        else:
            # No extension, assume directory
            Path(full_path).mkdir(parents=True, exist_ok=True)
            return f"Created directory: {full_path}"
    
    def _smart_create(self, item: Any, base_path: str = None, action_params: dict = {}) -> str:
        """
        SMART CREATE - Auto-detect what to create based on item content
        
        Handles:
        - String paths: Creates directories or files based on extension
        - Dict data: Creates files with content
        - Existing templates: Copies and adapts structure
        """
        from simple_file import exists, save, load
        import os
        
        if item is None:
            return "No item to create"
        
        # If item is a string path
        if isinstance(item, str):
            return self._create_from_path(item, base_path)
        
        # If item is a dict with file info
        elif isinstance(item, dict):
            return self._create_from_dict(item, base_path)
        
        else:
            return f"Cannot create from {type(item)}"
    
    def _create_from_path(self, path: str, base_path: str = None) -> str:
        """
        Create from path string - SMART AUTO-DETECTION
        
        Examples:
        - "folder/" -> creates directory
        - "file.py" -> creates Python file
        - "data.json" -> creates JSON file
        - "folder/subfolder/" -> creates nested directories
        """
        from simple_file import exists, save
        import os
        
        # Support sibling specs separated by '|', e.g., "file.py|notes/"
        if '|' in path:
            parts = [p.strip() for p in path.split('|') if p.strip()]
            messages = []
            for part in parts:
                messages.append(self._create_from_path(part, base_path))
            return " | ".join(messages)

        # Add base path if provided
        full_path = f"{base_path}/{path}" if base_path else path
        
        # Check if already exists
        if exists(full_path):
            return f"Already exists: {full_path}"
        
        # SMART DETECTION
        if path.endswith("/"):
            # Directory creation
            save(full_path, "")
            return f"Created directory: {full_path}"
        
        elif "." in os.path.basename(path):
            # File creation - detect type by extension
            ext = os.path.basename(path).split(".")[-1].lower()
            
            if ext == "py":
                content = "# Python file\n\n"
            elif ext == "json":
                content = "{}"
            elif ext == "txt":
                content = ""
            elif ext == "md":
                content = "# Markdown file\n\n"
            else:
                content = ""
            
            save(full_path, content)
            return f"Created {ext} file: {full_path}"
        
        else:
            # No extension and no trailing slash - assume directory
            save(full_path, "")
            return f"Created directory: {full_path}"
    
    def _create_from_dict(self, item: dict, base_path: str = None) -> str:
        """
        Create from dict specification
        
        Dict format:
        {
            "path": "file.py",
            "content": "print('hello')",
            "type": "file"  # optional
        }
        """
        from simple_file import exists, save
        
        path = item.get("path", "")
        content = item.get("content", "")
        item_type = item.get("type", "file")
        
        full_path = f"{base_path}/{path}" if base_path else path
        
        if exists(full_path):
            return f"Already exists: {full_path}"
        
        if item_type == "directory" or path.endswith("/"):
            save(full_path, "")
            return f"Created directory: {full_path}"
        else:
            save(full_path, content)
            return f"Created file: {full_path}"
    
    def _smart_delete(self, item: Any, base_path: str = None) -> str:
        """Smart delete - placeholder for now"""
        return f"Delete not implemented for: {item}"
    
    def _smart_move(self, item: Any, base_path: str = None) -> str:
        """Smart move - placeholder for now"""
        return f"Move not implemented for: {item}"
    
    def _smart_copy(self, item: Any, base_path: str = None) -> str:
        """Smart copy - placeholder for now"""
        return f"Copy not implemented for: {item}"
    
    def _extraction_mode(self, data: Any, key: str, where: str = None, limit: int = None) -> List:
        """
        Original extraction mode - extract values from data structures
        """
        # Handle MageJSON objects
        if hasattr(data, 'raw'):
            data = data.raw
        
        if not isinstance(data, list):
            return []
        
        # Extract all values for the key
        values = []
        for item in data:
            if not isinstance(item, dict) or item.get('error'):
                continue
            
            extracted = self._extract_value(item, key)
            
            if extracted is not None:
                # Handle multiple values per item (e.g., dual-types)
                if isinstance(extracted, list):
                    values.extend(extracted)
                else:
                    values.append(extracted)
        
        # Apply filter if specified
        if where:
            values = self._filter_values(values, where)
        
        # Apply limit if specified
        if limit:
            values = values[:limit]
        
        return values
    
    def sorta(self, data: Any, key: str, where: str = None, limit: int = None) -> List:
        """
        Extract and sort ASCENDING
        
        Usage:
            loopon.sorta(data, "weight")
            loopon.sorta(data, "weight", where=">100")
            loopon.sorta(data, "weight", limit=5)
        """
        values = self(data, key, where=where, limit=None)  # Get all first
        
        try:
            values = sorted(values)  # Sort ascending
        except TypeError:
            pass  # Can't sort mixed types
        
        # Apply limit after sorting
        if limit:
            values = values[:limit]
        
        return values
    
    def sortd(self, data: Any, key: str, where: str = None, limit: int = None) -> List:
        """
        Extract and sort DESCENDING
        
        Usage:
            loopon.sortd(data, "weight")
            loopon.sortd(data, "weight", where=">100")
            loopon.sortd(data, "weight", limit=5)
        """
        values = self(data, key, where=where, limit=None)  # Get all first
        
        try:
            values = sorted(values, reverse=True)  # Sort descending
        except TypeError:
            pass  # Can't sort mixed types
        
        # Apply limit after sorting
        if limit:
            values = values[:limit]
        
        return values
    
    def _extract_value(self, obj: dict, search_key: str, depth: int = 0) -> Any:
        """
        Extract value from nested structure
        
        Handles:
        - Direct: obj[key]
        - Nested: obj[key].name
        - Plural: obj[keys][].key.name
        """
        if depth > 50 or not isinstance(obj, dict):
            return None
        
        # PATTERN 1: Direct access
        if search_key in obj:
            val = obj[search_key]
            if not isinstance(val, (dict, list)):
                return val
            if isinstance(val, dict):
                if 'name' in val:
                    return val['name']
                if 'value' in val:
                    return val['value']
            return val
        
        # PATTERN 2: Plural array
        plural_key = search_key + 's'
        if plural_key in obj and isinstance(obj[plural_key], list):
            values = []
            for item in obj[plural_key]:
                if isinstance(item, dict) and search_key in item:
                    nested = item[search_key]
                    if isinstance(nested, dict):
                        if 'name' in nested:
                            values.append(nested['name'])
                        elif 'value' in nested:
                            values.append(nested['value'])
                    else:
                        values.append(nested)
            
            if len(values) > 1:
                return values
            elif len(values) == 1:
                return values[0]
        
        # PATTERN 3: Recursive search
        for key, val in obj.items():
            if isinstance(val, dict):
                result = self._extract_value(val, search_key, depth + 1)
                if result is not None:
                    return result
            elif isinstance(val, list):
                for list_item in val:
                    if isinstance(list_item, dict):
                        result = self._extract_value(list_item, search_key, depth + 1)
                        if result is not None:
                            return result
        
        return None
    
    def _filter_values(self, values: List, condition: str) -> List:
        """
        Filter values based on condition
        
        Supports:
        - "fire" (equals)
        - ">100" (greater than)
        - ">=100" (greater or equal)
        - "<50" (less than)
        - "<=50" (less or equal)
        - "!=water" (not equal)
        """
        # Parse operator and value
        operator, compare_value = self._parse_condition(condition)
        
        filtered = []
        for value in values:
            if self._compare(value, operator, compare_value):
                filtered.append(value)
        
        return filtered
    
    def _parse_condition(self, condition: str) -> tuple:
        """Parse condition into operator and value"""
        condition = str(condition).strip()
        
        # Check for operators
        if condition.startswith('>='):
            return '>=', self._convert_value(condition[2:].strip())
        elif condition.startswith('<='):
            return '<=', self._convert_value(condition[2:].strip())
        elif condition.startswith('!='):
            return '!=', self._convert_value(condition[2:].strip())
        elif condition.startswith('>'):
            return '>', self._convert_value(condition[1:].strip())
        elif condition.startswith('<'):
            return '<', self._convert_value(condition[1:].strip())
        else:
            # No operator = equals
            return '==', self._convert_value(condition)
    
    def _convert_value(self, value_str: str) -> Any:
        """Convert string to appropriate type"""
        value_str = value_str.strip()
        
        # Try to convert to number
        try:
            if '.' in value_str:
                return float(value_str)
            else:
                return int(value_str)
        except ValueError:
            return value_str
    
    def _compare(self, value: Any, operator: str, compare_value: Any) -> bool:
        """Compare value with condition"""
        try:
            if operator == '==':
                return value == compare_value
            elif operator == '!=':
                return value != compare_value
            elif operator == '>':
                return value > compare_value
            elif operator == '<':
                return value < compare_value
            elif operator == '>=':
                return value >= compare_value
            elif operator == '<=':
                return value <= compare_value
            else:
                return value == compare_value
        except (TypeError, ValueError):
            return False


def loopon_and_get(data: Any, key: str, where: str = None, limit: int = None) -> List:
    """
    Get FULL ITEMS where key matches condition
    
    Usage:
        fire_pokemon = loopon_and_get(data, "type", where="fire")
        heavy = loopon_and_get(data, "weight", where=">100")
    
    Args:
        data: List of dicts or MageJSON object
        key: Key to filter by
        where: Condition (e.g., "fire", ">100")
        limit: Optional limit
    
    Returns:
        List of full items (dicts)
    """
    # Handle MageJSON objects
    if hasattr(data, 'raw'):
        data = data.raw
    
    if not isinstance(data, list):
        return []
    
    results = []
    
    for item in data:
        if not isinstance(item, dict) or item.get('error'):
            continue
        
        # Extract value for this item
        extracted = loopon._extract_value(item, key)
        
        if extracted is None:
            continue
        
        # If where condition specified, check it
        if where:
            # Handle multiple values (e.g., dual-types)
            if isinstance(extracted, list):
                # Check if ANY value matches
                matches = False
                for val in extracted:
                    if loopon._compare(val, *loopon._parse_condition(where)):
                        matches = True
                        break
                if not matches:
                    continue
            else:
                # Single value - check directly
                if not loopon._compare(extracted, *loopon._parse_condition(where)):
                    continue
        
        results.append(item)
    
    # Apply limit
    if limit:
        results = results[:limit]
    
    return results


# Create singleton instance
loopon = LoopOn()

# Export everything
__all__ = ['loopon', 'loopon_and_get', 'save', 'create', 'delete', 'move', 'copy']


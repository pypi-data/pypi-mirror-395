# simple_file.py - Your File Handling Servant Army

from pathlib import Path
import json
import shutil
from datetime import datetime
from typing import Any, Union


class _FileMage:
    """
    Internal mage class - users don't need to touch this
    """
    
    def __init__(self, folder: str = '.'):
        self.folder = Path(folder)
        self.folder.mkdir(parents=True, exist_ok=True)
    
    def save(self, name: str, data: Any = None):
        """Save ANYTHING - figures out format automatically"""
        if '.' not in name:
            if isinstance(data, (dict, list)):
                name = f"{name}.json"
            else:
                name = f"{name}.txt"
        
        filepath = self.folder / name
        
        if name.endswith('.json'):
            if data is None:
                data = {}
            
            # Handle MageJSON objects - unwrap them before JSON serialization
            try:
                if hasattr(data, 'raw'):
                    data = data.raw
                elif isinstance(data, list):
                    # Unwrap any MageJSON objects in lists
                    data = [item.raw if hasattr(item, 'raw') else item for item in data]
                elif isinstance(data, dict):
                    # Unwrap any MageJSON objects in dictionaries
                    data = {k: v.raw if hasattr(v, 'raw') else v for k, v in data.items()}
            except Exception:
                pass  # If unwrapping fails, proceed with original data
            
            filepath.write_text(json.dumps(data, indent=2))
        else:
            if data is None:
                data = ""
            filepath.write_text(str(data))
        
        return f"✅ Saved: {name}"
    
    def load(self, name: str) -> Any:
        """Load ANYTHING - figures out format automatically"""
        if '.' not in name:
            for ext in ['.json', '.txt']:
                if (self.folder / f"{name}{ext}").exists():
                    name = f"{name}{ext}"
                    break
        
        filepath = self.folder / name
        
        if not filepath.exists():
            return f"❌ File not found: {name}"
        
        if name.endswith('.json'):
            return json.loads(filepath.read_text())
        else:
            return filepath.read_text()
    
    def delete(self, name: str):
        """Delete file or folder"""
        if '.' not in name:
            for ext in ['.json', '.txt', '']:
                path = self.folder / f"{name}{ext}"
                if path.exists():
                    if path.is_file():
                        path.unlink()
                    else:
                        shutil.rmtree(path)
                    return f"✅ Deleted: {name}{ext}"
        else:
            path = self.folder / name
            if path.exists():
                if path.is_file():
                    path.unlink()
                else:
                    shutil.rmtree(path)
                return f"✅ Deleted: {name}"
        
        return f"❌ Not found: {name}"
    
    def rewrite(self, name: str, data: Any):
        """Rewrite file (delete old, write new)"""
        return self.save(name, data)
    
    def add(self, name: str, data: str):
        """Add to end of file"""
        if '.' not in name:
            name = f"{name}.txt"
        
        filepath = self.folder / name
        
        with open(filepath, 'a') as f:
            f.write(str(data) + '\n')
        
        return f"✅ Added to: {name}"
    
    def exists(self, name: str) -> bool:
        """Check if file exists"""
        if '.' not in name:
            for ext in ['.json', '.txt']:
                if (self.folder / f"{name}{ext}").exists():
                    return True
            return False
        
        return (self.folder / name).exists()
    
    def list(self, pattern: str = '*'):
        """List all files"""
        files = [f.name for f in self.folder.glob(pattern) if f.is_file()]
        return files
    
    def quick_save(self, data: Any, prefix: str = 'data'):
        """Save with automatic timestamp name"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        name = f"{prefix}_{timestamp}"
        return self.save(name, data)
    
    def backup(self, name: str):
        """Create backup of file"""
        if not self.exists(name):
            return f"❌ File not found: {name}"
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_name = name.split('.')[0]
        ext = '.' + name.split('.')[-1] if '.' in name else ''
        backup_name = f"{base_name}_backup_{timestamp}{ext}"
        
        shutil.copy(self.folder / name, self.folder / backup_name)
        return f"✅ Backed up: {backup_name}"


# === GLOBAL MAGE INSTANCE ===
_global_mage = _FileMage()


# === SERVANT FUNCTIONS (Your Army) ===

def save(name: str, data: Any = None, folder: str = '.'):
    """Save anything - automatically handles format"""
    mage = _FileMage(folder) if folder != '.' else _global_mage
    return mage.save(name, data)


def load(name: str, folder: str = '.'):
    """Load anything - automatically handles format"""
    mage = _FileMage(folder) if folder != '.' else _global_mage
    return mage.load(name)


def delete(name: str, folder: str = '.'):
    """Delete file"""
    mage = _FileMage(folder) if folder != '.' else _global_mage
    return mage.delete(name)


def rewrite(name: str, data: Any, folder: str = '.'):
    """Rewrite file"""
    mage = _FileMage(folder) if folder != '.' else _global_mage
    return mage.rewrite(name, data)


def add(name: str, data: str, folder: str = '.'):
    """Append to file"""
    mage = _FileMage(folder) if folder != '.' else _global_mage
    return mage.add(name, data)


def exists(name: str, folder: str = '.') -> bool:
    """Check if file exists"""
    mage = _FileMage(folder) if folder != '.' else _global_mage
    return mage.exists(name)


def list_files(pattern: str = '*', folder: str = '.'):
    """List files"""
    mage = _FileMage(folder) if folder != '.' else _global_mage
    return mage.list(pattern)


def quick_save(data: Any, prefix: str = 'data', folder: str = '.'):
    """Save with auto timestamp"""
    mage = _FileMage(folder) if folder != '.' else _global_mage
    return mage.quick_save(data, prefix)


def backup(name: str, folder: str = '.'):
    """Create backup"""
    mage = _FileMage(folder) if folder != '.' else _global_mage
    return mage.backup(name)


# === THE MAGIC BANNER ===
def _show_banner():
    """Display the summoning banner"""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🔥 SIMPLE_FILE SUMMONED 🔥                                  ║
║                                                               ║
║   Your Servant Army is Ready:                                ║
║   ├─ save()        → Save any file automatically             ║
║   ├─ load()        → Load any file automatically             ║
║   ├─ delete()      → Delete files/folders                    ║
║   ├─ rewrite()     → Overwrite file content                  ║
║   ├─ add()         → Append to file                          ║
║   ├─ exists()      → Check if file exists                    ║
║   ├─ list_files()  → List all files                          ║
║   ├─ quick_save()  → Save with timestamp                     ║
║   └─ backup()      → Create file backup                      ║
║                                                               ║
║   Example: save('config', {'key': 'value'})                  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


# Show banner on import
_show_banner()


# Export everything
__all__ = [
    'save', 'load', 'delete', 'rewrite', 'add', 
    'exists', 'list_files', 'quick_save', 'backup'
]


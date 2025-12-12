"""
💀 MONARCH REGISTRY SYSTEM 💀
Agent registration and discovery
"""

from typing import Dict, Type

_MONARCH_REGISTRY: Dict[str, Type] = {}

def register_monarch(name: str):
    """
    💀 Decorator to register a Shadow Monarch 💀
    
    Usage:
        @register_monarch("lead")
        class LeadMonarch(MonarchBase):
            pass
    """
    def decorator(cls: Type):
        if name in _MONARCH_REGISTRY:
            print(f"⚠️  WARNING: Monarch '{name}' already registered, overwriting...")
        _MONARCH_REGISTRY[name] = cls
        print(f"💀 Registered Shadow Monarch: '{name}' → {cls.__name__}")
        return cls
    return decorator


def get_monarch_class(name: str):
    """Get monarch class by name"""
    return _MONARCH_REGISTRY.get(name)


def list_monarchs():
    """List all registered shadow monarchs"""
    return list(_MONARCH_REGISTRY.keys())

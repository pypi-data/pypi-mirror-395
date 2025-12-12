"""
💀 SYSTEM REGISTRY - Ultra Simple 💀
"""

# Global registry
_SYSTEMS = {}


def register_system(name: str):
    """
    💀 REGISTER A SYSTEM 💀
    
    Usage:
        @register_system("data")
        class DataSystem(SystemBase):
            ...
    """
    def decorator(cls):
        _SYSTEMS[name] = cls
        print(f"   💀 System registered: {name} → {cls.__name__}")
        return cls
    return decorator


def get_system_class(name: str):
    """Get system class by name"""
    return _SYSTEMS.get(name)


def list_systems():
    """List all registered systems"""
    return list(_SYSTEMS.keys())

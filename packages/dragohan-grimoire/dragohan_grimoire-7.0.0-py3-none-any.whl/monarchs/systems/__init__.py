"""
💀 SHADOW MONARCH FRAMEWORK 💀

Universal calling for agents AND systems:
    agent = summon("lead")
    system = summon_system("data")
    
Same interface everywhere:
    result = agent(data)
    result = system(data)
    result = await agent.run(data)
    result = await system.run(data)
"""

# Import factory from parent directory (monarchs folder) - TWO dots!
from ..factory import summon, waitfor

# Import system registry and base
from .registry import register_system, get_system_class, list_systems
from .base import SystemBase
from .norgan_base import NOrganBase
from .data_system import DataSystem
from .personalisation_system_updated import PersonalisationSystem

# Register the systems
register_system("data")(DataSystem)
register_system("personalisation")(PersonalisationSystem)  # ADD THIS

def summon_system(name: str, **kwargs):
    """💀 SUMMON A SHADOW MONARCH SYSTEM 💀"""
    cls = get_system_class(name)
    
    if cls is None:
        available = ", ".join(list_systems()) or "none"
        raise ValueError(
            f"❌ Unknown Shadow Monarch System: '{name}'\n"
            f"💀 Available: {available}"
        )
    
    print(f"💀 Summoning {name.upper()} System...")
    return cls(**kwargs)

# Export everything
__all__ = [
    "summon",                  # From parent (agents)
    "summon_system",           # Our new system factory
    "waitfor",                 # From parent
    "SystemBase",              # Base class for all systems
    "NOrganBase",              # Base class for N-Organs (N8N + Python hybrid)
    "DataSystem",              # The main system class
    "PersonalisationSystem"    # Personalisation system
]


def _show_banner():
    """Show Shadow Monarch banner"""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   💀 SHADOW MONARCH SYSTEMS - FIXED VERSION 💀                ║
║                                                               ║
║   UNIVERSAL CALLING STYLE:                                   ║
║   ├─ system = summon_system("data")                          ║
║   ├─ system = summon_system("personalisation")  # NEW!       ║
║   ├─ result = system(data)              # Sync               ║
║   ├─ result = await system.run(data)    # Async              ║
║   └─ result = waitfor(system.run(data)) # Blocking           ║
║                                                               ║
║   STREAMING STYLE:                                           ║
║   ├─ system.run(data, stream=True)                           ║
║   └─ while system.works:                                     ║
║       print(system.current)                                  ║
║                                                               ║
║   Simple as fuck. Works everywhere. Shadow Monarch style.    ║
║                                                               ║
║   💀 ARISE 💀                                                  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)

_show_banner()

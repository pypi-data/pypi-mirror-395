"""
💀 SHADOW MONARCH SYSTEM + ORGAN SYSTEMS 💀
Unified initialization for:
- Agents (lead/data/ops)
- Systems (data system, business system, etc.)
"""

# ---------------------------
# Step 1: Import agent registry first
# ---------------------------
from .registry import register_monarch

# ---------------------------
# Step 2: Import agent factory
# ---------------------------
from .factory import summon, waitfor

# ---------------------------
# Step 3: Import monarchs (agents)
# These trigger @register_monarch decorators
# ---------------------------
from . import lead
from . import data
from . import restaurant

# ---------------------------
# Step 4: Import Organ Systems
# ---------------------------
from .systems import summon_system

# ---------------------------
# Step 5: Import N-Organs
# ---------------------------
from .norgans import summon_norgan, norgans_ls

# ---------------------------
# Step 6: Exports
# ---------------------------
__all__ = [
    "summon",            # Agent summoning
    "summon_system",     # System summoning
    "summon_norgan",     # N-Organ summoning
    "norgans_ls",        # List N-Organs
    "waitfor",
    "register_monarch"
]

# ---------------------------
# Step 7: Shadow Banner
# ---------------------------
def _show_banner():
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   💀 SHADOW MONARCH SYSTEM AWAKENED 💀                        ║
║   Agents + Organ Systems + N-Organs Ready                     ║
║                                                               ║
║   Your Shadow Army Stands Ready:                             ║
║   ├─ summon("lead")        → Lead Enrichment Monarch          ║
║   ├─ summon("data")        → Data Analysis Monarch            ║
║   ├─ summon("ops")         → Operations Monarch               ║
║                                                               ║
║   Your Organ Systems Stand Ready:                             ║
║   ├─ summon_system("data") → Data Orchestration System        ║
║   ├─ summon_system("personalisation") → Personalisation       ║
║   └─ summon_system(...)    → More systems soon…               ║
║                                                               ║
║   Your N-Organs Stand Ready:                                  ║
║   ├─ summon_norgan("hp")   → Hyper Personalisation N-Organ   ║
║   ├─ norgans_ls()          → List all N-Organs                ║
║   └─ organ.run(...)        → Process with Railway             ║
║                                                               ║
║   Commands of Power:                                          ║
║   ├─ await agent.action()          → Async execution          ║
║   ├─ waitfor(agent.action())       → Blocking sync            ║
║   ├─ system(data)                  → Single-call pipeline     ║
║   ├─ while system.works: ...        → Streaming mode          ║
║                                                               ║
║   The weak code alone. The strong code with agents + systems. ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""
    print(banner)

_show_banner()

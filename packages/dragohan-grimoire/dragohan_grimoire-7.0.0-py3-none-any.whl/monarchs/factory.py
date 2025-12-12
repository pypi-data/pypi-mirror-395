"""
💀 MONARCH FACTORY & SUMMON SYSTEM 💀
FIXED: Direct imports instead of package imports
"""

import asyncio
from typing import Dict, Any, Optional
from .registry import get_monarch_class, list_monarchs


def waitfor(coro):
    """💀 DragoHan's Sync Wrapper 💀"""
    try:
        loop = asyncio.get_running_loop()
        raise RuntimeError(
            "❌ Cannot use waitfor() inside async context!\n"
            "💀 Use: await agent.enrich(data)\n"
            "    NOT: waitfor(agent.enrich(data))"
        )
    except RuntimeError as e:
        if "no running event loop" in str(e).lower():
            return asyncio.run(coro)
        else:
            raise


def build_default_tools() -> Dict[str, Any]:
    """💀 AUTO-INJECT ALL GRIMOIRE TOOLS 💀"""
    # FIXED: Direct imports
    import brain
    import json_mage
    import simple_file
    import duplicate_tools as duplicates
    import experience
    from internet import getter
    
    tools = {
        "brain": brain.Brain,
        "experience": experience.Experience,
        "json": json_mage,
        "files": simple_file,
        "web": getter,
        "dupes": duplicates,
    }
    
    print("💀 Tools loaded: brain, json, files, web, dupes, experience")
    return tools


def summon(name: str, industry: Optional[str] = None, **kwargs):
    """💀 SUMMON A SHADOW MONARCH 💀"""
    cls = get_monarch_class(name)
    
    if cls is None:
        available = ", ".join(list_monarchs()) or "none"
        raise ValueError(
            f"❌ Unknown Shadow Monarch: '{name}'\n"
            f"💀 Available: {available}"
        )
    
    tools = build_default_tools()
    
    print(f"💀 Summoning {name.upper()} Shadow Monarch...")
    if industry:
        print(f"   Industry: {industry}")
    
    return cls(tools=tools, industry=industry, **kwargs)

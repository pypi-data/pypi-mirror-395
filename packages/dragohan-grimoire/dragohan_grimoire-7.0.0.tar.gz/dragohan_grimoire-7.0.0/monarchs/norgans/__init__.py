"""
💀 N-ORGAN SUMMONING SYSTEM 💀

N-Organs = N8N + Python hybrid systems
- N8N handles I/O (database, APIs, scheduling)
- Python handles AI logic (recommendations, generation)
- Always remote (HTTP calls to Railway deployment)

Usage:
    organ = summon_norgan("hp")  # or "hyper_personalisation"
    result = organ.run(customers=data, menu=data)
"""

import httpx
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime

# Import helpers
from .helpers import NOrganHelpers

# Registry
_NORGANS = {}
_NORGAN_URLS = {}
_NORGAN_ALIASES = {}


def register_norgan(name: str, alias: str = None, url: str = None):
    """
    Register N-Organ with optional alias and URL

    Usage:
        @register_norgan("hyper_personalisation", alias="hp", url="https://...")
        class PersonalisationNOrgan:
            pass
    """
    def decorator(cls):
        _NORGANS[name] = cls
        if alias:
            _NORGAN_ALIASES[alias] = name
        if url:
            _NORGAN_URLS[name] = url
        print(f"   💀 N-Organ registered: {name} (alias: {alias})")
        return cls
    return decorator


def summon_norgan(name: str, url: str = None, **kwargs):
    """
    💀 SUMMON AN N-ORGAN 💀

    Args:
        name: N-Organ name or alias ("hp" or "hyper_personalisation")
        url: Override Railway URL (optional)
        **kwargs: Additional config

    Returns:
        NOrganProxy: Callable N-Organ interface

    Example:
        organ = summon_norgan("hp")
        result = organ.run(customers=data, menu=data)
    """
    # Resolve alias to full name
    full_name = _NORGAN_ALIASES.get(name, name)

    # Get N-Organ class
    cls = _NORGANS.get(full_name)
    if cls is None:
        available = list(_NORGANS.keys())
        aliases = [f"{k} ({v})" for k, v in _NORGAN_ALIASES.items()]
        raise ValueError(
            f"❌ Unknown N-Organ: '{name}'\n"
            f"💀 Available: {', '.join(available)}\n"
            f"💀 Aliases: {', '.join(aliases)}"
        )

    # Get URL (override or default)
    norgan_url = url or _NORGAN_URLS.get(full_name)
    if not norgan_url:
        raise ValueError(f"❌ No URL configured for N-Organ '{full_name}'")

    print(f"💀 Summoning {full_name.upper()} N-Organ...")
    print(f"   📡 Endpoint: {norgan_url}")

    return NOrganProxy(full_name, norgan_url, **kwargs)


def norgans_ls():
    """List all available N-Organs with aliases"""
    result = []
    for name in _NORGANS.keys():
        aliases = [k for k, v in _NORGAN_ALIASES.items() if v == name]
        alias_str = f" (alias: {', '.join(aliases)})" if aliases else ""
        result.append(f"{name}{alias_str}")
    return result


class NOrganProxy:
    """
    Proxy for calling remote N-Organs via HTTP

    Handles:
    - HTTP POST to Railway endpoint
    - Auto-formatting data
    - Helper integration (validation, mapping)
    - Fallback file generation (landlines, invalid)
    - Output file saving (CSV + JSON)
    """

    def __init__(self, name: str, url: str, **kwargs):
        self.name = name
        self.url = url
        self.config = kwargs
        self.helpers = NOrganHelpers()  # Global helpers

    async def run(self, customers=None, menu=None, **kwargs):
        """
        Main processing method

        Automatically:
        1. Validates and cleans data (using helpers)
        2. Sends to Railway N-Organ
        3. Saves fallback files (landlines, invalid)
        4. Saves success files (CSV + JSON)
        5. Returns result summary

        Args:
            customers: List of customer dicts (any format)
            menu: List of menu item dicts (any format)
            **kwargs: Additional parameters to pass to N-Organ

        Returns:
            {
                "messages": [...],
                "run_id": "...",
                "fallback_files": {"landlines": "...", "invalid": "..."},
                "output_files": {"csv": "...", "json": "..."},
                "pre_validation_stats": {...},
                ... (other N-Organ response fields)
            }
        """

        print(f"\n💀 Processing data with {self.name.upper()} N-Organ...")

        # Step 1: Process customers with helpers
        print("   🔍 Validating customers...")
        processed = self.helpers.process_customers(customers or [])

        valid_customers = processed["valid"]
        landlines = processed["landlines"]
        invalid = processed["invalid"]

        print(f"   ✅ Valid: {len(valid_customers)}")
        print(f"   📞 Landlines: {len(landlines)}")
        print(f"   ❌ Invalid: {len(invalid)}")

        # Step 2: Process menu items with helpers
        print("   🍽️  Processing menu...")
        menu_items = self.helpers.process_menu(menu or [])
        print(f"   ✅ Menu items: {len(menu_items)}")

        # Step 3: Call Railway N-Organ
        print(f"   📡 Calling Railway endpoint...")
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(
                f"{self.url}/personalise",
                json={
                    "customers": valid_customers,
                    "menu_items": menu_items,
                    **kwargs
                }
            )
            response.raise_for_status()
            result = response.json()

        print(f"   ✅ Railway processing complete")

        # Step 4: Generate run_id if not present
        run_id = result.get("run_id") or f"run-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        # Step 5: Save fallback files
        print("   💾 Saving fallback files...")
        fallback_files = self.helpers.save_fallbacks(landlines, invalid, run_id)

        if fallback_files["landlines"]:
            print(f"      📞 Landlines: {fallback_files['landlines']}")
        if fallback_files["invalid"]:
            print(f"      ❌ Invalid: {fallback_files['invalid']}")

        # Step 6: Save output files
        print("   💾 Saving output files...")
        output_files = self.helpers.save_outputs(
            result.get("messages", []),
            run_id,
            result.get("metadata")
        )

        print(f"      📊 CSV: {output_files['csv']}")
        print(f"      📋 JSON: {output_files['json']}")

        # Step 7: Return enhanced result
        print(f"\n💀 {self.name.upper()} complete!\n")

        return {
            **result,
            "run_id": run_id,
            "fallback_files": fallback_files,
            "output_files": output_files,
            "pre_validation_stats": {
                "total_input": len(customers or []),
                "valid": len(valid_customers),
                "landlines": len(landlines),
                "invalid": len(invalid)
            }
        }

    def __call__(self, *args, **kwargs):
        """Sync wrapper for async run()"""
        return asyncio.run(self.run(*args, **kwargs))


# Placeholder class for N-Organ registration
class PersonalisationNOrgan:
    """Hyper Personalisation N-Organ (deployed on Railway)"""
    pass


# Register the hyper_personalisation N-Organ
register_norgan(
    "hyper_personalisation",
    alias="hp",
    url="https://mygrimoire-production.up.railway.app"
)(PersonalisationNOrgan)


# Export everything
__all__ = [
    "summon_norgan",
    "norgans_ls",
    "register_norgan",
    "NOrganProxy"
]

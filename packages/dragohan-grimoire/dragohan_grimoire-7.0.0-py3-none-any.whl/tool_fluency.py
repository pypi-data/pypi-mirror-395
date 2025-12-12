# tool_fluency.py
"""
Backward-compatible import for Grimoire Fluency V2
Redirects to tool_fluency_v2 for seamless compatibility
"""

import sys
import os

# Avoid circular imports - only import if not already importing
if 'tool_fluency_v2' not in sys.modules:
    from tool_fluency_v2 import *
    
    # Ensure the module is activated
    try:
        activate_tool_fluency_v2()
    except Exception:
        pass  # Already activated
else:
    # If v2 is already imported, just re-export
    from tool_fluency_v2 import *


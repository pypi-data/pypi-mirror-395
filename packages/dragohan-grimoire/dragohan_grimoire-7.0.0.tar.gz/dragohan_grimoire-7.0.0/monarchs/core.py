"""
💀 MONARCH BASE - The Shadow Monarch Core 💀
Hybrid agent architecture: structured + command mode
"""

import asyncio
import time
from typing import Dict, Any, Optional, Union, List
from dataclasses import dataclass


@dataclass
class ThoughtResult:
    """Result from agent thinking"""
    thoughts: str
    metadata: Dict[str, Any]


@dataclass
class ActionResult:
    """Result from agent action"""
    action: str
    success: bool
    output: Any
    error: Optional[str] = None
    duration: float = 0.0


@dataclass
class ExecutionTrace:
    """Complete execution trace"""
    steps: List[Dict[str, Any]]
    start_time: float
    end_time: float
    success: bool
    final_result: Any = None


class MonarchBase:
    """
    💀 BASE SHADOW MONARCH 💀
    
    All monarchs inherit from this class.
    Provides:
    - Tool auto-injection (brain, json, files, web, dupes, experience)
    - Hybrid mode (structured + command)
    - Async internal, sync external
    - Incremental streaming via while agent.works
    """
    
    def __init__(self, tools: Dict[str, Any], industry: Optional[str] = None, 
                 monarch_id: Optional[str] = None, **kwargs):
        """
        Initialize Shadow Monarch with tools
        
        Args:
            tools: Dict of grimoire tools (from factory)
            industry: Optional industry specialization
            monarch_id: Optional custom ID
            **kwargs: Additional config
        """
        self.monarch_id = monarch_id or f"monarch-{int(time.time()*1000)}"
        self.industry = industry
        self._config = kwargs
        
        # ===== STATELESS TOOLS (Direct module access) =====
        self.json = tools.get("json")
        self.files = tools.get("files")
        self.web = tools.get("web")
        self.dupes = tools.get("dupes")
        
        # ===== STATEFUL TOOLS (Lazy-loaded instances) =====
        self._brain_class = tools.get("brain")
        self._brain_instance = None
        
        self._experience_class = tools.get("experience")
        self._experience_instance = None
        
        # ===== STREAMING STATE =====
        self._works = False  # Is agent producing incremental results?
        self._current = None  # Current incremental result
        self._results = []  # All results collected
        
        print(f"💀 {self.__class__.__name__} initialized (ID: {self.monarch_id})")
    
    # ========== LAZY-LOADED STATEFUL TOOLS ==========
    
    @property
    def brain(self):
        """Lazy-load Brain instance (tracks session cost)"""
        if self._brain_instance is None:
            print("🧠 Initializing Brain with DeepSeek...")
            self._brain_instance = self._brain_class(provider="deepseek")
        return self._brain_instance
    
    @property
    def experience(self):
        """Lazy-load Experience instance"""
        if self._experience_instance is None:
            self._experience_instance = self._experience_class()
        return self._experience_instance
    
    # ========== STREAMING PROPERTIES ==========
    
    @property
    def works(self) -> bool:
        """
        💀 Check if agent is producing incremental results 💀
        
        Usage:
            while agent.works:
                result = agent.current
                process(result)
        """
        return self._works
    
    @property
    def current(self):
        """Get current incremental result"""
        return self._current
    
    # ========== INTERNAL ASYNC METHODS (Hidden complexity) ==========
    
    async def think(self, prompt: str, max_tokens: int = 800) -> ThoughtResult:
        """
        💀 Use Brain for AI reasoning 💀
        
        Internal method - agents use this to plan and reason.
        """
        start = time.time()
        
        try:
            # Use brain.suggest for reasoning
            result = self.brain.suggest(context=prompt)
            
            duration = time.time() - start
            
            return ThoughtResult(
                thoughts=str(result),
                metadata={
                    "duration": duration,
                    "provider": "deepseek",
                    "prompt_length": len(prompt)
                }
            )
        except Exception as e:
            return ThoughtResult(
                thoughts="",
                metadata={"error": str(e)}
            )
    
    async def do(self, action: str, data: Any = None, params: Optional[Dict] = None) -> ActionResult:
        """
        💀 Execute a tool action 💀
        
        Maps action strings to grimoire tool calls.
        
        Supported actions:
        - "clean_json": Normalize JSON with json_mage
        - "save": Save file with simple_file
        - "load": Load file with simple_file
        - "fetch": Fetch URL with web getter
        - "find_duplicates": Find dupes
        """
        start = time.time()
        params = params or {}
        
        try:
            if action == "clean_json":
                cleaned = self.json.modify(data).clean()
                result = cleaned.raw
                
            elif action == "save":
                key = params.get("key", "output")
                self.files.save(key, data)
                result = {"saved": key}
                
            elif action == "load":
                key = params.get("key")
                result = self.files.load(key)
                
            elif action == "fetch":
                url = params.get("url") or data
                result = self.web.get.data(url)
                
            elif action == "find_duplicates":
                result = self.dupes.find_duplicates(data)
                
            else:
                return ActionResult(
                    action=action,
                    success=False,
                    output=None,
                    error=f"Unknown action: {action}",
                    duration=time.time() - start
                )
            
            return ActionResult(
                action=action,
                success=True,
                output=result,
                duration=time.time() - start
            )
            
        except Exception as e:
            return ActionResult(
                action=action,
                success=False,
                output=None,
                error=str(e),
                duration=time.time() - start
            )
    
    # ========== SYNC WRAPPERS (User-facing, baby simple) ==========
    
    def think_sync(self, prompt: str, **kwargs) -> ThoughtResult:
        """Sync wrapper for think()"""
        from .factory import waitfor
        return waitfor(self.think(prompt, **kwargs))
    
    def do_sync(self, action: str, **kwargs) -> ActionResult:
        """Sync wrapper for do()"""
        from .factory import waitfor
        return waitfor(self.do(action, **kwargs))

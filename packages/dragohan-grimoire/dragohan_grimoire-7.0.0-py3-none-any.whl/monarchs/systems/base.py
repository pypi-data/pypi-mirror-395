"""
💀 SYSTEM BASE - Shadow Monarch Foundation 💀

Universal calling style for ALL orchestration systems:
- system(data) → sync call
- await system.run(data) → async call  
- waitfor(system.run(data)) → blocking call
- while system.works: print(system.current) → streaming
"""

import asyncio
import time
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Union, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
import inspect


@dataclass
class StageResult:
    """Result from a single stage"""
    stage_name: str
    success: bool
    input_count: int
    output_count: int
    duration: float
    output_path: Optional[str] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class RunManifest:
    """Complete run manifest"""
    run_id: str
    run_name: str
    start_ts: str
    end_ts: Optional[str]
    duration: float
    stages: List[StageResult]
    paths: Dict[str, str]
    counts: Dict[str, int]
    errors: List[str]
    cost_by_agent: Dict[str, float]
    total_cost: float
    status: str  # "running", "completed", "failed"
    
    def to_dict(self):
        return {
            "run_id": self.run_id,
            "run_name": self.run_name,
            "start_ts": self.start_ts,
            "end_ts": self.end_ts,
            "duration": self.duration,
            "stages": [s.to_dict() for s in self.stages],
            "paths": self.paths,
            "counts": self.counts,
            "errors": self.errors,
            "cost_by_agent": self.cost_by_agent,
            "total_cost": self.total_cost,
            "status": self.status
        }


class SystemBase:
    """
    💀 SHADOW MONARCH SYSTEM BASE 💀
    
    Universal interface matching agent calling style:
    - Simple as fuck
    - Works everywhere  
    - Same pattern always
    """
    
    def __init__(self, runs_dir: str = "./runs"):
        """
        Initialize system base
        
        Args:
            runs_dir: Base directory for run folders
        """
        self.runs_dir = Path(runs_dir)
        self.runs_dir.mkdir(exist_ok=True)
        
        # Run state
        self.run_id: Optional[str] = None
        self.run_name: Optional[str] = None
        self.run_folder: Optional[Path] = None
        self.start_time: Optional[float] = None
        
        # Tracking
        self.stages: List[StageResult] = []
        self.paths: Dict[str, str] = {}
        self.errors: List[str] = []
        self.cost_by_agent: Dict[str, float] = {}
        
        # 💀 SHADOW MONARCH STREAMING STATE 💀
        # These MUST exist for universal interface
        self._works = False      # Is system working?
        self._current = None      # Current item being processed
        self._stream_buffer = []  # Buffer for streaming results
    
    # ========== 💀 SHADOW MONARCH INTERFACE 💀 ==========
    
    def __call__(self, data: Any, **kwargs):
        """
        💀 UNIVERSAL CALL: system(data) 💀
        
        Matches agent calling style exactly.
        Auto-detects sync/async context.
        """
        # Remove any stream flag from kwargs for sync call
        kwargs.pop('stream', None)
        
        # Always use sync for direct calls
        return self.run_sync(data, **kwargs)
    
    def run(self, data: Any, **kwargs):
        """
        💀 UNIVERSAL RUN METHOD 💀
        
        Auto-detects context:
        - In async context → returns coroutine
        - In sync context → returns result
        - With stream=True → enables polling via .works/.current
        """
        # Check if we're in async context
        try:
            loop = asyncio.get_running_loop()
            # We're in async context
            return self._run_async(data, **kwargs)
        except RuntimeError:
            # We're in sync context
            return self.run_sync(data, **kwargs)
    
    def run_sync(self, data: Any, **kwargs):
        """
        💀 SYNCHRONOUS RUN 💀
        
        For: system.run_sync(data) or waitfor(system.run(data))
        """
        # Get or create event loop
        try:
            loop = asyncio.get_running_loop()
            # We're already in a loop, can't use run_until_complete
            # This shouldn't happen if called correctly
            raise RuntimeError("Cannot call run_sync from async context - use await system.run() instead")
        except RuntimeError:
            # No loop running, we can create one
            pass
        
        # Run async method in new loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self._run_async(data, **kwargs))
        finally:
            loop.close()
    
    async def _run_async(self, data: Any, **kwargs):
        """
        💀 CORE ASYNC IMPLEMENTATION 💀
        
        Must be overridden by subclasses.
        This is where the actual work happens.
        """
        raise NotImplementedError("Subclass must implement _run_async")
    
    # ========== 💀 STREAMING INTERFACE 💀 ==========
    
    @property
    def works(self) -> bool:
        """
        💀 IS SYSTEM WORKING? 💀
        
        For: while system.works: print(system.current)
        """
        return self._works
    
    @property
    def current(self):
        """
        💀 CURRENT RESULT 💀
        
        For: while system.works: print(system.current)
        """
        return self._current
    
    def _set_streaming(self, enabled: bool = True):
        """Enable/disable streaming mode"""
        self._works = enabled
        if not enabled:
            self._current = None
            self._stream_buffer.clear()
    
    def _update_stream(self, item: Any):
        """Update streaming state"""
        self._current = item
        self._stream_buffer.append(item)
    
    # ========== RUN MANAGEMENT ==========
    
    def _init_run(self, run_name: Optional[str] = None, resume: bool = False) -> Path:
        """Initialize or resume a run"""
        if resume and run_name:
            # Check if run exists
            run_folder = self.runs_dir / self._sanitize_name(run_name)
            if run_folder.exists():
                manifest_path = run_folder / "manifest.json"
                if manifest_path.exists():
                    print(f"💀 Resuming run: {run_name}")
                    with open(manifest_path) as f:
                        manifest = json.load(f)
                    self.run_id = manifest["run_id"]
                    self.run_name = manifest["run_name"]
                    self.run_folder = run_folder
                    self.stages = [StageResult(**s) for s in manifest.get("stages", [])]
                    self.paths = manifest.get("paths", {})
                    self.errors = manifest.get("errors", [])
                    self.cost_by_agent = manifest.get("cost_by_agent", {})
                    return run_folder
        
        # Create new run
        if not run_name:
            # Auto-generate name from data if possible
            run_name = f"run-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        else:
            run_name = self._sanitize_name(run_name)
        
        self.run_id = f"{run_name}-{int(time.time()*1000)}"
        self.run_name = run_name
        self.run_folder = self.runs_dir / run_name
        self.run_folder.mkdir(exist_ok=True)
        self.start_time = time.time()
        
        print(f"💀 Run initialized: {self.run_name}")
        print(f"   Folder: {self.run_folder}")
        
        return self.run_folder
    
    def _sanitize_name(self, name: str) -> str:
        """Sanitize run name for filesystem"""
        # Auto-detect if it's a filepath
        if '/' in name or '\\' in name:
            # Extract just the filename
            name = Path(name).name
        
        # Remove extension if present
        name = name.rsplit('.', 1)[0] if '.' in name else name
        
        # Replace invalid chars
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '_')
        
        return name
    
    # ========== FILE OPERATIONS ==========
    
    def _save_stage(self, stage_name: str, filename: str, data: Any) -> str:
        """
        Save stage output with atomic write
        
        Args:
            stage_name: Stage identifier
            filename: Target filename (e.g., "02_preclean.json")
            data: Data to save
            
        Returns:
            Path to saved file
        """
        if not self.run_folder:
            # Auto-init if not initialized
            self._init_run()
        
        filepath = self.run_folder / filename
        temp_path = self.run_folder / f"{filename}.tmp"
        
        # Write to temp file
        with open(temp_path, 'w') as f:
            if isinstance(data, (dict, list)):
                json.dump(data, f, indent=2, default=str)
            else:
                f.write(str(data))
        
        # Atomic rename
        temp_path.rename(filepath)
        
        # Track path
        self.paths[stage_name] = str(filepath)
        
        print(f"   💾 Saved: {filename}")
        return str(filepath)
    
    def _load_stage(self, filename: str) -> Any:
        """Load stage output"""
        if not self.run_folder:
            raise RuntimeError("Run not initialized")
        
        filepath = self.run_folder / filename
        if not filepath.exists():
            return None
        
        with open(filepath) as f:
            try:
                return json.load(f)
            except:
                return f.read()
    
    # ========== STAGE TRACKING ==========
    
    def _record_stage(self, result: StageResult):
        """Record stage completion"""
        self.stages.append(result)
        if result.error:
            self.errors.append(f"{result.stage_name}: {result.error}")
    
    def _track_cost(self, agent_name: str, cost: float):
        """Track cost by agent"""
        self.cost_by_agent[agent_name] = self.cost_by_agent.get(agent_name, 0) + cost
    
    # ========== MANIFEST GENERATION ==========
    
    def _generate_manifest(self, status: str = "completed") -> RunManifest:
        """Generate run manifest"""
        if not self.start_time:
            self.start_time = time.time()
        
        end_time = time.time()
        duration = end_time - self.start_time
        
        # Calculate counts
        counts = {
            "stages": len(self.stages),
            "errors": len(self.errors)
        }
        
        manifest = RunManifest(
            run_id=self.run_id,
            run_name=self.run_name,
            start_ts=datetime.fromtimestamp(self.start_time).isoformat(),
            end_ts=datetime.fromtimestamp(end_time).isoformat(),
            duration=duration,
            stages=self.stages,
            paths=self.paths,
            counts=counts,
            errors=self.errors,
            cost_by_agent=self.cost_by_agent,
            total_cost=sum(self.cost_by_agent.values()),
            status=status
        )
        
        # Save manifest
        if self.run_folder:
            manifest_path = self.run_folder / "manifest.json"
            with open(manifest_path, 'w') as f:
                json.dump(manifest.to_dict(), f, indent=2, default=str)
        
        print(f"\n💀 Run complete: {self.run_name}")
        print(f"   Duration: {duration:.2f}s")
        print(f"   Stages: {len(self.stages)}")
        print(f"   Cost: ₹{manifest.total_cost:.4f}")
        print(f"   Status: {status}")
        
        return manifest


# ========== 💀 HELPER: waitfor FUNCTION 💀 ==========

def waitfor(coro_or_result):
    """
    💀 UNIVERSAL BLOCKING WRAPPER 💀
    
    Usage:
        result = waitfor(system.run(data))
        
    Works with:
        - Coroutines (async functions)
        - Regular values (pass-through)
    """
    # Check if it's a coroutine
    if asyncio.iscoroutine(coro_or_result):
        # It's async, need to run it
        try:
            loop = asyncio.get_running_loop()
            # Already in a loop
            raise RuntimeError("Cannot use waitfor() inside async context - use await instead")
        except RuntimeError:
            # No loop, create one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(coro_or_result)
            finally:
                loop.close()
    else:
        # It's already a result, just return it
        return coro_or_result

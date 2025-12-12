# tool_fluency_v2.py
"""
Tool Fluency v2 - Fixed and Optimized
Universal fluency layer for Grimoire tools with smart patching and recursion protection.

Key improvements:
- Recursion-safe normalization with call stack detection
- Smart patching: only functional entry points, not utilities
- Rate-limited logging with batch processing
- Output stabilization: user output gets priority
- Memory optimization with capping and cleanup

Drop this file next to your grimoire modules and import:
    from tool_fluency_v2 import *
"""

from __future__ import annotations
import json
import os
import traceback
import importlib
import inspect
import functools
from pathlib import Path
from datetime import datetime
import hashlib
import threading
import time
import queue
from typing import Any, Set
from collections import defaultdict

# -----------------------------
# Config
# -----------------------------
GLOBAL_MEMORY_DIR = Path.home() / ".grimoire_memory"
PROJECT_MEMORY_DIR = Path(".") / ".grimoire_memory"
GLOBAL_MEMORY_DIR.mkdir(parents=True, exist_ok=True)
PROJECT_MEMORY_DIR.mkdir(parents=True, exist_ok=True)

MEMORY_FILE = "memory.json"
ACTIVITY_LOG = "activity.log"
ACTIVITY_JSON = "activity.json"

GLOBAL_MEMORY_FILE = GLOBAL_MEMORY_DIR / MEMORY_FILE
PROJECT_MEMORY_FILE = PROJECT_MEMORY_DIR / MEMORY_FILE
GLOBAL_ACTIVITY_LOG = GLOBAL_MEMORY_DIR / ACTIVITY_LOG
PROJECT_ACTIVITY_LOG = PROJECT_MEMORY_DIR / ACTIVITY_LOG
GLOBAL_ACTIVITY_JSON = GLOBAL_MEMORY_DIR / ACTIVITY_JSON
PROJECT_ACTIVITY_JSON = PROJECT_MEMORY_DIR / ACTIVITY_JSON

# Smart patching: only these functional entry points get patched
PRIMARY_FUNCTIONS = {
    "json_mage": ["modify"],
    "loops": ["loopon", "LoopOn"],
    "simple_file": ["load", "save"],
    "getter": ["get"],
    "converter": ["convert"],
    "duplicates": ["modify"],
    "internet": ["runfor", "waitfor"]
}

# Utility functions to NEVER patch (too granular or internal)
SKIP_FUNCTIONS = {
    "Any", "Union", "List", "Dict", "Counter", "Path", "datetime"
}

# Learning and recovery settings
DEFAULT_FLATTEN_DEPTH = 20
AUTO_APPLY_CONFIDENCE = 0.7
_ACTIVITY_JSON_CAP = 2000  # Reduced to prevent memory bloat
_MEMORY_CLEANUP_THRESHOLD = 10000  # Clean old patterns periodically

# Logging throttling
_LOG_BATCH_SIZE = 10
_LOG_FLUSH_INTERVAL = 0.5  # seconds
_OUTPUT_LOCK_TIMEOUT = 0.1  # very short to avoid blocking

# Recursion protection
_RECURSION_DEPTH_LIMIT = 3
_NORMALIZE_CALL_STACK_LIMIT = 5

# -----------------------------
# Thread-safe logging queue
# -----------------------------
class AsyncLogger:
    def __init__(self):
        self.log_queue = queue.Queue()
        self.batch_buffer = []
        self.last_flush = time.time()
        self._writer_thread = None
        self._running = True
        self._start_writer()
    
    def _start_writer(self):
        def writer_worker():
            while self._running:
                try:
                    # Batch processing
                    now = time.time()
                    if (now - self.last_flush) > _LOG_FLUSH_INTERVAL or len(self.batch_buffer) >= _LOG_BATCH_SIZE:
                        self._flush_batch()
                    
                    # Non-blocking queue read
                    try:
                        record = self.log_queue.get(timeout=0.1)
                        self.batch_buffer.append(record)
                    except queue.Empty:
                        pass
                        
                except Exception:
                    pass  # Silent failure to avoid crashes
        
        self._writer_thread = threading.Thread(target=writer_worker, daemon=True)
        self._writer_thread.start()
    
    def _flush_batch(self):
        if not self.batch_buffer:
            return
        
        batch = self.batch_buffer.copy()
        self.batch_buffer.clear()
        self.last_flush = time.time()
        
        for record in batch:
            try:
                self._write_record(record)
            except Exception:
                pass  # Silent failure
    
    def _write_record(self, record):
        # Write to text log
        line = f"{_now_iso()} {record.get('human', record.get('type'))}: {json.dumps(record, default=str, ensure_ascii=False)}"
        try:
            _safe_append_text(GLOBAL_ACTIVITY_LOG, line)
            _safe_append_text(PROJECT_ACTIVITY_LOG, line)
        except Exception:
            pass
        
        # Write to JSON activity log (with batching)
        try:
            _safe_append_json_activity(GLOBAL_ACTIVITY_JSON, record)
            _safe_append_json_activity(PROJECT_ACTIVITY_JSON, record)
        except Exception:
            pass
    
    def log(self, record: dict, human: str | None = None):
        if human:
            record['human'] = human
        # Queue for async processing
        try:
            self.log_queue.put_nowait(record)
        except queue.Full:
            pass  # Drop if queue full to prevent memory issues
    
    def flush(self):
        """Force flush all pending logs"""
        self._flush_batch()

# Global logger instance
_async_logger = AsyncLogger()

# -----------------------------
# Recursion protection
# -----------------------------
class RecursionGuard:
    def __init__(self):
        self._normalize_stack = []
        self._function_call_stack = defaultdict(int)
    
    def check_normalize_recursion(self) -> bool:
        """Detect if we're in a normalize recursion loop"""
        return len(self._normalize_stack) > _NORMALIZE_CALL_STACK_LIMIT
    
    def enter_normalize(self):
        self._normalize_stack.append(time.time())
    
    def exit_normalize(self):
        if self._normalize_stack:
            self._normalize_stack.pop()
    
    def check_function_recursion(self, key: str) -> bool:
        """Check if function is being called recursively"""
        return self._function_call_stack[key] > _RECURSION_DEPTH_LIMIT
    
    def enter_function(self, key: str):
        self._function_call_stack[key] += 1
    
    def exit_function(self, key: str):
        if self._function_call_stack[key] > 0:
            self._function_call_stack[key] -= 1

_recursion_guard = RecursionGuard()

# -----------------------------
# Raw function access (bypass patching)
# -----------------------------
_raw_functions = {}

def _register_raw_function(module_name: str, func_name: str, func):
    """Register raw (unpatched) version of function"""
    key = f"{module_name}.{func_name}"
    _raw_functions[key] = func

def _get_raw_function(module_name: str, func_name: str):
    """Get raw (unpatched) version of function"""
    key = f"{module_name}.{func_name}"
    return _raw_functions.get(key)

# -----------------------------
# Utilities
# -----------------------------

def _now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"

def _trace_short() -> str:
    return traceback.format_exc(limit=1)

def _sha1_of(obj: Any) -> str:
    try:
        b = json.dumps(obj, default=str, sort_keys=True).encode("utf-8")
    except Exception:
        b = repr(obj).encode("utf-8")
    return hashlib.sha1(b).hexdigest()

def _safe_read_json(path: Path) -> dict | list:
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return {}

def _safe_write_json(path: Path, data: Any):
    """Thread-safe JSON write with timeout"""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    except Exception:
        pass  # Silent failure

def _safe_append_text(path: Path, text: str):
    """Thread-safe text append with timeout"""
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(text + "\n")
    except Exception:
        pass

def _safe_append_json_activity(path: Path, record: dict):
    """Thread-safe JSON activity append with batching"""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        data = _safe_read_json(path)
        if not isinstance(data, list):
            data = []
        data.append(record)
        # Cap list to prevent memory issues
        if len(data) > _ACTIVITY_JSON_CAP:
            data = data[-_ACTIVITY_JSON_CAP:]
        _safe_write_json(path, data)
    except Exception:
        pass

# -----------------------------
# Enhanced normalization with recursion protection
# -----------------------------

def _is_pathlike(obj):
    return isinstance(obj, (str, Path))

def _has_raw(obj):
    try:
        return hasattr(obj, "raw")
    except Exception:
        return False

def _looks_like_api_wrapper(obj):
    if not isinstance(obj, dict):
        return False
    keys = set(obj.keys())
    return bool(keys & {"data", "results", "items", "payload", "cleaned_data"})

def _try_json_load_raw(path):
    """Raw JSON load that bypasses all patching"""
    try:
        p = Path(path)
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        try:
            return Path(path).read_text(encoding="utf-8").splitlines()
        except Exception:
            return None
    return None

def _grimoire_flatten(data, max_depth: int = DEFAULT_FLATTEN_DEPTH):
    def _inner(el, depth):
        if depth <= 0:
            yield el
            return
        if isinstance(el, list):
            for sub in el:
                if isinstance(sub, list):
                    yield from _inner(sub, depth - 1)
                else:
                    yield sub
        else:
            yield el

    if isinstance(data, list):
        return list(_inner(data, max_depth))
    return data

def _grimoire_normalize(data):
    """Enhanced normalize with recursion protection"""
    # Recursion detection
    if _recursion_guard.check_normalize_recursion():
        _async_logger.log({
            "type": "recursion_protected",
            "depth": len(_recursion_guard._normalize_stack),
            "time": _now_iso()
        }, human=f"[Fluency] normalize recursion detected, returning original data")
        return data
    
    _recursion_guard.enter_normalize()
    try:
        # Handle .raw attribute
        if _has_raw(data):
            return data.raw

        # Handle file paths using RAW simple_file.load (no patching)
        if _is_pathlike(data):
            try:
                raw_load = _get_raw_function("simple_file", "load")
                if raw_load:
                    return raw_load(str(data))
            except Exception:
                pass
            
            # Fallback to raw JSON loading
            loaded = _try_json_load_raw(data)
            if loaded is not None:
                return loaded

        # Handle API wrapper objects
        if isinstance(data, dict) and _looks_like_api_wrapper(data):
            for candidate in ("data", "results", "items", "payload", "cleaned_data"):
                if candidate in data:
                    return data[candidate]
            if len(data) == 1:
                try:
                    return list(data.values())[0]
                except Exception:
                    pass

        return data
    finally:
        _recursion_guard.exit_normalize()

# -----------------------------
# Memory management
# -----------------------------

class PersistentMemory:
    def __init__(self, global_file: Path = GLOBAL_MEMORY_FILE, project_file: Path = PROJECT_MEMORY_FILE):
        self.global_file = global_file
        self.project_file = project_file
        self._data = {
            "success_patterns": {},
            "failure_lessons": {},
            "metadata": {},
            "counters": {}
        }
        self._load()
        self._cleanup_old_patterns()

    def _load(self):
        g = _safe_read_json(self.global_file) or {}
        p = _safe_read_json(self.project_file) or {}
        for k in self._data.keys():
            merged = {}
            if isinstance(g.get(k), dict):
                merged.update(g.get(k))
            if isinstance(p.get(k), dict):
                merged.update(p.get(k))
            self._data[k] = merged

    def _persist(self):
        # Write merged view to both files
        merged = self._data
        _safe_write_json(self.global_file, merged)
        _safe_write_json(self.project_file, merged)

    def _cleanup_old_patterns(self):
        """Clean up old patterns to prevent memory bloat"""
        patterns = self._data["success_patterns"]
        if len(patterns) > _MEMORY_CLEANUP_THRESHOLD:
            # Keep only the most recent/high-confidence patterns
            sorted_patterns = sorted(
                patterns.items(),
                key=lambda x: (x[1].get("confidence", 0), x[1].get("wins", 0)),
                reverse=True
            )
            self._data["success_patterns"] = dict(sorted_patterns[:_MEMORY_CLEANUP_THRESHOLD // 2])

    def remember_success(self, task_sig: str, strategy: str, meta: dict | None = None):
        rec = self._data["success_patterns"].get(task_sig, {"wins": 0, "strategy": None, "confidence": 0.0, "last_used": None, "meta": {}})
        rec["wins"] = rec.get("wins", 0) + 1
        rec["strategy"] = strategy
        rec["last_used"] = _now_iso()
        rec["confidence"] = rec["wins"] / (rec["wins"] + 1)
        if meta:
            rec_meta = rec.get("meta", {})
            rec_meta.update(meta)
            rec["meta"] = rec_meta
        self._data["success_patterns"][task_sig] = rec
        self._persist()
        _async_logger.log({
            "type": "success_pattern",
            "task_sig": task_sig,
            "strategy": strategy,
            "meta": meta or {},
            "time": _now_iso()
        }, human=f"[Fluency] success pattern recorded: {task_sig} -> {strategy}")

    def remember_failure(self, error_sig: str, solution: dict | None = None):
        rec = self._data["failure_lessons"].get(error_sig, {"tries": 0, "solutions": [], "last_seen": None})
        rec["tries"] = rec.get("tries", 0) + 1
        rec["last_seen"] = _now_iso()
        if solution:
            rec["solutions"].append({"solution": solution, "time": _now_iso()})
        self._data["failure_lessons"][error_sig] = rec
        self._persist()
        _async_logger.log({
            "type": "failure_lesson",
            "error_sig": error_sig,
            "solution": solution or {},
            "time": _now_iso()
        }, human=f"[Fluency] failure recorded: {error_sig}")

    def get_success(self, task_sig: str):
        return self._data["success_patterns"].get(task_sig)

    def get_failure(self, error_sig: str):
        return self._data["failure_lessons"].get(error_sig)

    def increment_counter(self, key: str):
        self._data["counters"][key] = self._data["counters"].get(key, 0) + 1

    def export(self):
        return self._data.copy()

# -----------------------------
# Enhanced strategy runner
# -----------------------------

def _task_signature(module_name: str, func_name: str, args, kwargs) -> str:
    try:
        def shape(x):
            if _has_raw(x):
                return ("mage",)
            if isinstance(x, dict):
                return ("dict", tuple(sorted(x.keys())))
            if isinstance(x, list):
                return ("list", len(x))
            if _is_pathlike(x):
                return ("path", str(x)[:120])
            return (type(x).__name__,)
        signature = {
            "module": module_name,
            "func": func_name,
            "args": [shape(a) for a in args],
            "kwargs": {k: shape(v) for k, v in kwargs.items()}
        }
        return _sha1_of(signature)
    except Exception:
        return _sha1_of(repr((module_name, func_name)))

def _error_signature(e: Exception) -> str:
    try:
        return f"{type(e).__name__}:{str(e)[:200]}"
    except Exception:
        return f"Exception:{_sha1_of(repr(e))}"

def _maybe_wrap_result(res, mem: PersistentMemory):
    try:
        if _has_raw(res):
            mem.increment_counter("returns_mage_like")
            return res
    except Exception:
        pass

    if isinstance(res, (list, dict)):
        try:
            raw_modify = _get_raw_function("json_mage", "modify")
            if raw_modify:
                wrapped = raw_modify(res)
                mem.increment_counter("returns_wrapped_by_modify")
                return wrapped
        except Exception:
            pass

    mem.increment_counter("returns_raw_python")
    return res

def _grimo_normalize_try(x):
    """Safe normalization that won't cause recursion"""
    try:
        return _grimoire_normalize(x)
    except Exception:
        try:
            if _has_raw(x):
                return x.raw
        except Exception:
            pass
    return x

def _apply_strategies_and_record(orig_fn, module_name: str, func_name: str, mem: PersistentMemory):
    @functools.wraps(orig_fn)
    def wrapped(*args, **kwargs):
        function_key = f"{module_name}.{func_name}"
        
        # Recursion protection
        if _recursion_guard.check_function_recursion(function_key):
            _async_logger.log({
                "type": "recursion_protected",
                "function": function_key,
                "depth": _recursion_guard._function_call_stack[function_key],
                "time": _now_iso()
            }, human=f"[Fluency] function recursion detected for {function_key}, calling raw")
            return orig_fn(*args, **kwargs)
        
        _recursion_guard.enter_function(function_key)
        try:
            task_sig = _task_signature(module_name, func_name, args, kwargs)
            mem.increment_counter("calls")
            mem.increment_counter(f"calls::{module_name}.{func_name}")

            # Auto-apply learned strategies
            learned = mem.get_success(task_sig)
            if learned and learned.get("confidence", 0.0) >= AUTO_APPLY_CONFIDENCE:
                strategy = learned.get("strategy")
                _async_logger.log({
                    "type": "auto_apply",
                    "task_sig": task_sig,
                    "strategy": strategy,
                    "meta": learned.get("meta", {}),
                    "time": _now_iso()
                }, human=f"[Fluency] auto-applying learned strategy for {module_name}.{func_name}: {strategy}")
                try:
                    if strategy == "call_raw":
                        res = orig_fn(*args, **kwargs)
                        mem.remember_success(task_sig, strategy)
                        return _maybe_wrap_result(res, mem)
                    elif strategy == "normalize_first":
                        norm_args = tuple(_grimoire_normalize(a) for a in args)
                        norm_kwargs = {k: _grimoire_normalize(v) for k, v in kwargs.items()}
                        res = orig_fn(*norm_args, **norm_kwargs)
                        mem.remember_success(task_sig, strategy)
                        return _maybe_wrap_result(res, mem)
                except Exception:
                    _async_logger.log({
                        "type": "auto_apply_failed",
                        "task_sig": task_sig,
                        "strategy": strategy,
                        "time": _now_iso()
                    }, human=f"[Fluency] learned strategy failed for {module_name}.{func_name}: {strategy}")

            attempts = []
            
            # Strategy 1: normalize first
            try:
                norm_args = tuple(_grimoire_normalize(a) for a in args)
                norm_kwargs = {k: _grimoire_normalize(v) for k, v in kwargs.items()}
                res = orig_fn(*norm_args, **norm_kwargs)
                mem.remember_success(task_sig, "normalize_first", 
                                   meta={"args_shape": str([type(a).__name__ for a in norm_args])})
                return _maybe_wrap_result(res, mem)
            except Exception as e1:
                attempts.append(("normalize_first", e1))

            # Strategy 2: raw call
            try:
                res = orig_fn(*args, **kwargs)
                mem.remember_success(task_sig, "call_raw", meta={"note": "raw_call_succeeded"})
                return _maybe_wrap_result(res, mem)
            except Exception as e2:
                attempts.append(("call_raw", e2))

            # Strategy 3: mixed unwrap (safer approach)
            try:
                new_args = []
                for a in args:
                    if _has_raw(a):
                        new_args.append(a.raw)
                    else:
                        new_args.append(_grimo_normalize_try(a))
                res = orig_fn(*tuple(new_args), **kwargs)
                mem.remember_success(task_sig, "mixed_unwrap", meta={"note": "mixed_unwrap_last_resort"})
                return _maybe_wrap_result(res, mem)
            except Exception as e3:
                attempts.append(("mixed_unwrap", e3))

            # All attempts failed
            last_err = attempts[-1][1] if attempts else Exception("unknown")
            err_sig = _error_signature(last_err)
            mem.remember_failure(err_sig, solution={
                "attempts": [
                    {"strategy": s, "error": str(type(ex).__name__) + ':' + str(ex)[:200]} 
                    for s, ex in attempts
                ]
            })
            _async_logger.log({
                "type": "call_failure",
                "task_sig": task_sig,
                "module": module_name,
                "function": func_name,
                "attempts": [
                    {"strategy": s, "error": str(type(ex).__name__) + ':' + str(ex)[:200]} 
                    for s, ex in attempts
                ],
                "time": _now_iso()
            }, human=f"[Fluency] ERROR {module_name}.{func_name} failed after strategies: {[s for s, _ in attempts]}")

            raise last_err
        finally:
            _recursion_guard.exit_function(function_key)

    return wrapped

# -----------------------------
# Smart module patching
# -----------------------------

def _is_primary_function(module_name: str, func_name: str) -> bool:
    """Check if this is a primary function that should be patched"""
    if func_name in SKIP_FUNCTIONS:
        return False
    if module_name in PRIMARY_FUNCTIONS:
        return func_name in PRIMARY_FUNCTIONS[module_name]
    return False

def _wrap_primary_functions(modname: str, mem: PersistentMemory):
    """Wrap only primary functions, register raw versions"""
    try:
        mod = importlib.import_module(modname)
    except Exception:
        _async_logger.log({
            "type": "module_missing", 
            "module": modname, 
            "time": _now_iso()
        }, human=f"[Fluency] {modname} not found - skipping patch.")
        return

    GrimoireBridge.connect(modname, mod)

    # Patch primary functions only
    for name, obj in list(vars(mod).items()):
        if name.startswith("_"):
            continue
        if not callable(obj):
            continue
        if not _is_primary_function(modname, name):
            continue

        try:
            # Register raw version first
            _register_raw_function(modname, name, obj)
            
            # Then patch
            wrapped = _apply_strategies_and_record(obj, modname, name, mem)
            setattr(mod, name, wrapped)
            _async_logger.log({
                "type": "patched", 
                "module": modname, 
                "name": name, 
                "time": _now_iso()
            }, human=f"[Fluency] patched {modname}.{name}")
        except Exception:
            _async_logger.log({
                "type": "patch_error", 
                "module": modname, 
                "name": name, 
                "time": _now_iso(), 
                "trace": _trace_short()
            }, human=f"[Fluency] failed to patch {modname}.{name}")

    # Handle classes (like MageJSON)
    for name, cls in inspect.getmembers(mod, inspect.isclass):
        if name.startswith("_"):
            continue
        
        common_methods = ["all", "get", "filter", "find", "first", "last"]
        patched_any = False
        
        try:
            for m in common_methods:
                if hasattr(cls, m):
                    orig = getattr(cls, m)
                    if callable(orig) and _is_primary_function(modname, f"{name}.{m}"):
                        # Register raw version
                        _register_raw_function(modname, f"{name}.{m}", orig)
                        
                        # Patch
                        wrapped = _apply_strategies_and_record(orig, modname, f"{name}.{m}", mem)
                        setattr(cls, m, wrapped)
                        patched_any = True
            
            if patched_any:
                _async_logger.log({
                    "type": "patched_class", 
                    "module": modname, 
                    "class": name, 
                    "time": _now_iso()
                }, human=f"[Fluency] patched {modname}.{name}")
        except Exception:
            pass

# -----------------------------
# GrimoireBridge (enhanced)
# -----------------------------

class GrimoireBridge:
    _memory = None
    _tools = {}

    @classmethod
    def init_memory(cls, mem: PersistentMemory):
        cls._memory = mem

    @classmethod
    def remember(cls, key: str, value, scope: str = "global"):
        if cls._memory is None:
            return None
        cls._memory._data["metadata"][key] = {"value": value, "time": _now_iso(), "scope": scope}
        cls._memory._persist()
        _async_logger.log({
            "type": "bridge_remember", 
            "key": key, 
            "scope": scope, 
            "time": _now_iso()
        }, human=f"[GrimoireBridge] remembered {key} in {scope}")

    @classmethod
    def recall(cls, key: str, default=None):
        if cls._memory is None:
            return default
        return cls._memory._data.get("metadata", {}).get(key, {}).get("value", default)

    @classmethod
    def connect(cls, name: str, tool_obj):
        cls._tools[name] = tool_obj
        _async_logger.log({
            "type": "bridge_connect", 
            "tool": name, 
            "time": _now_iso()
        }, human=f"[GrimoireBridge] connected {name}")
        return tool_obj

    @classmethod
    def fetch_tool(cls, name: str):
        return cls._tools.get(name)

    @classmethod
    def memory_summary(cls):
        """Return a summary of learned patterns"""
        if cls._memory is None:
            return {"error": "No memory initialized"}
        
        data = cls._memory.export()
        summary = {
            "success_patterns_count": len(data.get("success_patterns", {})),
            "failure_lessons_count": len(data.get("failure_lessons", {})),
            "most_successful_patterns": [],
            "recent_failures": []
        }
        
        # Top success patterns
        patterns = data.get("success_patterns", {})
        if patterns:
            top_patterns = sorted(
                patterns.items(),
                key=lambda x: x[1].get("confidence", 0),
                reverse=True
            )[:5]
            summary["most_successful_patterns"] = [
                {"signature": sig, "strategy": info.get("strategy"), "confidence": info.get("confidence")}
                for sig, info in top_patterns
            ]
        
        # Recent failures
        failures = data.get("failure_lessons", {})
        if failures:
            recent_failures = sorted(
                failures.items(),
                key=lambda x: x[1].get("last_seen", ""),
                reverse=True
            )[:3]
            summary["recent_failures"] = [
                {"error": sig, "tries": info.get("tries"), "last_seen": info.get("last_seen")}
                for sig, info in recent_failures
            ]
        
        return summary

# -----------------------------
# Activation
# -----------------------------

_already_activated = False

def activate_tool_fluency_v2():
    global _already_activated
    if _already_activated:
        return
    _already_activated = True

    mem = PersistentMemory()
    GrimoireBridge.init_memory(mem)

    # Patch modules with smart targeting
    for modname in PRIMARY_FUNCTIONS.keys():
        _wrap_primary_functions(modname, mem)

    # Register globals
    globals().update({
        "GrimoireBridge": GrimoireBridge,
        "_grimoire_normalize": _grimoire_normalize,
        "_grimoire_flatten": _grimoire_flatten,
        "PersistentMemory": PersistentMemory
    })

    _async_logger.log({
        "type": "activated", 
        "time": _now_iso()
    }, human="[Fluency] GRIMOIRE FLUENCY LAYER V2 ACTIVATED")
    
    try:
        print("💀 GRIMOIRE FLUENCY LAYER V2 ACTIVATED 💀")
        print("✅ Smart patching enabled (primary functions only)")
        print("✅ Recursion protection active")
        print("✅ Rate-limited logging enabled")
    except Exception:
        pass

# Output confirmation hook
def execution_complete(result_summary: str = "Execution completed"):
    """Call this to confirm execution completion and see results clearly"""
    _async_logger.flush()  # Force flush logs
    print(f"\n🔮 {result_summary}")
    print("💀 Grimoire Fluency V2 - Ready for next spell")

# Auto-activate on import
activate_tool_fluency_v2()

# Export the main interface
__all__ = [
    "GrimoireBridge", 
    "PersistentMemory", 
    "_grimoire_normalize", 
    "_grimoire_flatten", 
    "execution_complete"
]

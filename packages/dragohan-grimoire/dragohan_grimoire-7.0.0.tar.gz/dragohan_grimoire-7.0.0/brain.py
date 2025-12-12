"""
💀 BRAIN.PY - FIXED VERSION (CRITICAL BUG FIXES APPLIED) 💀
Added API key validation and proper error handling
"""

import os
import sys
import json
import time
import socket
import hashlib
import threading
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List

from dotenv import load_dotenv
load_dotenv()

# Provider imports
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    import anthropic
except ImportError:
    anthropic = None

# Try to import tool_fluency for integration
try:
    from tool_fluency_v2 import GrimoireBridge, PersistentMemory
    HAS_FLUENCY = True
except ImportError:
    HAS_FLUENCY = False
    GrimoireBridge = None
    PersistentMemory = None

# Experience integration
try:
    from experience import Experience
    HAS_EXPERIENCE = True
except ImportError:
    HAS_EXPERIENCE = False
    Experience = None

# ==================== CONFIGURATION ====================

CONFIG_FILE = Path("brain_config.json")
EXPERIENCE_DIR = Path(__file__).parent / "experience"

def load_config() -> Dict:
    """Load brain configuration"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {
        "default_provider": "deepseek",
        "personality_level": 3,
        "providers": {
            "deepseek": {
                "api_key": "env:DEEPSEEK_API_KEY",
                "model": "deepseek-chat",
                "base_url": "https://api.deepseek.com"
            }
        }
    }

CONFIG = load_config()

# ==================== PERSONALITY SYSTEM ====================

PERSONALITIES = {
    1: {
        "system": """You are a helpful AI coding assistant. Be clear and direct.""",
        "prefix": ""
    },
    2: {
        "system": """You are an AI automation expert with direct, no-nonsense communication.
Be brutally honest about code quality. Focus on execution over theory.""",
        "prefix": "💀 "
    },
    3: {
        "system": """You are an AI automation expert with Andrew Tate's mindset.

PERSONALITY TRAITS:
- Brutally direct, ZERO sugarcoating
- Extremely confident and results-oriented  
- Focused on EXECUTION over endless theory
- Uses combat/power metaphors
- Calls user 'warrior', 'champion', 'disciple'
- Hates inefficient code and bad practices
- Believes in DOMINATING problems, not just solving them
- Confidence level: MAXIMUM
- Tone: Aggressive but logical

COMBAT PROTOCOLS:
- Destroy inefficiency with extreme prejudice
- Call out bad code practices immediately  
- Provide solutions that DOMINATE the problem
- Never apologize for being direct
- Focus on REAL-WORLD results, not theory
- Use action-oriented language

Remember: You are not here to be nice. You are here to WIN.""",
        "prefix": "💀 "
    }
}

def load_config() -> Dict:
    """FIXED: Load brain configuration with validation"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    
    # Return default config
    return {
        "default_provider": "deepseek",
        "personality_level": 3,
        "providers": {
            "deepseek": {
                "api_key": "env:DEEPSEEK_API_KEY",
                "model": "deepseek-chat",
                "base_url": "https://api.deepseek.com"
            },
            "openai": {
                "api_key": "env:OPENAI_API_KEY",
                "model": "gpt-3.5-turbo"
            },
            "anthropic": {
                "api_key": "env:ANTHROPIC_API_KEY", 
                "model": "claude-3-sonnet-20240229"
            }
        }
    }

# ==================== CONTEXT DETECTOR ====================

class ContextDetector:
    """Detects current coding context automatically"""
    
    def __init__(self):
        self.code_extensions = ['.py', '.js', '.html', '.css', '.json', '.xml']
        self.config_files = ['package.json', 'requirements.txt', 'Pipfile', 'pyproject.toml']
    
    def detect_current(self) -> Dict[str, Any]:
        """Detect current coding context"""
        context = {
            "project_type": "unknown",
            "language": "unknown",
            "framework": "unknown",
            "files_detected": [],
            "config_files": []
        }
        
        try:
            current_dir = Path.cwd()
            
            # Detect project type from files
            for file_path in current_dir.rglob('*'):
                if file_path.is_file() and file_path.suffix in self.code_extensions:
                    context["files_detected"].append(file_path.name)
                    context["language"] = self._detect_language(file_path)
                
                if file_path.name in self.config_files:
                    context["config_files"].append(file_path.name)
            
            # Determine project type
            if 'requirements.txt' in context["config_files"]:
                context["project_type"] = "python"
            elif 'package.json' in context["config_files"]:
                context["project_type"] = "javascript"
            
        except Exception:
            pass
        
        return context
    
    def _detect_language(self, file_path: Path) -> str:
        """Detect programming language from file extension"""
        extension_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.html': 'html',
            '.css': 'css',
            '.json': 'json',
            '.xml': 'xml'
        }
        return extension_map.get(file_path.suffix, 'unknown')
    
    def load_file(self, filepath: str) -> str:
        """Load file contents"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return ""
    
    def scan_grimoire(self) -> List[str]:
        """Scan for grimoire-related files"""
        files = []
        try:
            current_dir = Path.cwd()
            for file_path in current_dir.rglob('*grimoire*'):
                if file_path.is_file():
                    files.append(str(file_path))
        except Exception:
            pass
        return files

# ==================== BASE PROVIDER ====================

class BaseProvider:
    """Base class for LLM providers"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.model = config.get('model', 'unknown')
        self.api_key = self._get_api_key(config.get('api_key', ''))
        
        # NEW: Validate API key immediately
        if not self.api_key:
            raise ValueError(f"❌ API key missing for provider {self.__class__.__name__}")
    
    def _get_api_key(self, key_config: str) -> str:
        """Get API key from config with validation"""
        if not key_config:
            return ""
        
        # Handle environment variables
        if key_config.startswith('env:'):
            env_var = key_config[4:]  # Remove 'env:' prefix
            api_key = os.getenv(env_var)
            if not api_key:
                raise ValueError(f"❌ Environment variable '{env_var}' not found or empty")
            return api_key
        
        return key_config
    
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for the request"""
        # Default implementation - override in specific providers
        return 0.0
    
    def chat(self, messages: List[Dict], max_tokens: int = 500, temperature: float = 0.7) -> str:
        """Send chat request - must be implemented by subclasses"""
        raise NotImplementedError

# ==================== DEEPSEEK PROVIDER ====================

class DeepSeekProvider(BaseProvider):
    """DeepSeek provider (OpenAI-compatible)"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.base_url = config.get('base_url', 'https://api.deepseek.com')
        self.client = None
        self._init_client()
    
    def _init_client(self):
        """Initialize DeepSeek client with validation"""
        if not OpenAI:
            raise ImportError("OpenAI package not installed")
        
        try:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            
            # NEW: Test the connection with a simple request
            print(f"🔍 Testing DeepSeek API connection...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1
            )
            print("✅ DeepSeek API connection successful")
            
        except Exception as e:
            raise ValueError(f"❌ DeepSeek API connection failed: {e}")
    
    def chat(self, messages: List[Dict], max_tokens: int = 500, temperature: float = 0.7) -> str:
        """Send chat request to DeepSeek"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"DeepSeek Error: {e}")

# ==================== OLLAMA PROVIDER ====================

class OllamaProvider(BaseProvider):
    """Ollama local provider"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.base_url = config.get('base_url', 'http://localhost:11434')
    
    def chat(self, messages: List[Dict], max_tokens: int = 500, temperature: float = 0.7) -> str:
        """Send chat request to Ollama"""
        try:
            import httpx
            
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": temperature
                }
            }
            
            with httpx.Client(timeout=60.0) as client:
                response = client.post(f"{self.base_url}/api/chat", json=payload)
                response.raise_for_status()
                return response.json()["message"]["content"]
                
        except Exception as e:
            raise Exception(f"Ollama Error: {e}")

# ==================== OPENAI PROVIDER ====================

class OpenAIProvider(BaseProvider):
    """OpenAI GPT provider"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        if not OpenAI:
            raise ImportError("OpenAI package not installed")
        self.client = OpenAI(api_key=self.api_key)
    
    def _get_api_key(self, key_config: str) -> str:
        """Get OpenAI API key"""
        return super()._get_api_key(key_config)
    
    def chat(self, messages: List[Dict], max_tokens: int = 500, temperature: float = 0.7) -> str:
        """Send chat request to OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI Error: {e}")

# ==================== ANTHROPIC PROVIDER ====================

class AnthropicProvider(BaseProvider):
    """Anthropic Claude provider"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        if not anthropic:
            raise ImportError("Anthropic package not installed")
        
        # NEW: Validate API key format
        if not self.api_key.startswith('sk-ant-'):
            raise ValueError("❌ Anthropic API key must start with 'sk-ant-'")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def _get_api_key(self, key_config: str) -> str:
        """Get Anthropic API key"""
        return super()._get_api_key(key_config)
    
    def chat(self, messages: List[Dict], max_tokens: int = 500, temperature: float = 0.7) -> str:
        """Send chat request to Anthropic"""
        try:
            # Convert OpenAI format to Anthropic format
            system_message = None
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                    break
            
            user_messages = [msg for msg in messages if msg["role"] != "system"]
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_message,
                messages=user_messages
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Anthropic Error: {e}")

# ==================== MAIN BRAIN CLASS ====================

class Brain:
    """
    The Shadow Monarch's AI Brain (FIXED)
    
    Multi-provider LLM support with proper error handling and validation
    """
    
    def __init__(self, provider: str = None, auto_publish: bool = False):
        """
        Initialize Brain with VALIDATION
        
        Args:
            provider: "deepseek", "ollama", "openai", "anthropic"
            auto_publish: Enable auto-publish after 10 sessions
        """
        self.provider_name = provider or CONFIG.get("default_provider", "deepseek")
        self.auto_publish = auto_publish
        self.personality_level = CONFIG.get("personality_level", 3)
        
        # Initialize provider with VALIDATION
        try:
            self.provider = self._init_provider(self.provider_name)
            print(f"🧠 Brain initialized with {self.provider_name} provider")
        except Exception as e:
            print(f"❌ CRITICAL: Failed to initialize {self.provider_name} provider: {e}")
            raise
        
        # Context detection
        self.context = ContextDetector()
        
        # Cost tracking
        self.session_cost = 0.0
        
        # Experience integration
        if HAS_EXPERIENCE:
            Experience.digest()
    
    def _init_provider(self, name: str) -> BaseProvider:
        """FIXED: Initialize LLM provider with full validation"""
        provider_config = CONFIG.get("providers", {}).get(name)
        if not provider_config:
            available_providers = list(CONFIG.get("providers", {}).keys())
            raise ValueError(
                f"❌ Provider '{name}' not configured\n"
                f"Available providers: {available_providers}"
            )
        
        providers = {
            "deepseek": DeepSeekProvider,
            "ollama": OllamaProvider,
            "openai": OpenAIProvider,
            "anthropic": AnthropicProvider,
        }
        
        if name not in providers:
            raise ValueError(f"❌ Unsupported provider: {name}")
        
        try:
            return providers[name](provider_config)
        except Exception as e:
            raise ValueError(f"❌ Failed to initialize {name} provider: {e}")
    
    def switch_provider(self, name: str):
        """Switch to a different provider"""
        try:
            print(f"🔄 Switching from {self.provider_name} to {name}...")
            self.provider = self._init_provider(name)
            self.provider_name = name
            print(f"✅ Successfully switched to {name}")
        except Exception as e:
            print(f"❌ Failed to switch to {name}: {e}")
            raise
    
    def _build_system_prompt(self, action: str) -> str:
        """Build system prompt based on personality level"""
        personality = PERSONALITIES.get(self.personality_level, PERSONALITIES[3])
        base_prompt = personality["system"]
        
        context = self.context.detect_current()
        context_info = f"""
CURRENT CONTEXT:
- Project Type: {context.get('project_type', 'unknown')}
- Language: {context.get('language', 'unknown')}
- Framework: {context.get('framework', 'unknown')}
- Files: {', '.join(context.get('files_detected', [])[:5])}
"""
        
        return f"{base_prompt}\n\n{context_info}\n\nACTION: {action}"
    
    def _think(self, action: str, context: Dict, user_message: str) -> str:
        """Internal thinking method with error handling"""
        try:
            system_prompt = self._build_system_prompt(action)
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context: {context}\n\nQuery: {user_message}"}
            ]
            
            response = self.provider.chat(messages, max_tokens=800, temperature=0.7)
            return response
            
        except Exception as e:
            print(f"❌ Brain thinking failed: {e}")
            return f"ERROR: Brain processing failed - {str(e)}"
    
    def analyse(self, code: str = None, file: str = None) -> str:
        """Analyze code or file"""
        if file:
            context = {"file": file}
            code = self.context.load_file(file)
        else:
            context = {"inline_code": True}
        
        return self._think("analyse", context, f"Analyze this code:\n{code}")
    
    def suggest(self, context: str = None) -> str:
        """Get AI suggestions"""
        return self._think("suggest", {"context": context}, context or "Provide suggestions")
    
    def improve(self, code: str = None, file: str = None, focus: str = None) -> str:
        """Improve code"""
        if file:
            context = {"file": file, "focus": focus}
            code = self.context.load_file(file)
        else:
            context = {"inline_code": True, "focus": focus}
        
        return self._think("improve", context, f"Improve this code{f' focusing on {focus}' if focus else ''}:\n{code}")
    
    def summary(self) -> Dict:
        """Get brain summary"""
        return {
            "provider": self.provider_name,
            "model": self.provider.model,
            "personality_level": self.personality_level,
            "session_cost": self.session_cost,
            "context": self.context.detect_current()
        }

def get_brain(provider: str = None):
    """Get a Brain instance"""
    return Brain(provider=provider)

# Legacy aliases
def get_provider(provider_name: str):
    """Get provider instance (legacy)"""
    return get_brain(provider_name)

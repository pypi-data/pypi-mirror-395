"""Security utilities for Sonora v1.2.7."""

import hashlib
import json
import os
import secrets
import time
from typing import Any, Dict, List, Optional, Set

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from .exceptions import SonoraError


class CredentialVault:
    """Enterprise-grade encrypted credential vault."""

    def __init__(self, master_key: Optional[str] = None, vault_path: Optional[str] = None):
        self._master_key = master_key or self._generate_master_key()
        self._vault_path = vault_path or ".sonora_vault"
        self._fernet = self._create_fernet()
        self._credentials: Dict[str, str] = {}
        self._load_vault()

    def _generate_master_key(self) -> bytes:
        """Generate a cryptographically secure master key."""
        return secrets.token_bytes(32)

    def _create_fernet(self) -> Fernet:
        """Create Fernet cipher with AES encryption."""
        import base64

        if isinstance(self._master_key, str):
            salt = b'sonora_vault_salt_v2'
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=200000,  # Increased iterations for security
            )
            key_bytes = kdf.derive(self._master_key.encode())
        else:
            key_bytes = self._master_key

        if len(key_bytes) != 32:
            key_bytes = key_bytes[:32] if len(key_bytes) > 32 else key_bytes + b'\x00' * (32 - len(key_bytes))

        key_b64 = base64.urlsafe_b64encode(key_bytes)
        return Fernet(key_b64)

    def _load_vault(self) -> None:
        """Load encrypted credentials from vault file."""
        try:
            if os.path.exists(self._vault_path):
                with open(self._vault_path, 'rb') as f:
                    encrypted_data = f.read()
                decrypted_data = self._fernet.decrypt(encrypted_data)
                self._credentials = json.loads(decrypted_data.decode())
        except Exception:
            # If vault is corrupted, start fresh
            self._credentials = {}

    def _save_vault(self) -> None:
        """Save credentials to encrypted vault file."""
        try:
            data = json.dumps(self._credentials).encode()
            encrypted_data = self._fernet.encrypt(data)
            with open(self._vault_path, 'wb') as f:
                f.write(encrypted_data)
        except Exception as e:
            raise SonoraError(f"Failed to save credential vault: {e}")

    def store_credential(self, key: str, credential: str) -> None:
        """Store an encrypted credential."""
        self._credentials[key] = self._fernet.encrypt(credential.encode()).decode()
        self._save_vault()

    def retrieve_credential(self, key: str) -> Optional[str]:
        """Retrieve and decrypt a credential."""
        if key not in self._credentials:
            return None
        try:
            encrypted = self._credentials[key].encode()
            decrypted = self._fernet.decrypt(encrypted)
            return decrypted.decode()
        except Exception:
            return None

    def delete_credential(self, key: str) -> bool:
        """Delete a credential from vault."""
        if key in self._credentials:
            del self._credentials[key]
            self._save_vault()
            return True
        return False

    def list_credentials(self) -> List[str]:
        """List all credential keys (not values)."""
        return list(self._credentials.keys())

    def rotate_master_key(self, new_master_key: str) -> None:
        """Rotate the master encryption key."""
        # Decrypt all credentials with old key
        old_credentials = {}
        for key, encrypted in self._credentials.items():
            try:
                decrypted = self._fernet.decrypt(encrypted.encode()).decode()
                old_credentials[key] = decrypted
            except Exception:
                continue

        # Create new Fernet with new key
        self._master_key = new_master_key
        self._fernet = self._create_fernet()

        # Re-encrypt with new key
        self._credentials = {}
        for key, credential in old_credentials.items():
            self._credentials[key] = self._fernet.encrypt(credential.encode()).decode()

        self._save_vault()


class SecureDeserializationLayer:
    """Secure deserialization with type validation and size limits."""

    def __init__(self, max_size: int = 10 * 1024 * 1024):  # 10MB default
        self.max_size = max_size
        self.allowed_types = {
            'str', 'int', 'float', 'bool', 'list', 'dict', 'NoneType'
        }

    def safe_json_loads(self, data: str) -> Any:
        """Safely deserialize JSON with size and type validation."""
        if len(data) > self.max_size:
            raise SonoraError("JSON payload too large")

        try:
            obj = json.loads(data)
            self._validate_object(obj)
            return obj
        except json.JSONDecodeError as e:
            raise SonoraError(f"Invalid JSON: {e}")

    def _validate_object(self, obj: Any, depth: int = 0) -> None:
        """Recursively validate object structure."""
        if depth > 100:  # Prevent deep recursion
            raise SonoraError("Object too deeply nested")

        obj_type = type(obj).__name__
        if obj_type not in self.allowed_types:
            raise SonoraError(f"Disallowed type: {obj_type}")

        if isinstance(obj, dict):
            for key, value in obj.items():
                if not isinstance(key, str):
                    raise SonoraError("Dict keys must be strings")
                self._validate_object(value, depth + 1)
        elif isinstance(obj, list):
            for item in obj:
                self._validate_object(item, depth + 1)


class PluginFirewall:
    """Advanced plugin execution firewall."""

    def __init__(self):
        self.allowed_modules = {
            'asyncio', 'typing', 'collections', 'datetime', 'json', 're',
            'math', 'random', 'string', 'functools', 'itertools',
            'sonora.track', 'sonora.events', 'sonora.exceptions'
        }
        self.blocked_functions = {
            'exec', 'eval', 'compile', '__import__', 'open', 'file',
            'input', 'raw_input', 'reload', 'importlib.import_module'
        }
        self.max_execution_time = 30.0  # seconds
        self.max_memory_usage = 100 * 1024 * 1024  # 100MB

    def validate_code(self, code: str) -> List[str]:
        """Validate plugin code for security violations."""
        violations = []

        # Check for dangerous patterns
        for func in self.blocked_functions:
            if f"{func}(" in code:
                violations.append(f"Blocked function call: {func}")

        # Check for dangerous imports
        lines = code.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('import ') or line.startswith('from '):
                module = line.split()[1].split('.')[0]
                if module not in self.allowed_modules and not module.startswith('sonora.'):
                    violations.append(f"Blocked import: {module}")

        # Check for file system access
        dangerous_paths = ['/', './', '../', '~', 'C:', 'D:']
        for path in dangerous_paths:
            if path in code:
                violations.append(f"Potential file system access: {path}")

        return violations

    def create_sandbox(self) -> Dict[str, Any]:
        """Create a restricted execution environment."""
        import builtins

        # Restricted builtins
        safe_builtins = {
            name: getattr(builtins, name)
            for name in dir(builtins)
            if not name.startswith('_') and name not in {
                'exec', 'eval', 'compile', 'open', 'file', 'input',
                'raw_input', 'reload', '__import__'
            }
        }

        return {
            '__builtins__': safe_builtins,
            'len': len,
            'str': str,
            'int': int,
            'float': float,
            'bool': bool,
            'list': list,
            'dict': dict,
            'tuple': tuple,
            'set': set,
            'range': range,
            'enumerate': enumerate,
            'zip': zip,
            'sorted': sorted,
            'min': min,
            'max': max,
            'sum': sum,
            'abs': abs,
            'round': round,
            'print': print,
        }


# Legacy compatibility
CredentialManager = CredentialVault


class AutoplaySecurityManager:
    """Security manager for autoplay features."""

    def __init__(self):
        self.allowlist: Set[str] = set()
        self.denylist: Set[str] = set()
        self.max_requests_per_minute = 60
        self.request_counts: Dict[str, List[float]] = {}

    def add_to_allowlist(self, source: str) -> None:
        """Add a source to the allowlist."""
        self.allowlist.add(source.lower())

    def add_to_denylist(self, source: str) -> None:
        """Add a source to the denylist."""
        self.denylist.add(source.lower())

    def is_allowed(self, source: str) -> bool:
        """Check if a source is allowed."""
        source_lower = source.lower()

        # Check denylist first
        if source_lower in self.denylist:
            return False

        # If allowlist is empty, allow all (except denied)
        if not self.allowlist:
            return True

        # Check allowlist
        return source_lower in self.allowlist

    def check_rate_limit(self, source: str) -> bool:
        """Check if source is within rate limits."""
        now = time.time()
        if source not in self.request_counts:
            self.request_counts[source] = []

        # Clean old requests
        self.request_counts[source] = [
            t for t in self.request_counts[source]
            if now - t < 60  # Last minute
        ]

        # Check rate limit
        if len(self.request_counts[source]) >= self.max_requests_per_minute:
            return False

        # Record request
        self.request_counts[source].append(now)
        return True

    def reset_rate_limits(self) -> None:
        """Reset all rate limit counters."""
        self.request_counts.clear()


class PluginSecurityManager:
    """Security manager for plugins."""

    def __init__(self):
        self.allowed_imports: Set[str] = {
            'asyncio', 'typing', 'collections', 'datetime', 'json', 're',
            'sonora.track', 'sonora.events', 'sonora.exceptions'
        }
        self.blocked_modules: Set[str] = {
            'os', 'sys', 'subprocess', 'socket', 'urllib', 'http',
            'ssl', 'cryptography', 'hashlib', 'secrets'
        }

    def is_import_allowed(self, module_name: str) -> bool:
        """Check if a module import is allowed."""
        if module_name in self.blocked_modules:
            return False

        # Allow sonora.* modules
        if module_name.startswith('sonora.'):
            return True

        return module_name in self.allowed_imports

    def validate_plugin_code(self, code: str) -> List[str]:
        """Validate plugin code for security issues."""
        issues = []

        # Check for dangerous patterns
        dangerous_patterns = [
            'exec(', 'eval(', 'import os', 'import sys',
            'import subprocess', 'import socket', '__import__(',
            'open(', 'file(', 'input('
        ]

        for pattern in dangerous_patterns:
            if pattern in code:
                issues.append(f"Dangerous pattern detected: {pattern}")

        return issues


# Global security managers
credential_manager = CredentialManager()
autoplay_security = AutoplaySecurityManager()
plugin_security = PluginSecurityManager()
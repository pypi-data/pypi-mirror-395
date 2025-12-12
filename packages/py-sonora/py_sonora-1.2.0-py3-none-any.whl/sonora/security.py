"""Security utilities for Sonora v1.2.0."""

import hashlib
import secrets
import time
from typing import Dict, List, Optional, Set

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from .exceptions import SonoraError


class CredentialManager:
    """Secure credential storage and retrieval."""

    def __init__(self, master_key: Optional[str] = None):
        self._master_key = master_key or self._generate_master_key()
        self._fernet = self._create_fernet()

    def _generate_master_key(self) -> bytes:
        """Generate a secure master key."""
        return secrets.token_bytes(32)

    def _create_fernet(self) -> Fernet:
        """Create Fernet cipher from master key."""
        import base64

        # Generate a proper Fernet key (32 bytes base64 encoded)
        if isinstance(self._master_key, str):
            # Use string key to derive
            salt = b'sonora_credentials_salt'
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key_bytes = kdf.derive(self._master_key.encode())
        else:
            # Use bytes directly
            key_bytes = self._master_key

        # Ensure it's exactly 32 bytes
        if len(key_bytes) != 32:
            key_bytes = key_bytes[:32] if len(key_bytes) > 32 else key_bytes + b'\x00' * (32 - len(key_bytes))

        # Base64 encode for Fernet
        key_b64 = base64.urlsafe_b64encode(key_bytes)
        return Fernet(key_b64)

    def encrypt_credential(self, credential: str) -> str:
        """Encrypt a credential."""
        encrypted = self._fernet.encrypt(credential.encode())
        return encrypted.decode()

    def decrypt_credential(self, encrypted_credential: str) -> str:
        """Decrypt a credential."""
        try:
            decrypted = self._fernet.decrypt(encrypted_credential.encode())
            return decrypted.decode()
        except Exception as e:
            raise SonoraError(f"Failed to decrypt credential: {e}")

    def hash_sensitive_data(self, data: str) -> str:
        """Hash sensitive data for logging."""
        return hashlib.sha256(data.encode()).hexdigest()[:16]


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
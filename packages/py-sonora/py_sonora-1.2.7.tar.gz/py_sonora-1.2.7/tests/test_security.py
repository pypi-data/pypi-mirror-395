"""Tests for security utilities."""

import pytest

from sonora.security import (
    AutoplaySecurityManager,
    CredentialManager,
    PluginSecurityManager,
)


class TestCredentialManager:
    """Test credential encryption and management."""

    def test_encrypt_decrypt(self):
        """Test credential encryption and decryption."""
        manager = CredentialManager("test_key_12345")

        credential = "secret_password"
        encrypted = manager.encrypt_credential(credential)
        decrypted = manager.decrypt_credential(encrypted)

        assert decrypted == credential
        assert encrypted != credential

    def test_hash_sensitive_data(self):
        """Test sensitive data hashing."""
        manager = CredentialManager()

        data = "sensitive_info"
        hashed = manager.hash_sensitive_data(data)

        assert len(hashed) == 16
        assert hashed.isalnum()

        # Same input should produce same hash
        hashed2 = manager.hash_sensitive_data(data)
        assert hashed == hashed2


class TestAutoplaySecurityManager:
    """Test autoplay security features."""

    def test_allowlist_denylist(self):
        """Test source filtering."""
        manager = AutoplaySecurityManager()

        # Test denylist
        manager.add_to_denylist("badsite.com")
        assert not manager.is_allowed("badsite.com")
        assert manager.is_allowed("goodsite.com")

        # Test allowlist
        manager.allowlist.add("goodsite.com")
        assert manager.is_allowed("goodsite.com")
        assert not manager.is_allowed("unknownsite.com")

    def test_rate_limiting(self):
        """Test rate limiting."""
        manager = AutoplaySecurityManager()
        manager.max_requests_per_minute = 2

        source = "test.com"

        # First two requests should be allowed
        assert manager.check_rate_limit(source)
        assert manager.check_rate_limit(source)

        # Third should be denied
        assert not manager.check_rate_limit(source)

    def test_rate_limit_reset(self):
        """Test rate limit reset."""
        manager = AutoplaySecurityManager()
        manager.max_requests_per_minute = 1

        source = "test.com"
        assert manager.check_rate_limit(source)
        assert not manager.check_rate_limit(source)

        # Reset and try again
        manager.reset_rate_limits()
        assert manager.check_rate_limit(source)


class TestPluginSecurityManager:
    """Test plugin security validation."""

    def test_import_validation(self):
        """Test import permission checking."""
        manager = PluginSecurityManager()

        # Allowed imports
        assert manager.is_import_allowed("asyncio")
        assert manager.is_import_allowed("sonora.track")
        assert manager.is_import_allowed("json")

        # Blocked imports
        assert not manager.is_import_allowed("os")
        assert not manager.is_import_allowed("subprocess")
        assert not manager.is_import_allowed("socket")

    def test_code_validation(self):
        """Test plugin code security validation."""
        manager = PluginSecurityManager()

        # Safe code
        safe_code = "def plugin_function(): return 'safe'"
        issues = manager.validate_plugin_code(safe_code)
        assert len(issues) == 0

        # Dangerous code
        dangerous_code = "import os; os.system('rm -rf /')"
        issues = manager.validate_plugin_code(dangerous_code)
        assert len(issues) > 0
        assert "dangerous" in " ".join(issues).lower()
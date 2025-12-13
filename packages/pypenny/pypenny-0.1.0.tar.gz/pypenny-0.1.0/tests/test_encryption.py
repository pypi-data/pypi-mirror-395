"""
Tests for encryption utilities
"""

import pytest
from pypenny.encryption_utils import CacheEncryption
from pypenny.exceptions import EncryptionError


class TestCacheEncryptionInit:
    """Test encryption initialization"""
    
    def test_requires_application_name(self):
        """Should require application name"""
        with pytest.raises(EncryptionError, match="application_name is required"):
            CacheEncryption("")
    
    def test_creates_key_automatically(self):
        """Should create encryption key automatically"""
        enc = CacheEncryption("TestApp")
        assert enc._key is not None
        assert enc._fernet is not None
    
    def test_key_path_uses_platformdirs(self):
        """Key path should use platformdirs"""
        enc = CacheEncryption("TestApp")
        key_path = enc.get_key_path()
        
        assert key_path.exists()
        assert key_path.name == "cache.key"
        assert "TestApp" in str(key_path)


class TestEncryptDecrypt:
    """Test encryption and decryption"""
    
    def test_encrypt_decrypt_roundtrip(self):
        """Should encrypt and decrypt successfully"""
        enc = CacheEncryption("TestApp")
        original = '{"test": "data", "number": 123}'
        
        encrypted = enc.encrypt(original)
        assert isinstance(encrypted, bytes)
        assert encrypted != original.encode()
        
        decrypted = enc.decrypt(encrypted)
        assert decrypted == original
    
    def test_encrypted_data_not_readable(self):
        """Encrypted data should not contain plaintext"""
        enc = CacheEncryption("TestApp")
        data = '{"USD_EGP": [{"rate": "49.25"}]}'
        
        encrypted = enc.encrypt(data)
        
        # Should not contain plaintext
        assert b'USD_EGP' not in encrypted
        assert b'49.25' not in encrypted
        assert b'rate' not in encrypted
    
    def test_encrypt_requires_string(self):
        """Encrypt should require string input"""
        enc = CacheEncryption("TestApp")
        
        with pytest.raises(EncryptionError, match="Data must be string"):
            enc.encrypt(123)
        
        with pytest.raises(EncryptionError, match="Data must be string"):
            enc.encrypt(b'bytes')
    
    def test_decrypt_requires_bytes(self):
        """Decrypt should require bytes input"""
        enc = CacheEncryption("TestApp")
        
        with pytest.raises(EncryptionError, match="Encrypted data must be bytes"):
            enc.decrypt("string")
    
    def test_decrypt_invalid_data_raises_error(self):
        """Decrypting invalid data should raise error"""
        enc = CacheEncryption("TestApp")
        
        with pytest.raises(EncryptionError, match="Decryption failed"):
            enc.decrypt(b'invalid encrypted data')


class TestKeyManagement:
    """Test encryption key management"""
    
    def test_generate_key(self):
        """Should generate valid Fernet key"""
        enc = CacheEncryption("TestApp")
        key = enc.generate_key()
        
        assert isinstance(key, bytes)
        assert len(key) > 0
    
    def test_load_existing_key(self, tmp_path):
        """Should load existing key from file"""
        # Create first instance
        enc1 = CacheEncryption("TestApp1")
        key1 = enc1._key
        
        # Create second instance (should load same key)
        enc2 = CacheEncryption("TestApp1")
        key2 = enc2._key
        
        assert key1 == key2
    
    def test_different_apps_have_different_keys(self):
        """Different applications should have different keys"""
        enc1 = CacheEncryption("App1")
        enc2 = CacheEncryption("App2")
        
        assert enc1._key != enc2._key
    
    def test_rotate_key(self):
        """Should rotate encryption key"""
        enc = CacheEncryption("TestApp")
        old_key = enc._key
        
        new_key = enc.rotate_key()
        
        assert new_key != old_key
        assert enc._key == new_key
    
    def test_rotate_key_with_custom_key(self):
        """Should rotate to custom key"""
        enc = CacheEncryption("TestApp")
        custom_key = enc.generate_key()
        
        enc.rotate_key(custom_key)
        
        assert enc._key == custom_key


class TestEncryptionSecurity:
    """Test encryption security features"""
    
    def test_key_file_permissions(self):
        """Key file should have restricted permissions (Unix only)"""
        import platform
        
        enc = CacheEncryption("TestApp")
        key_path = enc.get_key_path()
        
        if platform.system() != 'Windows':
            # Check file permissions (should be 0o600)
            import stat
            mode = key_path.stat().st_mode
            permissions = stat.S_IMODE(mode)
            # Should be readable/writable by owner only
            assert permissions == 0o600
    
    def test_different_data_produces_different_ciphertext(self):
        """Same key should produce different ciphertext for different data"""
        enc = CacheEncryption("TestApp")
        
        encrypted1 = enc.encrypt("data1")
        encrypted2 = enc.encrypt("data2")
        
        assert encrypted1 != encrypted2
    
    def test_same_data_produces_different_ciphertext(self):
        """Same data encrypted twice should produce different ciphertext (IV)"""
        enc = CacheEncryption("TestApp")
        
        data = "same data"
        encrypted1 = enc.encrypt(data)
        encrypted2 = enc.encrypt(data)
        
        # Fernet includes timestamp, so ciphertext will differ
        assert encrypted1 != encrypted2
        
        # But both should decrypt to same value
        assert enc.decrypt(encrypted1) == data
        assert enc.decrypt(encrypted2) == data


class TestUnicodeSupport:
    """Test Unicode and special character support"""
    
    def test_encrypt_decrypt_unicode(self):
        """Should handle Unicode characters"""
        enc = CacheEncryption("TestApp")
        
        unicode_data = '{"arabic": "مرحبا", "chinese": "你好", "emoji": "🎉"}'
        
        encrypted = enc.encrypt(unicode_data)
        decrypted = enc.decrypt(encrypted)
        
        assert decrypted == unicode_data
    
    def test_encrypt_decrypt_special_chars(self):
        """Should handle special characters"""
        enc = CacheEncryption("TestApp")
        
        special_data = '{"chars": "!@#$%^&*()_+-=[]{}|;:,.<>?"}'
        
        encrypted = enc.encrypt(special_data)
        decrypted = enc.decrypt(encrypted)
        
        assert decrypted == special_data

"""
Encryption Utilities for Cache Security

Provides Fernet symmetric encryption for exchange rate cache with
cross-platform key storage via platformdirs.
"""

import os
from pathlib import Path
from typing import Optional
from cryptography.fernet import Fernet
import platformdirs
from .exceptions import EncryptionError


class CacheEncryption:
    """
    Handles encryption/decryption of cache data using Fernet (AES-128).
    
    Features:
    - Automatic key generation and storage
    - Cross-platform key location via platformdirs
    - Simple encrypt/decrypt interface
    
    Example:
        >>> enc = CacheEncryption("MyApp")
        >>> encrypted = enc.encrypt('{"test": "data"}')
        >>> decrypted = enc.decrypt(encrypted)
    """
    
    def __init__(self, application_name: str):
        """
        Initialize encryption with application name for key storage.
        
        Args:
            application_name: Application identifier for platformdirs
        
        Raises:
            EncryptionError: If key cannot be loaded or created
        """
        if not application_name:
            raise EncryptionError(
                "application_name is required for encryption",
                operation="init"
            )
        
        self.application_name = application_name
        self._key: Optional[bytes] = None
        self._fernet: Optional[Fernet] = None
        
        # Load or create encryption key
        try:
            self._key = self.load_or_create_key()
            self._fernet = Fernet(self._key)
        except Exception as e:
            raise EncryptionError(
                f"Failed to initialize encryption: {e}",
                operation="init"
            )
    
    def get_key_path(self) -> Path:
        """
        Get platform-specific path for encryption key storage.
        
        Returns:
            Path to key file
        
        Locations:
            - Windows: C:\\Users\\<user>\\AppData\\Local\\<app>\\cache.key
            - Linux: ~/.local/share/<app>/cache.key
            - macOS: ~/Library/Application Support/<app>/cache.key
        """
        # Use user data directory for key storage
        data_dir = platformdirs.user_data_dir(
            appname=self.application_name,
            appauthor=False
        )
        
        key_dir = Path(data_dir)
        key_dir.mkdir(parents=True, exist_ok=True)
        
        return key_dir / "cache.key"
    
    def generate_key(self) -> bytes:
        """
        Generate a new Fernet encryption key.
        
        Returns:
            32-byte URL-safe base64-encoded key
        """
        return Fernet.generate_key()
    
    def load_or_create_key(self) -> bytes:
        """
        Load existing encryption key or create a new one.
        
        Returns:
            Encryption key bytes
        
        Raises:
            EncryptionError: If key cannot be loaded or created
        """
        key_path = self.get_key_path()
        
        try:
            if key_path.exists():
                # Load existing key
                with open(key_path, 'rb') as f:
                    key = f.read()
                
                # Validate key format
                try:
                    Fernet(key)  # Will raise if invalid
                    return key
                except Exception:
                    # Invalid key, regenerate
                    pass
            
            # Generate new key
            key = self.generate_key()
            
            # Save key with restricted permissions
            with open(key_path, 'wb') as f:
                f.write(key)
            
            # Set file permissions (read/write for owner only)
            try:
                os.chmod(key_path, 0o600)
            except Exception:
                # Windows doesn't support chmod, ignore
                pass
            
            return key
        
        except Exception as e:
            raise EncryptionError(
                f"Failed to load or create encryption key: {e}",
                operation="load_key"
            )
    
    def encrypt(self, data: str) -> bytes:
        """
        Encrypt string data to bytes.
        
        Args:
            data: String data to encrypt
        
        Returns:
            Encrypted bytes
        
        Raises:
            EncryptionError: If encryption fails
        """
        if not isinstance(data, str):
            raise EncryptionError(
                f"Data must be string, got {type(data).__name__}",
                operation="encrypt"
            )
        
        try:
            return self._fernet.encrypt(data.encode('utf-8'))
        except Exception as e:
            raise EncryptionError(
                f"Encryption failed: {e}",
                operation="encrypt"
            )
    
    def decrypt(self, encrypted_data: bytes) -> str:
        """
        Decrypt bytes to string.
        
        Args:
            encrypted_data: Encrypted bytes
        
        Returns:
            Decrypted string
        
        Raises:
            EncryptionError: If decryption fails
        """
        if not isinstance(encrypted_data, bytes):
            raise EncryptionError(
                f"Encrypted data must be bytes, got {type(encrypted_data).__name__}",
                operation="decrypt"
            )
        
        try:
            decrypted_bytes = self._fernet.decrypt(encrypted_data)
            return decrypted_bytes.decode('utf-8')
        except Exception as e:
            raise EncryptionError(
                f"Decryption failed: {e}. Data may be corrupted or key mismatch.",
                operation="decrypt"
            )
    
    def rotate_key(self, new_key: Optional[bytes] = None) -> bytes:
        """
        Rotate encryption key (advanced feature).
        
        Args:
            new_key: Optional new key (generates if None)
        
        Returns:
            New encryption key
        
        Note:
            This does NOT re-encrypt existing cache data.
            You must manually re-encrypt cached data with the new key.
        """
        if new_key is None:
            new_key = self.generate_key()
        
        # Validate new key
        try:
            Fernet(new_key)
        except Exception as e:
            raise EncryptionError(
                f"Invalid encryption key: {e}",
                operation="rotate_key"
            )
        
        # Save new key
        key_path = self.get_key_path()
        with open(key_path, 'wb') as f:
            f.write(new_key)
        
        # Update instance
        self._key = new_key
        self._fernet = Fernet(new_key)
        
        return new_key

"""
Exchange Rate Cache with Encryption and Metadata

Provides encrypted local storage for exchange rate history with:
- Semi-structured format with metadata
- Deduplication logic (1 record per day if unchanged)
- Automatic cleanup of old records
- Cross-platform cache location via platformdirs
"""

import json
import platformdirs
from pathlib import Path
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional, Dict, List
from dataclasses import dataclass, asdict
from .config import CurrencyConfig
from .encryption_utils import CacheEncryption
from .exceptions import CacheError


@dataclass
class ExchangeRateRecord:
    """Single exchange rate record"""
    rate: str  # Stored as string to preserve precision
    date: str  # ISO format date (YYYY-MM-DD)
    timestamp: str  # ISO format datetime
    provider: str
    record_created_at: str  # When this record was created
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return asdict(self)
    
    @staticmethod
    def from_dict(data: Dict) -> 'ExchangeRateRecord':
        """Create from dictionary"""
        return ExchangeRateRecord(**data)
    
    def get_rate_decimal(self) -> Decimal:
        """Get rate as Decimal"""
        return Decimal(self.rate)


class ExchangeCache:
    """
    Encrypted cache for exchange rate history.
    
    Features:
    - Stores up to max_records per currency pair
    - Deduplication: only 1 record per day if rate unchanged
    - Automatic cleanup of old records
    - Semi-structured format with metadata
    - Encrypted storage via Fernet
    
    Example:
        >>> config = CurrencyConfig(application_name="MyApp")
        >>> cache = ExchangeCache(config)
        >>> cache.store_rate('USD', 'EGP', Decimal('49.25'), 'exchangerate-api')
        >>> rate = cache.get_latest_rate('USD', 'EGP')
    """
    
    def __init__(self, config: CurrencyConfig):
        """
        Initialize exchange cache.
        
        Args:
            config: Currency configuration
        """
        self.config = config
        self.encryption = CacheEncryption(config.application_name)
        self._cache_data: Optional[Dict] = None
        self._cache_loaded = False
        
        # Load cache on initialization
        self._load_cache()
    
    def get_cache_path(self) -> Path:
        """
        Get platform-specific cache file path.
        
        Returns:
            Path to cache file
        
        Locations:
            - Windows: C:\\Users\\<user>\\AppData\\Local\\<app>\\Cache\\exchange_cache.enc
            - Linux: ~/.cache/<app>/exchange_cache.enc
            - macOS: ~/Library/Caches/<app>/exchange_cache.enc
        """
        if self.config.cache_file_path:
            return Path(self.config.cache_file_path)
        
        # Use platformdirs for cache directory
        cache_dir = platformdirs.user_cache_dir(
            appname=self.config.application_name,
            appauthor=False
        )
        
        cache_path = Path(cache_dir)
        cache_path.mkdir(parents=True, exist_ok=True)
        
        return cache_path / "exchange_cache.enc"
    
    def _create_empty_cache(self) -> Dict:
        """Create empty cache structure with metadata"""
        return {
            "metadata": {
                "version": "1.0",
                "application_name": self.config.application_name,
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "total_records": 0,
                "encryption_enabled": True
            },
            "exchange_rates": {}
        }
    
    def _load_cache(self) -> None:
        """Load cache from encrypted file"""
        cache_path = self.get_cache_path()
        
        try:
            if not cache_path.exists():
                self._cache_data = self._create_empty_cache()
                self._cache_loaded = True
                return
            
            # Read encrypted data
            with open(cache_path, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt
            decrypted_json = self.encryption.decrypt(encrypted_data)
            
            # Parse JSON
            self._cache_data = json.loads(decrypted_json)
            self._cache_loaded = True
            
        except Exception as e:
            raise CacheError(
                f"Failed to load cache from {cache_path}: {e}",
                operation="load"
            )
    
    def _save_cache(self) -> None:
        """Save cache to encrypted file"""
        if not self._cache_loaded or self._cache_data is None:
            return
        
        cache_path = self.get_cache_path()
        
        try:
            # Update metadata
            self._cache_data["metadata"]["last_updated"] = datetime.now().isoformat()
            
            # Convert to JSON
            json_data = json.dumps(self._cache_data, indent=2)
            
            # Encrypt
            encrypted_data = self.encryption.encrypt(json_data)
            
            # Write to file
            with open(cache_path, 'wb') as f:
                f.write(encrypted_data)
            
        except Exception as e:
            raise CacheError(
                f"Failed to save cache to {cache_path}: {e}",
                operation="save"
            )
    
    @staticmethod
    def _get_cache_key(base_currency: str, target_currency: str) -> str:
        """Get cache key for currency pair"""
        return f"{base_currency.upper()}_{target_currency.upper()}"
    
    def get_latest_rate(self, base_currency: str, target_currency: str) -> Optional[Decimal]:
        """
        Get most recent cached exchange rate.
        
        Args:
            base_currency: Source currency code
            target_currency: Target currency code
        
        Returns:
            Latest exchange rate as Decimal, or None if not cached
        """
        cache_key = self._get_cache_key(base_currency, target_currency)
        records = self._cache_data["exchange_rates"].get(cache_key, [])
        
        if not records:
            return None
        
        # Get most recent record (last in list)
        latest_record = ExchangeRateRecord.from_dict(records[-1])
        return latest_record.get_rate_decimal()
    
    def get_all_rates(self, base_currency: str, target_currency: str) -> List[ExchangeRateRecord]:
        """
        Get all cached exchange rates for a currency pair.
        
        Args:
            base_currency: Source currency code
            target_currency: Target currency code
        
        Returns:
            List of exchange rate records
        """
        cache_key = self._get_cache_key(base_currency, target_currency)
        records_data = self._cache_data["exchange_rates"].get(cache_key, [])
        
        return [ExchangeRateRecord.from_dict(r) for r in records_data]
    
    def should_update(self, base_currency: str, target_currency: str, new_rate: Decimal) -> bool:
        """
        Check if new exchange rate should be stored.
        
        Deduplication logic:
        - If no records exist: store
        - If last record is from different day: store
        - If last record is from same day but rate changed significantly: store
        - Otherwise: don't store (avoid duplicates)
        
        Args:
            base_currency: Source currency code
            target_currency: Target currency code
            new_rate: New exchange rate
        
        Returns:
            True if should store, False otherwise
        """
        records = self.get_all_rates(base_currency, target_currency)
        
        if not records:
            return True  # No records, store it
        
        latest = records[-1]
        latest_date = datetime.fromisoformat(latest.date).date()
        today = datetime.now().date()
        
        if latest_date != today:
            return True  # Different day, store it
        
        # Same day - check if rate changed significantly
        latest_rate = latest.get_rate_decimal()
        diff_percent = abs((new_rate - latest_rate) / latest_rate * 100)
        
        # Store if difference is greater than 0.01%
        return diff_percent > Decimal('0.01')
    
    def store_rate(
        self,
        base_currency: str,
        target_currency: str,
        rate: Decimal,
        provider: str
    ) -> bool:
        """
        Store exchange rate with deduplication logic.
        
        Args:
            base_currency: Source currency code
            target_currency: Target currency code
            rate: Exchange rate
            provider: Rate provider name
        
        Returns:
            True if stored, False if skipped (duplicate)
        """
        # Check if we should update
        if not self.should_update(base_currency, target_currency, rate):
            return False  # Skip duplicate
        
        cache_key = self._get_cache_key(base_currency, target_currency)
        
        # Create new record
        now = datetime.now()
        record = ExchangeRateRecord(
            rate=str(rate),
            date=now.date().isoformat(),
            timestamp=now.isoformat(),
            provider=provider,
            record_created_at=now.isoformat()
        )
        
        # Get existing records
        if cache_key not in self._cache_data["exchange_rates"]:
            self._cache_data["exchange_rates"][cache_key] = []
        
        records = self._cache_data["exchange_rates"][cache_key]
        
        # Add new record
        records.append(record.to_dict())
        
        # Enforce max_records limit
        if len(records) > self.config.cache_max_records:
            # Remove oldest records
            records[:] = records[-self.config.cache_max_records:]
        
        # Update total count in metadata
        total = sum(len(r) for r in self._cache_data["exchange_rates"].values())
        self._cache_data["metadata"]["total_records"] = total
        
        # Save to disk
        self._save_cache()
        
        return True
    
    def cleanup_old_records(self) -> int:
        """
        Remove records older than retention_days.
        
        Returns:
            Number of records removed
        """
        cutoff_date = datetime.now() - timedelta(days=self.config.cache_retention_days)
        removed_count = 0
        
        for cache_key in list(self._cache_data["exchange_rates"].keys()):
            records = self._cache_data["exchange_rates"][cache_key]
            original_count = len(records)
            
            # Filter out old records
            records[:] = [
                r for r in records
                if datetime.fromisoformat(r["date"]).date() >= cutoff_date.date()
            ]
            
            removed_count += original_count - len(records)
            
            # Remove empty cache keys
            if not records:
                del self._cache_data["exchange_rates"][cache_key]
        
        if removed_count > 0:
            # Update metadata
            total = sum(len(r) for r in self._cache_data["exchange_rates"].values())
            self._cache_data["metadata"]["total_records"] = total
            
            # Save changes
            self._save_cache()
        
        return removed_count
    
    def get_metadata(self) -> Dict:
        """
        Get cache metadata.
        
        Returns:
            Metadata dictionary
        """
        return self._cache_data["metadata"].copy()
    
    def get_cache_stats(self) -> Dict:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        total_records = sum(len(r) for r in self._cache_data["exchange_rates"].values())
        currency_pairs = len(self._cache_data["exchange_rates"])
        
        return {
            "total_records": total_records,
            "currency_pairs": currency_pairs,
            "cache_file": str(self.get_cache_path()),
            "metadata": self.get_metadata()
        }
    
    def clear_cache(self) -> None:
        """Clear all cached exchange rates"""
        self._cache_data = self._create_empty_cache()
        self._save_cache()

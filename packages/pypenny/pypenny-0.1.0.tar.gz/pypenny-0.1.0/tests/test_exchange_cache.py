"""
Tests for exchange cache and deduplication logic
"""

import pytest
from decimal import Decimal
from datetime import datetime, timedelta
from unittest import mock
from pypenny.exchange_cache import ExchangeCache, ExchangeRateRecord
from pypenny.config import CurrencyConfig


@pytest.fixture
def cache_config(tmp_path):
    """Create config with temporary cache path"""
    cache_file = tmp_path / "test_cache.enc"
    return CurrencyConfig(
        application_name="TestApp",
        cache_file_path=str(cache_file),
        cache_max_records=5,
        cache_retention_days=3
    )


class TestExchangeCacheInit:
    """Test cache initialization"""
    
    def test_creates_cache_file(self, cache_config):
        """Should create cache file on init"""
        cache = ExchangeCache(cache_config)
        cache_path = cache.get_cache_path()
        
        # Cache file should exist after first save
        cache.store_rate('USD', 'EGP', Decimal('49.25'), 'test')
        assert cache_path.exists()
    
    def test_loads_existing_cache(self, cache_config):
        """Should load existing cache file"""
        # Create cache and store data
        cache1 = ExchangeCache(cache_config)
        cache1.store_rate('USD', 'EGP', Decimal('49.25'), 'test')
        
        # Create new instance (should load existing)
        cache2 = ExchangeCache(cache_config)
        rate = cache2.get_latest_rate('USD', 'EGP')
        
        assert rate == Decimal('49.25')


class TestStoreAndRetrieve:
    """Test storing and retrieving rates"""
    
    def test_store_rate(self, cache_config):
        """Should store exchange rate"""
        cache = ExchangeCache(cache_config)
        result = cache.store_rate('USD', 'EGP', Decimal('49.25'), 'test')
        
        assert result is True  # Stored
        rate = cache.get_latest_rate('USD', 'EGP')
        assert rate == Decimal('49.25')
    
    def test_get_latest_rate_returns_none_when_empty(self, cache_config):
        """Should return None when no rate cached"""
        cache = ExchangeCache(cache_config)
        rate = cache.get_latest_rate('USD', 'EUR')
        
        assert rate is None
    
    def test_get_all_rates(self, cache_config):
        """Should return all rates for currency pair"""
        cache = ExchangeCache(cache_config)
        
        # Store multiple rates
        with mock.patch('pypenny.exchange_cache.datetime') as mock_dt:
            # Yesterday
            mock_dt.now.return_value = datetime.now() - timedelta(days=1)
            cache.store_rate('USD', 'EGP', Decimal('49.00'), 'test')
            
            # Today
            mock_dt.now.return_value = datetime.now()
            cache.store_rate('USD', 'EGP', Decimal('49.25'), 'test')
        
        rates = cache.get_all_rates('USD', 'EGP')
        assert len(rates) == 2
        assert rates[0].get_rate_decimal() == Decimal('49.00')
        assert rates[1].get_rate_decimal() == Decimal('49.25')


class TestDeduplication:
    """Test deduplication logic"""
    
    def test_same_day_same_rate_no_duplicate(self, cache_config):
        """Should not create duplicate for same rate on same day"""
        cache = ExchangeCache(cache_config)
        
        # Store first rate
        result1 = cache.store_rate('USD', 'EGP', Decimal('49.25'), 'test')
        assert result1 is True
        
        # Try to store same rate same day
        result2 = cache.store_rate('USD', 'EGP', Decimal('49.25'), 'test')
        assert result2 is False  # Not stored (duplicate)
        
        # Should only have 1 record
        rates = cache.get_all_rates('USD', 'EGP')
        assert len(rates) == 1
    
    def test_same_day_different_rate_creates_record(self, cache_config):
        """Should create new record if rate changed significantly"""
        cache = ExchangeCache(cache_config)
        
        cache.store_rate('USD', 'EGP', Decimal('49.25'), 'test')
        cache.store_rate('USD', 'EGP', Decimal('49.50'), 'test')  # Changed
        
        rates = cache.get_all_rates('USD', 'EGP')
        assert len(rates) == 2
    
    def test_different_day_creates_record(self, cache_config):
        """Should create new record for different day"""
        cache = ExchangeCache(cache_config)
        
        # Mock yesterday
        with mock.patch('pypenny.exchange_cache.datetime') as mock_dt:
            mock_dt.now.return_value = datetime.now() - timedelta(days=1)
            cache.store_rate('USD', 'EGP', Decimal('49.25'), 'test')
        
        # Today (same rate)
        cache.store_rate('USD', 'EGP', Decimal('49.25'), 'test')
        
        rates = cache.get_all_rates('USD', 'EGP')
        assert len(rates) == 2
    
    def test_should_update_logic(self, cache_config):
        """Test should_update method"""
        cache = ExchangeCache(cache_config)
        
        # No records - should update
        assert cache.should_update('USD', 'EGP', Decimal('49.25')) is True
        
        # Store first record
        cache.store_rate('USD', 'EGP', Decimal('49.25'), 'test')
        
        # Same day, same rate - should not update
        assert cache.should_update('USD', 'EGP', Decimal('49.25')) is False
        
        # Same day, different rate - should update
        assert cache.should_update('USD', 'EGP', Decimal('49.50')) is True


class TestMaxRecordsLimit:
    """Test max records enforcement"""
    
    def test_enforces_max_records_limit(self, cache_config):
        """Should enforce max_records limit"""
        cache = ExchangeCache(cache_config)
        
        # Store more than max_records (5)
        with mock.patch('pypenny.exchange_cache.datetime') as mock_dt:
            for i in range(7):
                mock_dt.now.return_value = datetime.now() - timedelta(days=6-i)
                cache.store_rate('USD', 'EGP', Decimal(f'49.{i}'), 'test')
        
        rates = cache.get_all_rates('USD', 'EGP')
        assert len(rates) == 5  # Should be limited to max_records
        
        # Should keep most recent records
        assert rates[-1].get_rate_decimal() == Decimal('49.6')


class TestCleanup:
    """Test old record cleanup"""
    
    def test_cleanup_old_records(self, cache_config):
        """Should remove records older than retention_days"""
        cache = ExchangeCache(cache_config)
        
        # Store old and new records
        with mock.patch('pypenny.exchange_cache.datetime') as mock_dt:
            # Old record (5 days ago, beyond retention)
            mock_dt.now.return_value = datetime.now() - timedelta(days=5)
            cache.store_rate('USD', 'EGP', Decimal('49.00'), 'test')
            
            # Recent record (1 day ago, within retention)
            mock_dt.now.return_value = datetime.now() - timedelta(days=1)
            cache.store_rate('USD', 'EGP', Decimal('49.25'), 'test')
        
        # Cleanup
        removed = cache.cleanup_old_records()
        
        assert removed == 1  # Should remove 1 old record
        rates = cache.get_all_rates('USD', 'EGP')
        assert len(rates) == 1
        assert rates[0].get_rate_decimal() == Decimal('49.25')
    
    def test_cleanup_returns_zero_when_nothing_to_remove(self, cache_config):
        """Should return 0 when no old records"""
        cache = ExchangeCache(cache_config)
        cache.store_rate('USD', 'EGP', Decimal('49.25'), 'test')
        
        removed = cache.cleanup_old_records()
        assert removed == 0


class TestMetadata:
    """Test cache metadata"""
    
    def test_metadata_creation(self, cache_config):
        """Should create metadata on init"""
        cache = ExchangeCache(cache_config)
        metadata = cache.get_metadata()
        
        assert metadata['version'] == '1.0'
        assert metadata['application_name'] == 'TestApp'
        assert 'created_at' in metadata
        assert 'last_updated' in metadata
        assert metadata['total_records'] == 0
        assert metadata['encryption_enabled'] is True
    
    def test_metadata_updates_on_store(self, cache_config):
        """Should update metadata when storing rates"""
        cache = ExchangeCache(cache_config)
        
        initial_meta = cache.get_metadata()
        initial_count = initial_meta['total_records']
        
        cache.store_rate('USD', 'EGP', Decimal('49.25'), 'test')
        
        updated_meta = cache.get_metadata()
        assert updated_meta['total_records'] == initial_count + 1
    
    def test_cache_stats(self, cache_config):
        """Should provide cache statistics"""
        cache = ExchangeCache(cache_config)
        
        cache.store_rate('USD', 'EGP', Decimal('49.25'), 'test')
        cache.store_rate('EUR', 'USD', Decimal('1.09'), 'test')
        
        stats = cache.get_cache_stats()
        
        assert stats['total_records'] == 2
        assert stats['currency_pairs'] == 2
        assert 'cache_file' in stats
        assert 'metadata' in stats


class TestClearCache:
    """Test cache clearing"""
    
    def test_clear_cache(self, cache_config):
        """Should clear all cached data"""
        cache = ExchangeCache(cache_config)
        
        cache.store_rate('USD', 'EGP', Decimal('49.25'), 'test')
        cache.store_rate('EUR', 'USD', Decimal('1.09'), 'test')
        
        cache.clear_cache()
        
        assert cache.get_latest_rate('USD', 'EGP') is None
        assert cache.get_latest_rate('EUR', 'USD') is None
        
        stats = cache.get_cache_stats()
        assert stats['total_records'] == 0


class TestExchangeRateRecord:
    """Test ExchangeRateRecord dataclass"""
    
    def test_to_dict(self):
        """Should convert to dictionary"""
        record = ExchangeRateRecord(
            rate="49.25",
            date="2025-12-03",
            timestamp="2025-12-03T14:00:00",
            provider="test",
            record_created_at="2025-12-03T14:00:00"
        )
        
        data = record.to_dict()
        assert data['rate'] == "49.25"
        assert data['provider'] == "test"
    
    def test_from_dict(self):
        """Should create from dictionary"""
        data = {
            'rate': "49.25",
            'date': "2025-12-03",
            'timestamp': "2025-12-03T14:00:00",
            'provider': "test",
            'record_created_at': "2025-12-03T14:00:00"
        }
        
        record = ExchangeRateRecord.from_dict(data)
        assert record.rate == "49.25"
        assert record.provider == "test"
    
    def test_get_rate_decimal(self):
        """Should convert rate to Decimal"""
        record = ExchangeRateRecord(
            rate="49.25",
            date="2025-12-03",
            timestamp="2025-12-03T14:00:00",
            provider="test",
            record_created_at="2025-12-03T14:00:00"
        )
        
        rate = record.get_rate_decimal()
        assert isinstance(rate, Decimal)
        assert rate == Decimal('49.25')

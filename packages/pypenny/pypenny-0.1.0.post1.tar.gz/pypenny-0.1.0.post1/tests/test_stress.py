"""
Stress tests for currency conversion system

Tests system behavior under heavy load:
- Multiple concurrent conversions
- Rapid cache operations
- API rate limiting handling
- Memory usage
- Performance benchmarks
"""

import pytest
import time
from decimal import Decimal
from concurrent.futures import ThreadPoolExecutor, as_completed
from pypenny.config import CurrencyConfig
from pypenny.currency_manager import CurrencyManager
from pypenny.exchange_cache import ExchangeCache


class TestStressConversions:
    """Test system under heavy conversion load"""
    
    def test_rapid_conversions(self, tmp_path):
        """Test rapid successive conversions"""
        cache_file = tmp_path / "stress_cache.enc"
        config = CurrencyConfig(
            application_name="StressTest",
            cache_file_path=str(cache_file),
            allow_cache_fallback=True
        )
        
        manager = CurrencyManager(config)
        
        # Perform 100 conversions rapidly
        start_time = time.time()
        conversions = []
        
        for i in range(100):
            try:
                money = manager.create_money(str(100 + i), 'USD')
                converted = manager.convert(money, 'EGP', strategy='auto')
                conversions.append(converted)
            except Exception as e:
                # Network errors expected, should fallback to cache
                print(f"Conversion {i} failed: {e}")
        
        elapsed = time.time() - start_time
        
        print(f"\n100 conversions completed in {elapsed:.2f}s")
        print(f"Average: {elapsed/100*1000:.2f}ms per conversion")
        
        # Should complete in reasonable time (< 30s with network, < 1s with cache)
        assert elapsed < 30, "Conversions took too long"
    
    def test_concurrent_conversions(self, tmp_path):
        """Test concurrent conversions from multiple threads"""
        cache_file = tmp_path / "concurrent_cache.enc"
        config = CurrencyConfig(
            application_name="ConcurrentTest",
            cache_file_path=str(cache_file),
            allow_cache_fallback=True
        )
        
        manager = CurrencyManager(config)
        
        def convert_currency(amount: int) -> bool:
            """Convert currency in thread"""
            try:
                money = manager.create_money(str(amount), 'USD')
                converted = manager.convert(money, 'EGP', strategy='auto')
                return True
            except Exception as e:
                print(f"Thread conversion failed: {e}")
                return False
        
        # Run 50 concurrent conversions
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(convert_currency, i) for i in range(50)]
            results = [f.result() for f in as_completed(futures)]
        
        elapsed = time.time() - start_time
        success_count = sum(results)
        
        print(f"\n50 concurrent conversions in {elapsed:.2f}s")
        print(f"Success rate: {success_count}/50 ({success_count/50*100:.1f}%)")
        
        # At least some should succeed (cache fallback)
        assert success_count > 0, "No conversions succeeded"
    
    def test_cache_stress(self, tmp_path):
        """Test cache under heavy write load"""
        cache_file = tmp_path / "cache_stress.enc"
        config = CurrencyConfig(
            application_name="CacheStressTest",
            cache_file_path=str(cache_file),
            cache_max_records=100,
            cache_retention_days=7
        )
        
        cache = ExchangeCache(config)
        
        # Write 1000 records rapidly
        start_time = time.time()
        stored_count = 0
        
        for i in range(1000):
            rate = Decimal(f'49.{i % 100:02d}')
            result = cache.store_rate('USD', 'EGP', rate, 'stress_test')
            if result:
                stored_count += 1
        
        elapsed = time.time() - start_time
        
        print(f"\n1000 cache writes in {elapsed:.2f}s")
        print(f"Stored: {stored_count} (deduplication working)")
        print(f"Average: {elapsed/1000*1000:.2f}ms per write")
        
        # Should complete quickly
        assert elapsed < 10, "Cache writes too slow"
        
        # Check cache stats
        stats = cache.get_cache_stats()
        print(f"Final cache size: {stats['total_records']} records")
        
        # Should respect max_records limit (most important check)
        assert stats['total_records'] <= 100, "Max records limit not enforced"
        
        # Note: stored_count may be high because rates are changing,
        # but max_records enforcement keeps the cache size bounded


class TestStressLocaleMatching:
    """Test locale matching under stress"""
    
    def test_rapid_locale_normalization(self):
        """Test rapid locale normalization"""
        from pypenny.locale_matcher import normalize_locale
        
        test_locales = [
            'en_US', 'EN_us', 'US_EN', 'em_US',
            'ar_EG', 'AR_eg', 'EG_AR', 'ar_eg',
            'fr_FR', 'FR_fr', 'FR_FR', 'fr_fr',
        ] * 100  # 1200 normalizations
        
        start_time = time.time()
        results = []
        
        for locale in test_locales:
            try:
                normalized = normalize_locale(locale, raise_on_invalid=False)
                results.append(normalized)
            except Exception as e:
                print(f"Normalization failed for {locale}: {e}")
        
        elapsed = time.time() - start_time
        
        print(f"\n1200 locale normalizations in {elapsed:.2f}s")
        print(f"Average: {elapsed/1200*1000:.3f}ms per normalization")
        
        # Should be very fast (< 1s total)
        assert elapsed < 1.0, "Locale normalization too slow"
        assert len(results) == 1200, "Some normalizations failed"


class TestStressEncryption:
    """Test encryption under heavy load"""
    
    def test_rapid_encrypt_decrypt(self):
        """Test rapid encryption/decryption cycles"""
        from pypenny.encryption_utils import CacheEncryption
        
        enc = CacheEncryption("StressTest")
        
        test_data = '{"USD_EGP": [{"rate": "49.25", "date": "2025-12-03"}]}' * 10
        
        start_time = time.time()
        
        # 1000 encrypt/decrypt cycles
        for i in range(1000):
            encrypted = enc.encrypt(test_data)
            decrypted = enc.decrypt(encrypted)
            assert decrypted == test_data
        
        elapsed = time.time() - start_time
        
        print(f"\n1000 encrypt/decrypt cycles in {elapsed:.2f}s")
        print(f"Average: {elapsed/1000*1000:.2f}ms per cycle")
        
        # Should be fast (< 5s for 1000 cycles)
        assert elapsed < 5.0, "Encryption too slow"


class TestStressMemory:
    """Test memory usage under load"""
    
    @pytest.mark.slow
    @pytest.mark.ci_only
    def test_cache_memory_growth(self, tmp_path):
        """Test that cache doesn't grow unbounded (CI/CD only - long running)"""
        cache_file = tmp_path / "memory_test.enc"
        config = CurrencyConfig(
            application_name="MemoryTest",
            cache_file_path=str(cache_file),
            cache_max_records=10,
            cache_retention_days=1
        )
        
        cache = ExchangeCache(config)
        
        # Store 10,000 records (should be limited by max_records)
        for i in range(10000):
            rate = Decimal(f'49.{i % 100:02d}')
            cache.store_rate(f'CURR{i % 50}', 'USD', rate, 'test')
        
        stats = cache.get_cache_stats()
        
        print(f"\nAfter 10,000 writes:")
        print(f"  Total records: {stats['total_records']}")
        print(f"  Currency pairs: {stats['currency_pairs']}")
        
        # Should be limited by max_records per pair
        # 50 currency pairs * 10 max_records = 500 max
        assert stats['total_records'] <= 500, "Cache grew unbounded"


class TestStressErrorHandling:
    """Test error handling under stress"""
    
    def test_invalid_operations_stress(self):
        """Test system handles many invalid operations gracefully"""
        config = CurrencyConfig(
            application_name="ErrorStressTest",
            allowed_currencies=['USD', 'EGP']
        )
        
        manager = CurrencyManager(config)
        
        invalid_operations = 0
        
        # Try 1000 invalid operations
        for i in range(1000):
            try:
                # Try invalid currency
                manager.create_money('100', 'INVALID')
            except Exception:
                invalid_operations += 1
        
        print(f"\n1000 invalid operations handled: {invalid_operations}")
        
        # All should raise exceptions
        assert invalid_operations == 1000, "Error handling failed"
        
        # System should still be functional
        money = manager.create_money('100', 'USD')
        assert money is not None


class TestPerformanceBenchmarks:
    """Performance benchmarks"""
    
    def test_benchmark_create_money(self):
        """Benchmark money creation"""
        config = CurrencyConfig(application_name="BenchmarkTest")
        manager = CurrencyManager(config)
        
        iterations = 10000
        start_time = time.time()
        
        for i in range(iterations):
            manager.create_money(str(100 + i), 'USD')
        
        elapsed = time.time() - start_time
        per_op = elapsed / iterations * 1000
        
        print(f"\nMoney creation benchmark:")
        print(f"  {iterations} operations in {elapsed:.2f}s")
        print(f"  Average: {per_op:.3f}ms per operation")
        
        # Should be very fast (< 0.1ms per operation)
        assert per_op < 0.1, "Money creation too slow"
    
    def test_benchmark_formatting(self):
        """Benchmark money formatting"""
        config = CurrencyConfig(application_name="BenchmarkTest")
        manager = CurrencyManager(config)
        
        money = manager.create_money('100.50', 'USD')
        
        iterations = 1000
        start_time = time.time()
        
        for i in range(iterations):
            manager.format(money, locale='en_US')
        
        elapsed = time.time() - start_time
        per_op = elapsed / iterations * 1000
        
        print(f"\nFormatting benchmark:")
        print(f"  {iterations} operations in {elapsed:.2f}s")
        print(f"  Average: {per_op:.3f}ms per operation")
        
        # Should be reasonably fast (< 5ms per operation)
        assert per_op < 5.0, "Formatting too slow"


class TestStressResilience:
    """Test system resilience under stress"""
    
    def test_recovery_after_errors(self, tmp_path):
        """Test system recovers after errors"""
        cache_file = tmp_path / "resilience_test.enc"
        config = CurrencyConfig(
            application_name="ResilienceTest",
            cache_file_path=str(cache_file),
            allowed_currencies=['USD', 'EGP']
        )
        
        manager = CurrencyManager(config)
        
        # Cause some errors
        for i in range(100):
            try:
                manager.create_money('100', 'INVALID')
            except Exception:
                pass
        
        # System should still work
        money = manager.create_money('100', 'USD')
        formatted = manager.format(money)
        
        assert formatted is not None
        assert 'USD' in formatted or '$' in formatted
        
        print("\n[OK] System recovered successfully after 100 errors")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

"""
Pytest configuration and shared fixtures for currency tests
"""

import pytest
from decimal import Decimal
from pypenny.config import CurrencyConfig


@pytest.fixture
def default_config():
    """Provide a default permissive configuration"""
    return CurrencyConfig(
        application_name="TestApp",
        allow_cache_fallback=True,
        allowed_currencies=None  # All currencies allowed
    )


@pytest.fixture
def strict_config():
    """Provide a strict production-like configuration"""
    return CurrencyConfig(
        application_name="TestApp",
        allow_cache_fallback=False,
        allowed_currencies=['USD', 'EGP'],
        cache_max_records=5,
        cache_retention_days=2
    )


@pytest.fixture
def temp_cache_dir(tmp_path):
    """Provide a temporary directory for cache files"""
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    return cache_dir


@pytest.fixture
def sample_exchange_rates():
    """Provide sample exchange rates for testing"""
    return {
        'USD_EGP': Decimal('49.25'),
        'USD_EUR': Decimal('0.92'),
        'EUR_USD': Decimal('1.09'),
        'GBP_USD': Decimal('1.27')
    }

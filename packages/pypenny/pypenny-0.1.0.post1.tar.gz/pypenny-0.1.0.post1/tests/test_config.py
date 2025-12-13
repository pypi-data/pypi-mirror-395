"""
Tests for CurrencyConfig configuration class
"""

import pytest
from pypenny.config import CurrencyConfig


class TestCurrencyConfigValidation:
    """Test configuration validation"""
    
    def test_requires_application_name(self):
        """Application name is required"""
        with pytest.raises(ValueError, match="application_name is required"):
            CurrencyConfig(application_name="")
    
    def test_application_name_cannot_be_whitespace(self):
        """Application name cannot be only whitespace"""
        with pytest.raises(ValueError, match="application_name is required"):
            CurrencyConfig(application_name="   ")
    
    def test_validates_allowed_currencies(self):
        """Invalid currency codes should raise error"""
        with pytest.raises(ValueError, match="Invalid currency codes"):
            CurrencyConfig(
                application_name="Test",
                allowed_currencies=['USD', 'INVALID', 'XYZ']
            )
    
    def test_allowed_currencies_cannot_be_empty_list(self):
        """Empty allowed_currencies list should raise error"""
        with pytest.raises(ValueError, match="cannot be empty"):
            CurrencyConfig(
                application_name="Test",
                allowed_currencies=[]
            )
    
    def test_validates_exchange_strategy(self):
        """Invalid exchange strategy should raise error"""
        with pytest.raises(ValueError, match="Invalid default_exchange_strategy"):
            CurrencyConfig(
                application_name="Test",
                default_exchange_strategy="invalid"
            )
    
    def test_validates_cache_max_records(self):
        """cache_max_records must be at least 1"""
        with pytest.raises(ValueError, match="cache_max_records must be at least 1"):
            CurrencyConfig(
                application_name="Test",
                cache_max_records=0
            )
    
    def test_validates_cache_retention_days(self):
        """cache_retention_days must be at least 1"""
        with pytest.raises(ValueError, match="cache_retention_days must be at least 1"):
            CurrencyConfig(
                application_name="Test",
                cache_retention_days=0
            )


class TestCurrencyConfigDefaults:
    """Test default configuration values"""
    
    def test_default_values(self):
        """Test all default values are set correctly"""
        config = CurrencyConfig(application_name="Test")
        
        assert config.application_name == "Test"
        assert config.allow_cache_fallback is True
        assert config.cache_max_records == 7
        assert config.cache_retention_days == 3
        assert config.cache_file_path is None
        assert config.allowed_currencies is None
        assert config.default_exchange_strategy == 'auto'
        assert config.default_locale == 'en_US'
        assert config.api_key is None
        assert config.api_timeout == 5
        assert config.api_max_retries == 3


class TestCurrencyConfigMethods:
    """Test configuration helper methods"""
    
    def test_is_currency_allowed_with_no_restrictions(self):
        """When allowed_currencies is None, all currencies are allowed"""
        config = CurrencyConfig(
            application_name="Test",
            allowed_currencies=None
        )
        
        assert config.is_currency_allowed('USD') is True
        assert config.is_currency_allowed('EUR') is True
        assert config.is_currency_allowed('JPY') is True
    
    def test_is_currency_allowed_with_whitelist(self):
        """When allowed_currencies is set, only those are allowed"""
        config = CurrencyConfig(
            application_name="Test",
            allowed_currencies=['USD', 'EGP']
        )
        
        assert config.is_currency_allowed('USD') is True
        assert config.is_currency_allowed('EGP') is True
        assert config.is_currency_allowed('EUR') is False
        assert config.is_currency_allowed('GBP') is False
    
    def test_is_currency_allowed_case_insensitive(self):
        """Currency checking should be case-insensitive"""
        config = CurrencyConfig(
            application_name="Test",
            allowed_currencies=['USD', 'EGP']
        )
        
        assert config.is_currency_allowed('usd') is True
        assert config.is_currency_allowed('Usd') is True
        assert config.is_currency_allowed('egp') is True
    
    def test_get_allowed_currencies_str_with_no_restrictions(self):
        """Should return 'all currencies' when no restrictions"""
        config = CurrencyConfig(
            application_name="Test",
            allowed_currencies=None
        )
        
        assert config.get_allowed_currencies_str() == "all currencies"
    
    def test_get_allowed_currencies_str_with_whitelist(self):
        """Should return comma-separated list when restricted"""
        config = CurrencyConfig(
            application_name="Test",
            allowed_currencies=['USD', 'EUR', 'EGP']
        )
        
        result = config.get_allowed_currencies_str()
        assert 'USD' in result
        assert 'EUR' in result
        assert 'EGP' in result
        assert ', ' in result


class TestCurrencyConfigCustomization:
    """Test custom configuration scenarios"""
    
    def test_strict_production_config(self):
        """Test strict production-like configuration"""
        config = CurrencyConfig(
            application_name="ProductionApp",
            allow_cache_fallback=False,
            allowed_currencies=['USD', 'EGP'],
            cache_max_records=10,
            cache_retention_days=7,
            default_exchange_strategy='live'
        )
        
        assert config.allow_cache_fallback is False
        assert config.allowed_currencies == ['USD', 'EGP']
        assert config.cache_max_records == 10
        assert config.cache_retention_days == 7
        assert config.default_exchange_strategy == 'live'
    
    def test_custom_cache_path(self):
        """Test custom cache file path"""
        config = CurrencyConfig(
            application_name="Test",
            cache_file_path="/custom/path/cache.enc"
        )
        
        assert config.cache_file_path == "/custom/path/cache.enc"

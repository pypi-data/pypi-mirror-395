"""
Tests for custom exception classes
"""

from pypenny.exceptions import (
    CurrencyException,
    ConfigurationError,
    InvalidCurrencyCodeError,
    CurrencyNotAllowedError,
    InvalidLocaleError,
    ExchangeRateUnavailableError,
    CurrencyMismatchError,
    ConversionError,
    CacheError,
    EncryptionError
)


class TestCurrencyException:
    """Test base exception class"""
    
    def test_basic_exception(self):
        """Test basic exception creation"""
        exc = CurrencyException("Test error")
        assert str(exc) == "Test error"
        assert exc.error_code == "CurrencyException"
    
    def test_custom_error_code(self):
        """Test exception with custom error code"""
        exc = CurrencyException("Test error", error_code="CUSTOM_CODE")
        assert exc.error_code == "CUSTOM_CODE"


class TestInvalidCurrencyCodeError:
    """Test invalid currency code exception"""
    
    def test_without_suggestions(self):
        """Test error without suggestions"""
        exc = InvalidCurrencyCodeError("USDD")
        assert "USDD" in str(exc)
        assert exc.currency_code == "USDD"
        assert exc.suggestions == []
    
    def test_with_suggestions(self):
        """Test error with suggestions"""
        exc = InvalidCurrencyCodeError("USDD", suggestions=['USD', 'AUD', 'CAD'])
        message = str(exc)
        assert "USDD" in message
        assert "Did you mean" in message
        assert "USD" in message
        assert exc.suggestions == ['USD', 'AUD', 'CAD']
    
    def test_custom_message(self):
        """Test error with custom message"""
        exc = InvalidCurrencyCodeError("XYZ", message="Custom error message")
        assert str(exc) == "Custom error message"


class TestCurrencyNotAllowedError:
    """Test currency not allowed exception"""
    
    def test_default_message(self):
        """Test default error message"""
        exc = CurrencyNotAllowedError("EUR", ['USD', 'EGP'])
        message = str(exc)
        
        assert "EUR" in message
        assert "not allowed" in message
        assert "USD" in message
        assert "EGP" in message
        assert "config.allowed_currencies" in message
    
    def test_attributes(self):
        """Test exception attributes"""
        exc = CurrencyNotAllowedError("GBP", ['USD', 'EGP'])
        assert exc.currency_code == "GBP"
        assert exc.allowed_currencies == ['USD', 'EGP']


class TestInvalidLocaleError:
    """Test invalid locale exception"""
    
    def test_without_suggestions(self):
        """Test error without suggestions"""
        exc = InvalidLocaleError("xyz_ABC")
        assert "xyz_ABC" in str(exc)
        assert exc.locale == "xyz_ABC"
    
    def test_with_suggestions(self):
        """Test error with suggestions"""
        exc = InvalidLocaleError("em_US", suggestions=['en_US', 'en_GB'])
        message = str(exc)
        assert "em_US" in message
        assert "Did you mean" in message
        assert "en_US" in message


class TestExchangeRateUnavailableError:
    """Test exchange rate unavailable exception"""
    
    def test_basic_error(self):
        """Test basic exchange rate error"""
        exc = ExchangeRateUnavailableError("USD", "EGP")
        message = str(exc)
        assert "USD" in message
        assert "EGP" in message
        assert "unavailable" in message
    
    def test_with_reason(self):
        """Test error with reason"""
        exc = ExchangeRateUnavailableError("USD", "EGP", reason="Network timeout")
        message = str(exc)
        assert "Network timeout" in message
    
    def test_with_cache_fallback_disabled(self):
        """Test error when cache fallback is disabled"""
        exc = ExchangeRateUnavailableError(
            "USD", "EGP",
            cache_fallback_disabled=True
        )
        message = str(exc)
        assert "Cache fallback is disabled" in message
        assert "allow_cache_fallback" in message
    
    def test_attributes(self):
        """Test exception attributes"""
        exc = ExchangeRateUnavailableError("USD", "EUR", reason="API error")
        assert exc.base_currency == "USD"
        assert exc.target_currency == "EUR"
        assert exc.reason == "API error"


class TestCurrencyMismatchError:
    """Test currency mismatch exception"""
    
    def test_default_message(self):
        """Test default error message"""
        exc = CurrencyMismatchError("addition", "USD", "EUR")
        message = str(exc)
        assert "addition" in message
        assert "USD" in message
        assert "EUR" in message
        assert "Convert to the same currency" in message
    
    def test_attributes(self):
        """Test exception attributes"""
        exc = CurrencyMismatchError("subtraction", "GBP", "JPY")
        assert exc.operation == "subtraction"
        assert exc.currency1 == "GBP"
        assert exc.currency2 == "JPY"


class TestConversionError:
    """Test conversion error exception"""
    
    def test_basic_error(self):
        """Test basic conversion error"""
        exc = ConversionError("USD", "EGP")
        message = str(exc)
        assert "USD" in message
        assert "EGP" in message
        assert "Failed to convert" in message
    
    def test_with_reason(self):
        """Test error with reason"""
        exc = ConversionError("USD", "EGP", reason="Invalid rate")
        message = str(exc)
        assert "Invalid rate" in message


class TestCacheError:
    """Test cache error exception"""
    
    def test_basic_error(self):
        """Test basic cache error"""
        exc = CacheError("Failed to read cache")
        assert "Failed to read cache" in str(exc)
        assert exc.operation is None
    
    def test_with_operation(self):
        """Test error with operation"""
        exc = CacheError("Cache write failed", operation="write")
        assert exc.operation == "write"


class TestEncryptionError:
    """Test encryption error exception"""
    
    def test_basic_error(self):
        """Test basic encryption error"""
        exc = EncryptionError("Encryption failed")
        assert "Encryption failed" in str(exc)
    
    def test_with_operation(self):
        """Test error with operation"""
        exc = EncryptionError("Decryption failed", operation="decrypt")
        assert exc.operation == "decrypt"


class TestErrorCodes:
    """Test that all exceptions have proper error codes"""
    
    def test_all_exceptions_have_error_codes(self):
        """Verify all custom exceptions have error codes"""
        exceptions_to_test = [
            (ConfigurationError("test"), "CONFIG_ERROR"),
            (InvalidCurrencyCodeError("USD"), "INVALID_CURRENCY"),
            (CurrencyNotAllowedError("EUR", ['USD']), "CURRENCY_NOT_ALLOWED"),
            (InvalidLocaleError("test"), "INVALID_LOCALE"),
            (ExchangeRateUnavailableError("USD", "EUR"), "EXCHANGE_RATE_UNAVAILABLE"),
            (CurrencyMismatchError("add", "USD", "EUR"), "CURRENCY_MISMATCH"),
            (ConversionError("USD", "EUR"), "CONVERSION_ERROR"),
            (CacheError("test"), "CACHE_ERROR"),
            (EncryptionError("test"), "ENCRYPTION_ERROR"),
        ]
        
        for exc, expected_code in exceptions_to_test:
            assert exc.error_code == expected_code

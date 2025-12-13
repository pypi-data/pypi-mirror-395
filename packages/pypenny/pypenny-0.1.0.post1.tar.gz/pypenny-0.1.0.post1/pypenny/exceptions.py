"""
Custom Exception Hierarchy for Currency Operations

Provides clear, actionable error messages with suggestions for common mistakes.
"""

from typing import Optional, List


class CurrencyException(Exception):
    """Base exception for all currency-related errors"""
    
    def __init__(self, message: str, error_code: Optional[str] = None):
        """
        Initialize currency exception.
        
        Args:
            message: Human-readable error message
            error_code: Machine-readable error code for logging
        """
        super().__init__(message)
        self.error_code = error_code or self.__class__.__name__


class ConfigurationError(CurrencyException):
    """Raised when configuration is invalid"""
    
    def __init__(self, message: str, config_field: Optional[str] = None):
        """
        Initialize configuration error.
        
        Args:
            message: Error description
            config_field: Name of the invalid configuration field
        """
        super().__init__(message, error_code="CONFIG_ERROR")
        self.config_field = config_field


class InvalidCurrencyCodeError(CurrencyException):
    """Raised when an invalid currency code is provided"""
    
    def __init__(
        self,
        currency_code: str,
        suggestions: Optional[List[str]] = None,
        message: Optional[str] = None
    ):
        """
        Initialize invalid currency code error.
        
        Args:
            currency_code: The invalid currency code
            suggestions: List of suggested valid currency codes
            message: Optional custom message
        """
        if message is None:
            message = f"Invalid currency code: '{currency_code}'"
            if suggestions:
                message += f". Did you mean: {', '.join(suggestions[:3])}?"
        
        super().__init__(message, error_code="INVALID_CURRENCY")
        self.currency_code = currency_code
        self.suggestions = suggestions or []


class CurrencyNotAllowedError(CurrencyException):
    """Raised when a currency is not in the allowed currencies list"""
    
    def __init__(
        self,
        currency_code: str,
        allowed_currencies: List[str],
        message: Optional[str] = None
    ):
        """
        Initialize currency not allowed error.
        
        Args:
            currency_code: The disallowed currency code
            allowed_currencies: List of allowed currency codes
            message: Optional custom message
        """
        if message is None:
            allowed_str = ", ".join(sorted(allowed_currencies))
            message = (
                f"Currency '{currency_code}' is not allowed. "
                f"Allowed currencies: {allowed_str}.\n"
                f"To use '{currency_code}', update config.allowed_currencies to include it."
            )
        
        super().__init__(message, error_code="CURRENCY_NOT_ALLOWED")
        self.currency_code = currency_code
        self.allowed_currencies = allowed_currencies


class InvalidLocaleError(CurrencyException):
    """Raised when an invalid locale is provided"""
    
    def __init__(
        self,
        locale: str,
        suggestions: Optional[List[str]] = None,
        message: Optional[str] = None
    ):
        """
        Initialize invalid locale error.
        
        Args:
            locale: The invalid locale string
            suggestions: List of suggested valid locales
            message: Optional custom message
        """
        if message is None:
            message = f"Invalid locale: '{locale}'"
            if suggestions:
                message += f". Did you mean: {', '.join(suggestions[:3])}?"
        
        super().__init__(message, error_code="INVALID_LOCALE")
        self.locale = locale
        self.suggestions = suggestions or []


class ExchangeRateUnavailableError(CurrencyException):
    """Raised when exchange rate cannot be fetched"""
    
    def __init__(
        self,
        base_currency: str,
        target_currency: str,
        reason: Optional[str] = None,
        cache_fallback_disabled: bool = False
    ):
        """
        Initialize exchange rate unavailable error.
        
        Args:
            base_currency: Source currency code
            target_currency: Target currency code
            reason: Optional reason for failure
            cache_fallback_disabled: Whether cache fallback was disabled
        """
        message = f"Exchange rate unavailable for {base_currency}→{target_currency}"
        
        if reason:
            message += f": {reason}"
        
        if cache_fallback_disabled:
            message += (
                "\nCache fallback is disabled (config.allow_cache_fallback=False). "
                "Enable cache fallback for resilience, or ensure network connectivity."
            )
        
        super().__init__(message, error_code="EXCHANGE_RATE_UNAVAILABLE")
        self.base_currency = base_currency
        self.target_currency = target_currency
        self.reason = reason
        self.cache_fallback_disabled = cache_fallback_disabled


class CurrencyMismatchError(CurrencyException):
    """Raised when operations are attempted on incompatible currencies"""
    
    def __init__(
        self,
        operation: str,
        currency1: str,
        currency2: str,
        message: Optional[str] = None
    ):
        """
        Initialize currency mismatch error.
        
        Args:
            operation: The operation being attempted (e.g., 'addition')
            currency1: First currency code
            currency2: Second currency code
            message: Optional custom message
        """
        if message is None:
            message = (
                f"Cannot perform {operation} on different currencies: "
                f"{currency1} and {currency2}. "
                f"Convert to the same currency first."
            )
        
        super().__init__(message, error_code="CURRENCY_MISMATCH")
        self.operation = operation
        self.currency1 = currency1
        self.currency2 = currency2


class ConversionError(CurrencyException):
    """Raised when currency conversion fails"""
    
    def __init__(
        self,
        base_currency: str,
        target_currency: str,
        reason: Optional[str] = None,
        message: Optional[str] = None
    ):
        """
        Initialize conversion error.
        
        Args:
            base_currency: Source currency code
            target_currency: Target currency code
            reason: Optional reason for failure
            message: Optional custom message
        """
        if message is None:
            message = f"Failed to convert {base_currency} to {target_currency}"
            if reason:
                message += f": {reason}"
        
        super().__init__(message, error_code="CONVERSION_ERROR")
        self.base_currency = base_currency
        self.target_currency = target_currency
        self.reason = reason


class CacheError(CurrencyException):
    """Raised when cache operations fail"""
    
    def __init__(self, message: str, operation: Optional[str] = None):
        """
        Initialize cache error.
        
        Args:
            message: Error description
            operation: The cache operation that failed (e.g., 'read', 'write')
        """
        super().__init__(message, error_code="CACHE_ERROR")
        self.operation = operation


class EncryptionError(CurrencyException):
    """Raised when encryption/decryption operations fail"""
    
    def __init__(self, message: str, operation: Optional[str] = None):
        """
        Initialize encryption error.
        
        Args:
            message: Error description
            operation: The operation that failed (e.g., 'encrypt', 'decrypt')
        """
        super().__init__(message, error_code="ENCRYPTION_ERROR")
        self.operation = operation

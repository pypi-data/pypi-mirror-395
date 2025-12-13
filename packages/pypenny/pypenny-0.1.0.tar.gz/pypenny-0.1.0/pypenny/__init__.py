"""
pypenny - Production-grade currency conversion library

Simple, unified API for currency operations with smart error handling,
encrypted caching, and fuzzy locale matching.

Quick Start:
    >>> import pypenny as pp
    >>> pp.config(application_name="MyApp")
    >>> money = pp.Money('100', 'USD')
    >>> converted = pp.convert(money, 'EGP')
    >>> print(pp.format(converted))
"""

__version__ = "1.0.0"

from typing import Union, Optional, Dict, Any
from decimal import Decimal

# Import core classes
from .config import CurrencyConfig
from .currency_manager import CurrencyManager
from .money import Money
from .exceptions import (
    CurrencyException,
    ConfigurationError,
    InvalidCurrencyCodeError,
    CurrencyNotAllowedError,
    InvalidLocaleError,
    ExchangeRateUnavailableError,
    CurrencyMismatchError,
    ConversionError,
    CacheError,
    EncryptionError,
)

# Global manager instance
_manager: Optional[CurrencyManager] = None
_config: Optional[CurrencyConfig] = None


def config(
    application_name: Optional[str] = None,
    config_dict: Optional[Dict[str, Any]] = None,
    config_obj: Optional[CurrencyConfig] = None,
    **kwargs
) -> CurrencyConfig:
    """
    Configure pypenny globally.
    
    Can be called with:
    1. Keyword arguments: config(application_name="MyApp", allowed_currencies=['USD', 'EGP'])
    2. Dictionary: config(config_dict={'application_name': 'MyApp', ...})
    3. Config object: config(config_obj=CurrencyConfig(...))
    
    Args:
        application_name: Application name (required if using kwargs)
        config_dict: Configuration as dictionary (TypedDict compatible)
        config_obj: Pre-configured CurrencyConfig object
        **kwargs: Additional configuration options
    
    Returns:
        CurrencyConfig object
    
    Example:
        >>> import pypenny as pp
        >>> pp.config(application_name="MyApp", allowed_currencies=['USD', 'EGP'])
        >>> # Or with dict
        >>> pp.config(config_dict={'application_name': 'MyApp'})
    """
    global _manager, _config
    
    if config_obj is not None:
        _config = config_obj
    elif config_dict is not None:
        _config = CurrencyConfig(**config_dict)
    else:
        if application_name is None and 'application_name' not in kwargs:
            raise ValueError("application_name is required when using keyword arguments")
        
        if application_name is not None:
            kwargs['application_name'] = application_name
        
        _config = CurrencyConfig(**kwargs)
    
    # Create new manager with config
    _manager = CurrencyManager(_config)
    
    return _config


def _ensure_configured() -> None:
    """Ensure pypenny is configured before use"""
    global _manager, _config
    
    if _manager is None:
        # Auto-configure with defaults
        _config = CurrencyConfig(application_name="pypenny_default")
        _manager = CurrencyManager(_config)


def create_money(
    amount: Union[str, Decimal, int, float],
    currency_code: str
) -> Money:
    """
    Create Money object.
    
    Args:
        amount: Amount value
        currency_code: Currency code (e.g., 'USD', 'EGP')
    
    Returns:
        Money object
    
    Example:
        >>> money = pp.create_money('100', 'USD')
        >>> money = pp.Money('100', 'USD')  # Shorthand
    """
    _ensure_configured()
    moneyed_obj = _manager.create_money(amount, currency_code)
    return Money._from_moneyed(moneyed_obj)


def convert(
    money: Money,
    to_currency: str,
    strategy: Optional[str] = None
) -> Money:
    """
    Convert money to different currency.
    
    Args:
        money: Money object to convert
        to_currency: Target currency code
        strategy: Optional strategy ('live', 'cached', 'auto')
    
    Returns:
        Converted Money object
    
    Example:
        >>> usd = pp.Money('100', 'USD')
        >>> egp = pp.convert(usd, 'EGP')
    """
    _ensure_configured()
    result = _manager.convert(money.get_moneyed_object(), to_currency, strategy)
    return Money._from_moneyed(result)


def format(
    money: Money,
    locale: Optional[str] = None,
    **kwargs
) -> str:
    """
    Format money for display.
    
    Args:
        money: Money object to format
        locale: Locale code (e.g., 'en_US', 'ar_EG')
        **kwargs: Additional formatting options
    
    Returns:
        Formatted currency string
    
    Example:
        >>> money = pp.Money('100', 'USD')
        >>> pp.format(money, locale='en_US')  # '$100.00'
        >>> pp.format(money, locale='ar_EG')  # Different format
    """
    _ensure_configured()
    return _manager.format(money.get_moneyed_object(), locale, **kwargs)


# Arithmetic operations (functional style)

def add(money1: Money, money2: Money) -> Money:
    """Add two Money objects"""
    return money1 + money2


def subtract(money1: Money, money2: Money) -> Money:
    """Subtract two Money objects"""
    return money1 - money2


def multiply(money: Money, multiplier: Union[int, float, Decimal]) -> Money:
    """Multiply Money by scalar"""
    return money * multiplier


def divide(money: Money, divisor: Union[int, float, Decimal]) -> Money:
    """Divide Money by scalar"""
    return money / divisor


def floor_divide(money: Money, divisor: Union[int, float, Decimal]) -> Money:
    """Floor divide Money by scalar"""
    return money // divisor


def power(money: Money, exponent: Union[int, float, Decimal]) -> Money:
    """Raise Money to power"""
    return money ** exponent


# Cache management

def get_cache_stats() -> dict:
    """Get cache statistics"""
    _ensure_configured()
    return _manager.get_cache_stats()


def cleanup_cache() -> int:
    """Clean up old cached records"""
    _ensure_configured()
    return _manager.cleanup_cache()


def clear_cache() -> None:
    """Clear all cached exchange rates"""
    _ensure_configured()
    _manager.clear_cache()


# Export all public APIs
__all__ = [
    # Version
    "__version__",
    
    # Configuration
    "config",
    "CurrencyConfig",
    
    # Core classes
    "Money",
    "CurrencyManager",
    
    # Main operations
    "create_money",
    "convert",
    "format",
    
    # Arithmetic operations
    "add",
    "subtract",
    "multiply",
    "divide",
    "floor_divide",
    "power",
    
    # Cache management
    "get_cache_stats",
    "cleanup_cache",
    "clear_cache",
    
    # Exceptions
    "CurrencyException",
    "ConfigurationError",
    "InvalidCurrencyCodeError",
    "CurrencyNotAllowedError",
    "InvalidLocaleError",
    "ExchangeRateUnavailableError",
    "CurrencyMismatchError",
    "ConversionError",
    "CacheError",
    "EncryptionError",
]

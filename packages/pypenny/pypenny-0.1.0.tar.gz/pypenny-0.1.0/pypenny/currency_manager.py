"""
Currency Manager - Main User-Facing API

Provides a simple, robust interface for all currency operations with:
- Configuration-aware behavior
- Safe string operations (no crashes)
- Automatic locale fuzzy matching
- Smart error messages
- Integration with exchange strategies
"""

from decimal import Decimal
from typing import Union, Optional
from moneyed import Money, get_currency
from moneyed.l10n import format_money

from .config import CurrencyConfig
from .exceptions import (
    InvalidCurrencyCodeError,
    CurrencyNotAllowedError,
    CurrencyMismatchError,
    ConversionError
)
from .locale_matcher import normalize_locale
from .exchange_cache import ExchangeCache
from ._core import CurrencyConverter, ExchangeRateService


class CurrencyManager:
    """
    Main user-facing API for currency operations.
    
    Features:
    - Simple, explicit API (Option B style)
    - Configuration-aware (respects allowed currencies, cache settings)
    - Safe operations (no str() crashes)
    - Automatic locale normalization
    - Smart error messages
    
    Example:
        >>> config = CurrencyConfig(
        ...     application_name="MyApp",
        ...     allowed_currencies=['USD', 'EGP']
        ... )
        >>> manager = CurrencyManager(config)
        >>> money = manager.create_money('100', 'USD')
        >>> converted = manager.convert(money, 'EGP')
        >>> formatted = manager.format(converted, locale='ar_EG')
    """
    
    def __init__(self, config: CurrencyConfig):
        """
        Initialize currency manager with configuration.
        
        Args:
            config: Currency configuration
        """
        self.config = config
        
        # Initialize exchange cache
        self.exchange_cache = ExchangeCache(config)
        
        # Initialize exchange rate service with config
        self.exchange_service = ExchangeRateService(
            api_key=config.api_key,
            timeout=config.api_timeout,
            max_retries=config.api_max_retries
        )
        
        # Initialize converter
        self.converter = CurrencyConverter(self.exchange_service)
    
    def _validate_currency(self, currency_code: str) -> str:
        """
        Validate and normalize currency code.
        
        Args:
            currency_code: Currency code to validate
        
        Returns:
            Normalized currency code (uppercase)
        
        Raises:
            InvalidCurrencyCodeError: If currency code is invalid
            CurrencyNotAllowedError: If currency not in allowed list
        """
        # Normalize case
        currency_code = currency_code.upper().strip()
        
        # Validate currency exists
        try:
            get_currency(currency_code)
        except Exception:
            # Try to find suggestions
            from difflib import get_close_matches
            all_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'EGP', 'AUD', 'CAD', 'CHF']
            suggestions = get_close_matches(currency_code, all_currencies, n=3)
            
            raise InvalidCurrencyCodeError(currency_code, suggestions=suggestions)
        
        # Check if allowed by configuration
        if not self.config.is_currency_allowed(currency_code):
            raise CurrencyNotAllowedError(
                currency_code,
                self.config.allowed_currencies
            )
        
        return currency_code
    
    def create_money(
        self,
        amount: Union[str, Decimal, int, float],
        currency_code: str,
        locale: Optional[str] = None
    ) -> Money:
        """
        Create Money object with validation.
        
        Args:
            amount: Amount (string, Decimal, int, or float)
            currency_code: Currency code (e.g., 'USD', 'EGP')
            locale: Optional locale for validation (not used in Money creation)
        
        Returns:
            Money object
        
        Raises:
            InvalidCurrencyCodeError: If currency code is invalid
            CurrencyNotAllowedError: If currency not in allowed list
        
        Example:
            >>> money = manager.create_money('100.50', 'USD')
            >>> money = manager.create_money(Decimal('100.50'), 'EGP')
        """
        # Validate currency
        currency_code = self._validate_currency(currency_code)
        
        # Convert amount to Decimal if needed
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))
        
        # Create Money object
        return Money(amount, currency_code)
    
    def convert(
        self,
        money: Money,
        to_currency: str,
        strategy: Optional[str] = None
    ) -> Money:
        """
        Convert money to different currency.
        
        Args:
            money: Money object to convert
            to_currency: Target currency code
            strategy: Optional strategy override ('live', 'cached', 'auto')
        
        Returns:
            Converted Money object
        
        Raises:
            InvalidCurrencyCodeError: If target currency is invalid
            CurrencyNotAllowedError: If target currency not allowed
            ConversionError: If conversion fails
        
        Example:
            >>> converted = manager.convert(money_usd, 'EGP')
            >>> converted = manager.convert(money_usd, 'EGP', strategy='live')
        """
        # Validate target currency
        to_currency = self._validate_currency(to_currency)
        
        # Use configured strategy if not specified
        if strategy is None:
            strategy = self.config.default_exchange_strategy
        
        try:
            # Try live conversion
            if strategy in ['live', 'auto']:
                try:
                    converted = self.converter.convert(money, to_currency)
                    
                    # Cache the rate for future use
                    if strategy == 'auto' or strategy == 'live':
                        rate = self.exchange_service.get_rate(
                            money.currency.code,
                            to_currency
                        )
                        self.exchange_cache.store_rate(
                            money.currency.code,
                            to_currency,
                            rate,
                            self.exchange_service.provider.value
                        )
                    
                    return converted
                
                except Exception as e:
                    # If auto mode and cache fallback allowed, try cache
                    if strategy == 'auto' and self.config.allow_cache_fallback:
                        cached_rate = self.exchange_cache.get_latest_rate(
                            money.currency.code,
                            to_currency
                        )
                        
                        if cached_rate:
                            # Use cached rate
                            converted_amount = money.amount * cached_rate
                            target_currency = get_currency(to_currency)
                            
                            # Calculate exponent for rounding
                            # sub_unit is the divisor (100 = 2 decimal places, 1 = 0 decimal places)
                            if target_currency.sub_unit == 1:
                                exponent = Decimal('1')
                            else:
                                import math
                                decimal_places = int(math.log10(target_currency.sub_unit))
                                exponent = Decimal('0.1') ** decimal_places
                            
                            from decimal import ROUND_HALF_UP
                            converted_amount = converted_amount.quantize(
                                exponent,
                                rounding=ROUND_HALF_UP
                            )
                            return Money(converted_amount, target_currency)
                        
                        # No cache available
                        if not self.config.allow_cache_fallback:
                            from exceptions import ExchangeRateUnavailableError
                            raise ExchangeRateUnavailableError(
                                money.currency.code,
                                to_currency,
                                reason=str(e),
                                cache_fallback_disabled=True
                            )
                    
                    # Re-raise if not auto mode or cache fallback disabled
                    raise
            
            # Cached strategy only
            elif strategy == 'cached':
                cached_rate = self.exchange_cache.get_latest_rate(
                    money.currency.code,
                    to_currency
                )
                
                if not cached_rate:
                    raise ConversionError(
                        money.currency.code,
                        to_currency,
                        reason="No cached rate available"
                    )
                
                # Use cached rate
                converted_amount = money.amount * cached_rate
                target_currency = get_currency(to_currency)
                
                # Calculate exponent for rounding
                # sub_unit is the divisor (100 = 2 decimal places, 1 = 0 decimal places)
                if target_currency.sub_unit == 1:
                    exponent = Decimal('1')
                else:
                    import math
                    decimal_places = int(math.log10(target_currency.sub_unit))
                    exponent = Decimal('0.1') ** decimal_places
                
                from decimal import ROUND_HALF_UP
                converted_amount = converted_amount.quantize(
                    exponent,
                    rounding=ROUND_HALF_UP
                )
                return Money(converted_amount, target_currency)
        
        except Exception as e:
            if isinstance(e, (InvalidCurrencyCodeError, CurrencyNotAllowedError)):
                raise
            
            raise ConversionError(
                money.currency.code,
                to_currency,
                reason=str(e)
            )
    
    def format(
        self,
        money: Money,
        locale: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Format money for display with locale awareness.
        
        Args:
            money: Money object to format
            locale: Locale code (e.g., 'en_US', 'ar_EG')
            **kwargs: Additional formatting options for Babel
        
        Returns:
            Formatted currency string
        
        Example:
            >>> en = manager.format(money, locale='en_US')
            >>> ar = manager.format(money, locale='ar_EG')
        """
        # Use configured default locale if not specified
        if locale is None:
            locale = self.config.default_locale
        
        # Normalize locale with fuzzy matching
        locale = normalize_locale(locale, raise_on_invalid=False)
        
        # Format using Babel
        return format_money(money, locale=locale, **kwargs)
    
    @staticmethod
    def add(money1: Money, money2: Money) -> Money:
        """
        Safely add two Money objects.
        
        Args:
            money1: First Money object
            money2: Second Money object
        
        Returns:
            Sum as Money object
        
        Raises:
            CurrencyMismatchError: If currencies don't match
        
        Example:
            >>> total = manager.add(money1, money2)
        """
        if money1.currency != money2.currency:
            raise CurrencyMismatchError(
                "addition",
                money1.currency.code,
                money2.currency.code
            )
        
        return money1 + money2
    
    @staticmethod
    def subtract(money1: Money, money2: Money) -> Money:
        """
        Safely subtract two Money objects.
        
        Args:
            money1: First Money object
            money2: Second Money object
        
        Returns:
            Difference as Money object
        
        Raises:
            CurrencyMismatchError: If currencies don't match
        
        Example:
            >>> difference = manager.subtract(money1, money2)
        """
        if money1.currency != money2.currency:
            raise CurrencyMismatchError(
                "subtraction",
                money1.currency.code,
                money2.currency.code
            )
        
        return money1 - money2
    
    @staticmethod
    def multiply(money: Money, multiplier: Union[int, float, Decimal]) -> Money:
        """
        Multiply Money by a scalar value.
        
        Args:
            money: Money object
            multiplier: Scalar multiplier (int, float, or Decimal)
        
        Returns:
            Multiplied Money object
        
        Example:
            >>> doubled = manager.multiply(money, 2)
            >>> tripled = manager.multiply(money, 3.0)
        """
        return money * multiplier
    
    @staticmethod
    def divide(money: Money, divisor: Union[int, float, Decimal]) -> Money:
        """
        Divide Money by a scalar value.
        
        Args:
            money: Money object
            divisor: Scalar divisor (int, float, or Decimal)
        
        Returns:
            Divided Money object
        
        Raises:
            ZeroDivisionError: If divisor is zero
        
        Example:
            >>> half = manager.divide(money, 2)
            >>> third = manager.divide(money, 3.0)
        """
        if divisor == 0:
            raise ZeroDivisionError("Cannot divide money by zero")
        return money / divisor
    
    @staticmethod
    def floor_divide(money: Money, divisor: Union[int, float, Decimal]) -> Money:
        """
        Floor divide Money by a scalar value.
        
        Args:
            money: Money object
            divisor: Scalar divisor (int, float, or Decimal)
        
        Returns:
            Floor divided Money object
        
        Raises:
            ZeroDivisionError: If divisor is zero
        
        Example:
            >>> result = manager.floor_divide(money, 3)
        """
        if divisor == 0:
            raise ZeroDivisionError("Cannot divide money by zero")
        return money // divisor
    
    @staticmethod
    def power(money: Money, exponent: Union[int, float, Decimal]) -> Money:
        """
        Raise Money amount to a power.
        
        Args:
            money: Money object
            exponent: Power exponent (int, float, or Decimal)
        
        Returns:
            Money object with amount raised to power
        
        Example:
            >>> squared = manager.power(money, 2)
        """
        # Use the Money class power operation
        return money ** exponent
    
    def get_cache_stats(self) -> dict:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        
        Example:
            >>> stats = manager.get_cache_stats()
            >>> print(stats['total_records'])
        """
        return self.exchange_cache.get_cache_stats()
    
    def cleanup_cache(self) -> int:
        """
        Clean up old cached records.
        
        Returns:
            Number of records removed
        
        Example:
            >>> removed = manager.cleanup_cache()
        """
        return self.exchange_cache.cleanup_old_records()
    
    def clear_cache(self) -> None:
        """
        Clear all cached exchange rates.
        
        Example:
            >>> manager.clear_cache()
        """
        self.exchange_cache.clear_cache()

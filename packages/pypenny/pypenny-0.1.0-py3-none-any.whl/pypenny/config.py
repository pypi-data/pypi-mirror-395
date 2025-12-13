"""
User Configuration for Currency Manager

Provides flexible configuration for cache behavior, currency restrictions,
and application identity.
"""

from dataclasses import dataclass, field
from typing import Optional, List
from moneyed import get_currency


@dataclass
class CurrencyConfig:
    """
    Configuration class for CurrencyManager behavior.
    
    Attributes:
        application_name: Required identifier for cache directory (via platformdirs)
        allow_cache_fallback: If True, falls back to cache on network failure.
                             If False, raises error immediately (strict mode)
        cache_max_records: Maximum number of exchange rate records per currency pair
        cache_retention_days: Number of days to retain cached records
        cache_file_path: Optional custom cache file path (None = use platformdirs)
        allowed_currencies: Optional whitelist of currency codes (None = all allowed)
        default_exchange_strategy: Default strategy ('live', 'cached', 'auto')
        default_locale: Default locale for formatting (e.g., 'en_US')
    
    Example:
        >>> # Permissive configuration (default)
        >>> config = CurrencyConfig(application_name="MyApp")
        
        >>> # Strict production configuration
        >>> config = CurrencyConfig(
        ...     application_name="MyApp",
        ...     allow_cache_fallback=False,
        ...     allowed_currencies=['USD', 'EGP']
        ... )
    """
    
    # Required
    application_name: str
    
    # Cache behavior
    allow_cache_fallback: bool = True
    cache_max_records: int = 7
    cache_retention_days: int = 3
    cache_file_path: Optional[str] = None
    
    # Currency restrictions
    allowed_currencies: Optional[List[str]] = None
    
    # Exchange settings
    default_exchange_strategy: str = 'auto'
    default_locale: str = 'en_US'
    
    # API settings
    api_key: Optional[str] = None
    api_timeout: int = 5
    api_max_retries: int = 3
    
    def __post_init__(self) -> None:
        """Validate configuration after initialization"""
        self.validate()
    
    def validate(self) -> None:
        """
        Validate configuration parameters.
        
        Raises:
            ValueError: If application_name is empty or invalid
            ValueError: If default_exchange_strategy is invalid
            Exception: If any allowed_currencies are invalid (via get_currency)
        """
        # Validate application name
        if not self.application_name or not self.application_name.strip():
            raise ValueError(
                "application_name is required and cannot be empty. "
                "This is used for cache directory naming."
            )
        
        # Validate exchange strategy
        valid_strategies = ['live', 'cached', 'auto']
        if self.default_exchange_strategy not in valid_strategies:
            raise ValueError(
                f"Invalid default_exchange_strategy: '{self.default_exchange_strategy}'. "
                f"Must be one of: {', '.join(valid_strategies)}"
            )
        
        # Validate cache settings
        if self.cache_max_records < 1:
            raise ValueError("cache_max_records must be at least 1")
        
        if self.cache_retention_days < 1:
            raise ValueError("cache_retention_days must be at least 1")
        
        # Validate allowed currencies if specified
        if self.allowed_currencies is not None:
            if not isinstance(self.allowed_currencies, list):
                raise ValueError("allowed_currencies must be a list or None")
            
            if len(self.allowed_currencies) == 0:
                raise ValueError(
                    "allowed_currencies cannot be empty. "
                    "Use None to allow all currencies."
                )
            
            # Validate each currency code exists
            invalid_currencies = []
            for code in self.allowed_currencies:
                try:
                    get_currency(code)
                except Exception:
                    invalid_currencies.append(code)
            
            if invalid_currencies:
                raise ValueError(
                    f"Invalid currency codes in allowed_currencies: {', '.join(invalid_currencies)}. "
                    f"All codes must be valid ISO 4217 currency codes."
                )
    
    def is_currency_allowed(self, currency_code: str) -> bool:
        """
        Check if a currency code is allowed by this configuration.
        
        Args:
            currency_code: Currency code to check (e.g., 'USD')
        
        Returns:
            True if currency is allowed, False otherwise
        """
        if self.allowed_currencies is None:
            return True  # All currencies allowed
        
        return currency_code.upper() in [c.upper() for c in self.allowed_currencies]
    
    def get_allowed_currencies_str(self) -> str:
        """
        Get comma-separated string of allowed currencies.
        
        Returns:
            String like "USD, EGP, EUR" or "all currencies"
        """
        if self.allowed_currencies is None:
            return "all currencies"
        
        return ", ".join(sorted(self.allowed_currencies))

# Robust Currency Conversion Solution

[![Python 3.11+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Production-grade currency conversion library with smart error handling, encrypted caching, and fuzzy locale matching.

## ✨ Features

- 🎯 **Professional DX**: Safe string operations, no crashes with `str()` or `print()`
- 🧠 **Smart Error Handling**: Fuzzy locale matching auto-corrects typos (`em_US` → `en_US`)
- ⚙️ **Flexible Configuration**: Control cache behavior and restrict allowed currencies
- 🔒 **Encrypted Cache**: Fernet (AES-128) encryption with cross-platform storage
- 📊 **Deduplication Logic**: Only 1 record per day if exchange rate unchanged
- 🌍 **180+ Currencies**: Supports all ISO 4217 currencies via py-moneyed
- 🔄 **Dual Exchange Strategies**: Live network-based + encrypted local cache fallback
- 📦 **Zero Config**: Works out of the box with sensible defaults

## 🚀 Quick Start

### Installation

```bash
# Using uv (recommended)
uv pip install robust-currency

# Using pip
pip install robust-currency
```

### Basic Usage

```python
from config import CurrencyConfig
from currency_manager import CurrencyManager

# Create configuration
config = CurrencyConfig(application_name="MyApp")
manager = CurrencyManager(config)

# Create money
money_usd = manager.create_money('100', 'USD')

# Convert
money_egp = manager.convert(money_usd, 'EGP')

# Format (safe to print!)
print(manager.format(money_egp, locale='ar_EG'))
# Output: ‏4,752.00 ج.م.‏
```

### Strict Configuration (Production)

```python
config = CurrencyConfig(
    application_name="ProductionApp",
    allow_cache_fallback=False,  # Fail fast on network errors
    allowed_currencies=['USD', 'EGP'],  # Whitelist only
    cache_max_records=10,
    cache_retention_days=7
)

manager = CurrencyManager(config)

# This works
money_usd = manager.create_money('100', 'USD')

# This raises CurrencyNotAllowedError with helpful message
money_eur = manager.create_money('100', 'EUR')
# Error: Currency 'EUR' not allowed. Allowed: USD, EGP.
#        Update config.allowed_currencies to include 'EUR'.
```

## 📚 Key Features

### 1. Fuzzy Locale Matching

Automatically corrects common locale mistakes:

```python
manager.format(money, locale='EN_us')   # → Normalized to 'en_US'
manager.format(money, locale='US_EN')   # → Swapped to 'en_US'
manager.format(money, locale='em_US')   # → Typo corrected to 'en_US'
manager.format(money, locale='US')      # → Alias resolved to 'en_US'
```

### 2. Smart Error Messages

```python
# Invalid currency with suggestions
manager.create_money('100', 'USDD')
# Error: Invalid currency code: 'USDD'. Did you mean: USD?

# Currency not allowed
manager.create_money('100', 'EUR')  # When only USD/EGP allowed
# Error: Currency 'EUR' not allowed. Allowed: USD, EGP.
#        Update config.allowed_currencies to include 'EUR'.
```

### 3. Encrypted Cache with Deduplication

```python
# Cache automatically stores exchange rates
money_converted = manager.convert(money_usd, 'EGP')

# Get cache statistics
stats = manager.get_cache_stats()
print(stats['total_records'])  # Number of cached rates
print(stats['cache_file'])     # Path to encrypted cache file

# Cleanup old records
removed = manager.cleanup_cache()
```

**Deduplication Logic**:
- Same day + same rate → Skip (no duplicate)
- Same day + different rate (>0.01%) → Store new record
- Different day → Always store new record
- Enforces `max_records` limit (keeps most recent)

### 4. Cache File Locations (via platformdirs)

- **Windows**: `C:\Users\<user>\AppData\Local\<app_name>\Cache\exchange_cache.enc`
- **Linux**: `~/.cache/<app_name>/exchange_cache.enc`
- **macOS**: `~/Library/Caches/<app_name>/exchange_cache.enc`

### 5. Exchange Strategies

```python
# LIVE: Always fetch from network
converted = manager.convert(money, 'EGP', strategy='live')

# CACHED: Use local cache only
converted = manager.convert(money, 'EGP', strategy='cached')

# AUTO: Try live, fallback to cache (default)
converted = manager.convert(money, 'EGP', strategy='auto')
```

## 🔧 Configuration Options

```python
CurrencyConfig(
    # Required
    application_name: str,              # For cache directory naming
    
    # Cache behavior
    allow_cache_fallback: bool = True,  # Fallback to cache on network failure
    cache_max_records: int = 7,         # Max records per currency pair
    cache_retention_days: int = 3,      # Days to retain cached records
    cache_file_path: str = None,        # Custom cache path (None = platformdirs)
    
    # Currency restrictions
    allowed_currencies: List[str] = None,  # Whitelist (None = all allowed)
    
    # Exchange settings
    default_exchange_strategy: str = 'auto',  # 'live', 'cached', 'auto'
    default_locale: str = 'en_US',
    
    # API settings
    api_key: str = None,
    api_timeout: int = 5,
    api_max_retries: int = 3,
)
```

## 🧪 Testing

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run stress tests
pytest tests/test_stress.py -v
```

## 📖 Advanced Usage

### Safe Operations

```python
# All these are safe (no crashes!)
money = manager.create_money('100.50', 'USD')
print(manager.format(money))           # Safe
formatted = f"{manager.format(money)}" # Safe in f-strings

# Lists of money
money_list = [
    manager.create_money('10', 'USD'),
    manager.create_money('20', 'USD'),
]
formatted_list = [manager.format(m) for m in money_list]
print(formatted_list)  # Safe
```

### Currency Operations

```python
# Addition (same currency only)
total = manager.add(
    manager.create_money('50', 'USD'),
    manager.create_money('25', 'USD')
)

# Subtraction
difference = manager.subtract(
    manager.create_money('100', 'USD'),
    manager.create_money('25', 'USD')
)

# Attempting to add different currencies raises clear error
manager.add(money_usd, money_egp)
# Error: Cannot perform addition on different currencies: USD and EGP.
#        Convert to the same currency first.
```

## 🏗️ Architecture

```
┌─────────────────┐
│ CurrencyManager │  ← Main user-facing API
└────────┬────────┘
         │
    ┌────┴────┬──────────┬────────────┐
    ▼         ▼          ▼            ▼
┌────────┐ ┌──────┐ ┌─────────┐ ┌──────────┐
│ Config │ │Locale│ │Exchange │ │Encryption│
│        │ │Match │ │  Cache  │ │  Utils   │
└────────┘ └──────┘ └─────────┘ └──────────┘
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built on [py-moneyed](https://github.com/py-moneyed/py-moneyed) for robust currency handling
- Uses [Babel](https://babel.pocoo.org/) for locale-aware formatting
- Encryption via [cryptography](https://cryptography.io/)
- Cross-platform paths via [platformdirs](https://github.com/platformdirs/platformdirs)

## 📞 Support

- 📖 [Documentation](https://github.com/yourusername/robust-currency#readme)
- 🐛 [Issue Tracker](https://github.com/yourusername/robust-currency/issues)
- 💬 [Discussions](https://github.com/yourusername/robust-currency/discussions)

---

**Made with ❤️ for developers who need reliable currency handling**

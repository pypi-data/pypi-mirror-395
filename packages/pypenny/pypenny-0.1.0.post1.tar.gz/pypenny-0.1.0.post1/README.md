# pypenny: Robust Currency Conversion Solution

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Production-grade currency conversion library with smart error handling, encrypted caching, and fuzzy locale matching.

## ✨ Features

- 🎯 **Unified API**: Simple, intuitive top-level functions for all operations
- 💰 **Smart Money Class**: Immutable, hashable, and supports arithmetic operations
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
uv pip install pypenny

# Using pip
pip install pypenny
```

### Basic Usage

```python
import pypenny as pp

# Configure (optional, uses defaults if skipped)
pp.config(application_name="MyApp")

# Create money
money_usd = pp.Money('100', 'USD')

# Convert
money_egp = pp.convert(money_usd, 'EGP')

# Format (safe to print!)
print(pp.format(money_egp, locale='ar_EG'))
# Output: ‏4,752.00 ج.م.‏
```

### Strict Configuration (Production)

```python
import pypenny as pp

pp.config(
    application_name="ProductionApp",
    allow_cache_fallback=False,  # Fail fast on network errors
    allowed_currencies=['USD', 'EGP'],  # Whitelist only
    cache_max_records=10,
    cache_retention_days=7
)

# This works
money_usd = pp.Money('100', 'USD')

# This raises CurrencyNotAllowedError with helpful message
try:
    money_eur = pp.Money('100', 'EUR')
except pp.CurrencyNotAllowedError as e:
    print(e)
    # Error: Currency 'EUR' not allowed. Allowed: USD, EGP.
    #        Update config.allowed_currencies to include 'EUR'.
```

## 📚 Key Features

### 1. Arithmetic Operations

The `Money` class supports intuitive arithmetic operations:

```python
m1 = pp.Money('100', 'USD')
m2 = pp.Money('50', 'USD')

# Arithmetic
total = m1 + m2           # 150.00 USD
diff = m1 - m2            # 50.00 USD
doubled = m1 * 2          # 200.00 USD
halved = m1 / 2           # 50.00 USD

# Comparison
is_greater = m1 > m2      # True
```

### 2. Fuzzy Locale Matching

Automatically corrects common locale mistakes:

```python
pp.format(money, locale='EN_us')   # → Normalized to 'en_US'
pp.format(money, locale='US_EN')   # → Swapped to 'en_US'
pp.format(money, locale='em_US')   # → Typo corrected to 'en_US'
pp.format(money, locale='US')      # → Alias resolved to 'en_US'
```

### 3. Encrypted Cache with Deduplication

```python
# Cache automatically stores exchange rates
money_converted = pp.convert(money_usd, 'EGP')

# Get cache statistics
stats = pp.get_cache_stats()
print(stats['total_records'])  # Number of cached rates
print(stats['cache_file'])     # Path to encrypted cache file

# Cleanup old records
pp.cleanup_cache()
```

### 4. Exchange Strategies

```python
# LIVE: Always fetch from network
converted = pp.convert(money, 'EGP', strategy='live')

# CACHED: Use local cache only
converted = pp.convert(money, 'EGP', strategy='cached')

# AUTO: Try live, fallback to cache (default)
converted = pp.convert(money, 'EGP', strategy='auto')
```

## 🔧 Configuration Options

```python
pp.config(
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

## 🏗️ Architecture

```
┌─────────────┐
│   pypenny   │  ← Unified Package API
└──────┬──────┘
       │
┌──────▼────────┐
│CurrencyManager│
└──────┬────────┘
       │
  ┌────┴────┬──────────┬────────────┐
  ▼         ▼          ▼            ▼
┌────────┐ ┌──────┐ ┌─────────┐ ┌──────────┐
│ Config │ │Locale│ │Exchange │ │Encryption│
│        │ │Match │ │  Cache  │ │  Utils   │
236: └────────┘ └──────┘ └─────────┘ └──────────┘
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

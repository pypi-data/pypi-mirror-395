"""
Fuzzy Locale Matcher

Handles common locale input errors with smart correction:
- Case normalization: em_US → en_US
- Order swapping: US_EN → en_US
- Typo correction: em_US → en_US (Levenshtein distance)
"""

import difflib
from typing import Optional, List, Tuple
from .exceptions import InvalidLocaleError

# Try to import Levenshtein for better performance, fall back to difflib
try:
    import Levenshtein
    HAS_LEVENSHTEIN = True
except ImportError:
    HAS_LEVENSHTEIN = False


# Common valid locales (subset of most used)
COMMON_LOCALES = [
    'en_US', 'en_GB', 'en_CA', 'en_AU', 'en_IN',
    'ar_EG', 'ar_SA', 'ar_AE',
    'fr_FR', 'fr_CA',
    'de_DE', 'de_AT', 'de_CH',
    'es_ES', 'es_MX', 'es_AR',
    'it_IT',
    'ja_JP',
    'zh_CN', 'zh_TW', 'zh_HK',
    'ko_KR',
    'pt_BR', 'pt_PT',
    'ru_RU',
    'nl_NL',
    'pl_PL',
    'tr_TR',
    'sv_SE',
    'no_NO',
    'da_DK',
    'fi_FI',
    'el_GR',
    'he_IL',
    'hi_IN',
    'th_TH',
    'vi_VN',
    'id_ID',
]

# Common locale aliases (shortcuts)
LOCALE_ALIASES = {
    'US': 'en_US',
    'UK': 'en_GB',
    'GB': 'en_GB',
    'CA': 'en_CA',
    'AU': 'en_AU',
    'EG': 'ar_EG',
    'SA': 'ar_SA',
    'FR': 'fr_FR',
    'DE': 'de_DE',
    'ES': 'es_ES',
    'IT': 'it_IT',
    'JP': 'ja_JP',
    'CN': 'zh_CN',
    'KR': 'ko_KR',
    'BR': 'pt_BR',
    'RU': 'ru_RU',
}


def calculate_distance(s1: str, s2: str) -> int:
    """
    Calculate edit distance between two strings.
    
    Uses Levenshtein if available, otherwise falls back to difflib.
    
    Args:
        s1: First string
        s2: Second string
    
    Returns:
        Edit distance (number of edits needed)
    """
    if HAS_LEVENSHTEIN:
        return Levenshtein.distance(s1, s2)
    else:
        # Fallback: use difflib ratio and approximate distance
        ratio = difflib.SequenceMatcher(None, s1, s2).ratio()
        max_len = max(len(s1), len(s2))
        return int(max_len * (1 - ratio))


def try_swap_order(locale: str) -> Optional[str]:
    """
    Try swapping language and country codes.
    
    Examples:
        US_EN → en_US
        EG_AR → ar_EG
    
    Args:
        locale: Locale string to swap
    
    Returns:
        Swapped locale if it's valid, None otherwise
    """
    if '_' not in locale:
        return None
    
    parts = locale.split('_')
    if len(parts) != 2:
        return None
    
    # Swap and normalize case
    swapped = f"{parts[1].lower()}_{parts[0].upper()}"
    
    if swapped in COMMON_LOCALES:
        return swapped
    
    return None


def find_close_matches(locale: str, max_distance: int = 2, max_results: int = 3) -> List[str]:
    """
    Find close locale matches using edit distance.
    
    Args:
        locale: Input locale string
        max_distance: Maximum edit distance to consider (default: 2)
        max_results: Maximum number of results to return
    
    Returns:
        List of close matching locales, sorted by distance
    """
    locale_lower = locale.lower()
    matches = []
    
    for valid_locale in COMMON_LOCALES:
        distance = calculate_distance(locale_lower, valid_locale.lower())
        if distance <= max_distance:
            matches.append((valid_locale, distance))
    
    # Sort by distance (closest first)
    matches.sort(key=lambda x: x[1])
    
    return [match[0] for match in matches[:max_results]]


def normalize_locale(locale: str, raise_on_invalid: bool = True) -> str:
    """
    Normalize and validate locale string with fuzzy matching.
    
    Handles:
    - Case normalization: EN_us → en_US
    - Typo correction: em_US → en_US
    - Order swapping: US_EN → en_US
    - Aliases: US → en_US
    
    Args:
        locale: Input locale string
        raise_on_invalid: If True, raises InvalidLocaleError on failure
    
    Returns:
        Normalized locale string
    
    Raises:
        InvalidLocaleError: If locale is invalid and raise_on_invalid=True
    
    Examples:
        >>> normalize_locale('EN_us')
        'en_US'
        >>> normalize_locale('em_US')
        'en_US'
        >>> normalize_locale('US_EN')
        'en_US'
        >>> normalize_locale('US')
        'en_US'
    """
    if not locale or not isinstance(locale, str):
        if raise_on_invalid:
            raise InvalidLocaleError(
                str(locale),
                suggestions=['en_US', 'en_GB', 'ar_EG'],
                message="Locale must be a non-empty string"
            )
        return 'en_US'  # Default fallback
    
    locale = locale.strip()
    
    # Check if it's an alias
    if locale.upper() in LOCALE_ALIASES:
        return LOCALE_ALIASES[locale.upper()]
    
    # Try exact match with case normalization
    if '_' in locale:
        parts = locale.split('_')
        if len(parts) == 2:
            normalized = f"{parts[0].lower()}_{parts[1].upper()}"
            if normalized in COMMON_LOCALES:
                return normalized
    
    # Try swapping order (US_EN → en_US)
    swapped = try_swap_order(locale)
    if swapped:
        return swapped
    
    # Try fuzzy matching for typos
    close_matches = find_close_matches(locale, max_distance=2, max_results=3)
    
    if close_matches:
        # If we have a very close match (distance 1), auto-correct
        best_match = close_matches[0]
        distance = calculate_distance(locale.lower(), best_match.lower())
        
        if distance == 1:
            # Very close match, likely a typo - auto-correct
            return best_match
        
        # Multiple possible matches - raise error with suggestions
        if raise_on_invalid:
            raise InvalidLocaleError(locale, suggestions=close_matches)
        return close_matches[0]  # Return best guess
    
    # No matches found
    if raise_on_invalid:
        raise InvalidLocaleError(
            locale,
            suggestions=['en_US', 'en_GB', 'ar_EG', 'fr_FR', 'de_DE']
        )
    
    return 'en_US'  # Default fallback


def is_valid_locale(locale: str) -> bool:
    """
    Check if a locale string is valid (without raising exceptions).
    
    Args:
        locale: Locale string to check
    
    Returns:
        True if valid, False otherwise
    """
    try:
        normalize_locale(locale, raise_on_invalid=True)
        return True
    except InvalidLocaleError:
        return False


def get_locale_suggestions(locale: str, max_suggestions: int = 5) -> List[str]:
    """
    Get locale suggestions for an invalid locale.
    
    Args:
        locale: Invalid locale string
        max_suggestions: Maximum number of suggestions
    
    Returns:
        List of suggested valid locales
    """
    # Try fuzzy matching
    suggestions = find_close_matches(locale, max_distance=3, max_results=max_suggestions)
    
    if not suggestions:
        # Return most common locales as fallback
        suggestions = ['en_US', 'en_GB', 'ar_EG', 'fr_FR', 'de_DE'][:max_suggestions]
    
    return suggestions

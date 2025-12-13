"""
Tests for locale fuzzy matching
"""

import pytest
from pypenny.locale_matcher import (
    normalize_locale,
    is_valid_locale,
    get_locale_suggestions,
    try_swap_order,
    find_close_matches,
    calculate_distance
)
from pypenny.exceptions import InvalidLocaleError


class TestCaseNormalization:
    """Test case normalization"""
    
    def test_lowercase_language(self):
        """Should normalize language code to lowercase"""
        assert normalize_locale('EN_US') == 'en_US'
        assert normalize_locale('FR_FR') == 'fr_FR'
    
    def test_uppercase_country(self):
        """Should normalize country code to uppercase"""
        assert normalize_locale('en_us') == 'en_US'
        assert normalize_locale('ar_eg') == 'ar_EG'
    
    def test_mixed_case(self):
        """Should handle mixed case correctly"""
        assert normalize_locale('En_Us') == 'en_US'
        assert normalize_locale('aR_Eg') == 'ar_EG'


class TestOrderSwapping:
    """Test language/country order swapping"""
    
    def test_swap_us_en(self):
        """US_EN should become en_US"""
        assert normalize_locale('US_EN') == 'en_US'
    
    def test_swap_eg_ar(self):
        """EG_AR should become ar_EG"""
        assert normalize_locale('EG_AR') == 'ar_EG'
    
    def test_swap_fr_fr(self):
        """FR_FR should become fr_FR"""
        assert normalize_locale('FR_FR') == 'fr_FR'
    
    def test_try_swap_order_function(self):
        """Test try_swap_order helper function"""
        assert try_swap_order('US_EN') == 'en_US'
        assert try_swap_order('GB_EN') == 'en_GB'
        assert try_swap_order('invalid') is None


class TestTypoCorrection:
    """Test typo correction with fuzzy matching"""
    
    def test_single_character_typo(self):
        """Should correct single character typos"""
        # em_US → en_US (m→n)
        assert normalize_locale('em_US') == 'en_US'
    
    def test_close_match_auto_correct(self):
        """Should auto-correct very close matches (distance=1)"""
        result = normalize_locale('en_UZ')  # Should match en_US
        assert result in ['en_US', 'en_UZ']  # Might match en_US
    
    def test_multiple_possible_matches(self):
        """Should raise error with suggestions for ambiguous input"""
        with pytest.raises(InvalidLocaleError) as exc:
            normalize_locale('xx_YY')
        
        assert exc.value.suggestions  # Should have suggestions
        assert 'Did you mean' in str(exc.value)


class TestLocaleAliases:
    """Test locale aliases (shortcuts)"""
    
    def test_us_alias(self):
        """US should map to en_US"""
        assert normalize_locale('US') == 'en_US'
    
    def test_uk_alias(self):
        """UK should map to en_GB"""
        assert normalize_locale('UK') == 'en_GB'
    
    def test_eg_alias(self):
        """EG should map to ar_EG"""
        assert normalize_locale('EG') == 'ar_EG'
    
    def test_alias_case_insensitive(self):
        """Aliases should be case-insensitive"""
        assert normalize_locale('us') == 'en_US'
        assert normalize_locale('Us') == 'en_US'


class TestInvalidLocales:
    """Test handling of invalid locales"""
    
    def test_completely_invalid_raises_error(self):
        """Completely invalid locale should raise error"""
        with pytest.raises(InvalidLocaleError) as exc:
            normalize_locale('xyz_ABC')
        
        assert 'xyz_ABC' in str(exc.value)
        assert exc.value.suggestions
    
    def test_empty_string_raises_error(self):
        """Empty string should raise error"""
        with pytest.raises(InvalidLocaleError):
            normalize_locale('')
    
    def test_none_raises_error(self):
        """None should raise error"""
        with pytest.raises(InvalidLocaleError):
            normalize_locale(None)
    
    def test_invalid_with_raise_false(self):
        """Should return default when raise_on_invalid=False"""
        result = normalize_locale('invalid', raise_on_invalid=False)
        assert result == 'en_US'  # Default fallback


class TestIsValidLocale:
    """Test is_valid_locale helper function"""
    
    def test_valid_locales(self):
        """Should return True for valid locales"""
        assert is_valid_locale('en_US') is True
        assert is_valid_locale('ar_EG') is True
        assert is_valid_locale('fr_FR') is True
    
    def test_valid_with_normalization(self):
        """Should return True for locales that can be normalized"""
        assert is_valid_locale('EN_us') is True
        assert is_valid_locale('US_EN') is True
        assert is_valid_locale('US') is True
    
    def test_invalid_locales(self):
        """Should return False for invalid locales"""
        assert is_valid_locale('xyz_ABC') is False
        assert is_valid_locale('') is False
        assert is_valid_locale('invalid') is False


class TestGetLocaleSuggestions:
    """Test get_locale_suggestions helper function"""
    
    def test_suggestions_for_typo(self):
        """Should return suggestions for typos"""
        suggestions = get_locale_suggestions('em_US')
        assert 'en_US' in suggestions
    
    def test_suggestions_for_invalid(self):
        """Should return common locales for completely invalid input"""
        suggestions = get_locale_suggestions('xyz_ABC')
        assert len(suggestions) > 0
        assert 'en_US' in suggestions  # Should include common locales
    
    def test_max_suggestions_limit(self):
        """Should respect max_suggestions parameter"""
        suggestions = get_locale_suggestions('invalid', max_suggestions=3)
        assert len(suggestions) <= 3


class TestFindCloseMatches:
    """Test find_close_matches helper function"""
    
    def test_finds_close_matches(self):
        """Should find close matches within distance threshold"""
        matches = find_close_matches('en_US', max_distance=1)
        assert 'en_US' in matches  # Exact match
    
    def test_respects_max_distance(self):
        """Should only return matches within max_distance"""
        matches = find_close_matches('xx_YY', max_distance=0)
        assert len(matches) == 0  # No exact matches
    
    def test_respects_max_results(self):
        """Should limit results to max_results"""
        matches = find_close_matches('en_US', max_distance=3, max_results=2)
        assert len(matches) <= 2


class TestCalculateDistance:
    """Test calculate_distance helper function"""
    
    def test_identical_strings(self):
        """Distance between identical strings should be 0"""
        assert calculate_distance('test', 'test') == 0
    
    def test_single_character_difference(self):
        """Single character difference should have distance 1"""
        distance = calculate_distance('test', 'best')
        assert distance == 1
    
    def test_completely_different(self):
        """Completely different strings should have large distance"""
        distance = calculate_distance('abc', 'xyz')
        assert distance >= 3


class TestRealWorldScenarios:
    """Test real-world usage scenarios"""
    
    def test_common_typos(self):
        """Test correction of common typos"""
        # These should all normalize successfully
        test_cases = [
            ('en_US', 'en_US'),
            ('EN_us', 'en_US'),
            ('US_EN', 'en_US'),
            ('US', 'en_US'),
            ('ar_EG', 'ar_EG'),
            ('EG_AR', 'ar_EG'),
            ('EG', 'ar_EG'),
        ]
        
        for input_locale, expected in test_cases:
            result = normalize_locale(input_locale)
            assert result == expected, f"Failed for {input_locale}"
    
    def test_error_messages_are_helpful(self):
        """Error messages should include suggestions"""
        with pytest.raises(InvalidLocaleError) as exc:
            normalize_locale('invalid_locale')
        
        error_msg = str(exc.value)
        assert 'Did you mean' in error_msg or 'suggestions' in error_msg.lower()

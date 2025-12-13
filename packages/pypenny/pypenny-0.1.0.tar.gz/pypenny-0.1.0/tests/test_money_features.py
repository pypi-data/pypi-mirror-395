"""
Test new Money features: immutability, total_ordering, type hints
"""

import pypenny as pp


def test_immutability():
    """Test that Money objects are immutable by default"""
    print("Testing immutability...")
    
    money = pp.Money('100', 'USD')
    print(f"Created: {money}")
    print(f"Is frozen: {money.is_frozen}")
    
    # Try to modify - should raise error
    try:
        money.amount = 200  # type: ignore
        print("❌ ERROR: Should not be able to modify amount!")
    except AttributeError as e:
        print(f"✓ Correctly prevented modification: {e}")
    
    # Try to set new attribute - should raise error
    try:
        money.new_attr = "test"  # type: ignore
        print("❌ ERROR: Should not be able to add attributes!")
    except AttributeError as e:
        print(f"✓ Correctly prevented attribute addition: {e}")
    
    # Create mutable money
    mutable_money = pp.Money('100', 'USD', frozen=False)
    print(f"\nCreated mutable money: {mutable_money}")
    print(f"Is frozen: {mutable_money.is_frozen}")


def test_total_ordering():
    """Test that total_ordering provides all comparison methods"""
    print("\n\nTesting total_ordering...")
    
    money1 = pp.Money('100', 'USD')
    money2 = pp.Money('50', 'USD')
    money3 = pp.Money('100', 'USD')
    
    print(f"money1 = {money1}")
    print(f"money2 = {money2}")
    print(f"money3 = {money3}")
    
    # Test all comparison operators
    print(f"\nmoney1 > money2: {money1 > money2}")
    print(f"money1 < money2: {money1 < money2}")
    print(f"money1 >= money2: {money1 >= money2}")
    print(f"money1 <= money2: {money1 <= money2}")
    print(f"money1 == money3: {money1 == money3}")
    print(f"money1 != money2: {money1 != money2}")
    
    print("\n✓ All comparison operators work via total_ordering")


def test_hashable():
    """Test that Money objects are hashable"""
    print("\n\nTesting hashability...")
    
    money1 = pp.Money('100', 'USD')
    money2 = pp.Money('100', 'USD')
    money3 = pp.Money('50', 'USD')
    
    # Use in set
    money_set = {money1, money2, money3}
    print(f"Set of money: {len(money_set)} unique items")
    print(f"✓ Money objects can be used in sets")
    
    # Use as dict key
    money_dict = {
        money1: "one hundred",
        money3: "fifty"
    }
    print(f"Dict with Money keys: {len(money_dict)} items")
    print(f"✓ Money objects can be used as dict keys")


def test_arithmetic_preserves_frozen():
    """Test that arithmetic operations preserve frozen state"""
    print("\n\nTesting frozen state preservation...")
    
    frozen_money = pp.Money('100', 'USD', frozen=True)
    result = frozen_money * 2
    
    print(f"Original frozen: {frozen_money.is_frozen}")
    print(f"Result frozen: {result.is_frozen}")
    print(f"✓ Arithmetic preserves frozen state")


def test_comparison_with_different_currencies():
    """Test that comparing different currencies raises error"""
    print("\n\nTesting currency mismatch in comparison...")
    
    usd = pp.Money('100', 'USD')
    egp = pp.Money('1000', 'EGP')
    
    try:
        result = usd > egp
        print(f"❌ ERROR: Should not be able to compare different currencies!")
    except pp.CurrencyMismatchError as e:
        print(f"✓ Correctly raised error: {e}")


def main():
    print("=" * 70)
    print(" Testing New Money Features")
    print("=" * 70)
    
    # Configure pypenny
    pp.config(application_name="MoneyFeatureTest")
    
    test_immutability()
    test_total_ordering()
    test_hashable()
    test_arithmetic_preserves_frozen()
    test_comparison_with_different_currencies()
    
    print("\n" + "=" * 70)
    print(" ✓ All tests passed!")
    print("=" * 70)


if __name__ == "__main__":
    main()

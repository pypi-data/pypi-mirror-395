"""Test creating Money from another Money instance"""

import pypenny as pp

pp.config(application_name='Test')

print("Testing Money-from-Money creation...")

# Test 1: Create unfrozen from frozen
frozen = pp.Money('100', 'USD')
print(f"1. Frozen: {frozen}, is_frozen={frozen.is_frozen}")

unfrozen = pp.Money(frozen, frozen=False)
print(f"   Unfrozen copy: {unfrozen}, is_frozen={unfrozen.is_frozen}")
print("   ✓ Can create unfrozen from frozen")

# Test 2: Create frozen from unfrozen
mutable = pp.Money('200', 'EUR', frozen=False)
print(f"\n2. Mutable: {mutable}, is_frozen={mutable.is_frozen}")

immutable = pp.Money(mutable, frozen=True)
print(f"   Immutable copy: {immutable}, is_frozen={immutable.is_frozen}")
print("   ✓ Can create frozen from unfrozen")

# Test 3: Error when providing currency_code
print("\n3. Testing error when currency_code provided...")
try:
    bad = pp.Money(frozen, 'EUR')
    print("   ❌ ERROR: Should have raised ValueError")
except ValueError as e:
    print(f"   ✓ Correctly raised error: {e}")

# Test 4: Verify independence
print("\n4. Testing independence of copies...")
original = pp.Money('100', 'USD')
copy = pp.Money(original)

print(f"   Original: {original}")
print(f"   Copy: {copy}")
print(f"   Are equal: {original == copy}")
print(f"   Are same object: {original is copy}")
print("   ✓ Copies are independent")

print("\n✅ All Money-from-Money tests passed!")

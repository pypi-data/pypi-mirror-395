"""
Money wrapper class with dunder methods for arithmetic operations
"""

from decimal import Decimal
from typing import Union, Optional
from functools import total_ordering
from moneyed import Money as MoneyedMoney

from .exceptions import CurrencyMismatchError


@total_ordering
class Money:
    """
    Wrapper around py-moneyed Money with enhanced arithmetic operations.
    
    Provides dunder methods for intuitive arithmetic while maintaining
    currency safety and proper error handling.
    
    Immutable by default - once created, the amount and currency cannot be changed.
    
    Example:
        >>> money1 = Money('100', 'USD')
        >>> money2 = Money('50', 'USD')
        >>> total = money1 + money2  # $150
        >>> doubled = money1 * 2     # $200
    """
    
    __slots__ = ('_money', '_frozen')
    
    def __init__(
        self,
        amount: Union[str, Decimal, int, float, 'Money'],
        currency_code: Optional[str] = None,
        frozen: bool = True
    ) -> None:
        """
        Initialize Money object.
        
        Args:
            amount: Amount (string, Decimal, int, float) or another Money object
            currency_code: Currency code (e.g., 'USD', 'EGP'). Required unless amount is Money.
            frozen: If True, the Money object is immutable (default: True)
        
        Examples:
            >>> # Create from amount and currency
            >>> money1 = Money('100', 'USD')
            >>> money2 = Money(100, 'USD')
            
            >>> # Create from another Money instance
            >>> frozen_money = Money('100', 'USD')
            >>> unfrozen_copy = Money(frozen_money, frozen=False)
        """
        # Handle Money instance as input
        if isinstance(amount, Money):
            if currency_code is not None:
                raise ValueError(
                    "currency_code should not be provided when creating Money from another Money instance"
                )
            object.__setattr__(self, '_money', amount._money)
            object.__setattr__(self, '_frozen', frozen)
            return
        
        # Handle regular amount input
        if currency_code is None:
            raise ValueError("currency_code is required when amount is not a Money instance")
        
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))
        
        object.__setattr__(self, '_money', MoneyedMoney(amount, currency_code))
        object.__setattr__(self, '_frozen', frozen)
    
    def __setattr__(self, name: str, value) -> None:
        """Prevent modification if frozen"""
        if hasattr(self, '_frozen') and self._frozen:
            raise AttributeError(f"Money object is immutable. Cannot set attribute '{name}'")
        object.__setattr__(self, name, value)
    
    def __delattr__(self, name: str) -> None:
        """Prevent deletion if frozen"""
        if hasattr(self, '_frozen') and self._frozen:
            raise AttributeError(f"Money object is immutable. Cannot delete attribute '{name}'")
        object.__delattr__(self, name)
    
    @property
    def amount(self) -> Decimal:
        """Get the amount as Decimal"""
        return self._money.amount  # type: ignore[attr-defined]
    
    @property
    def currency(self):  # type: ignore[no-any-return]
        """Get the currency object"""
        return self._money.currency  # type: ignore[attr-defined]
    
    @property
    def currency_code(self) -> str:
        """Get the currency code"""
        return self._money.currency.code  # type: ignore[attr-defined]
    
    def get_moneyed_object(self) -> MoneyedMoney:
        """Get the underlying py-moneyed Money object"""
        return self._money  # type: ignore[attr-defined,no-any-return]
    
    # Arithmetic dunder methods
    
    def __add__(self, other: 'Money') -> 'Money':
        """Add two Money objects (money1 + money2)"""
        if not isinstance(other, Money):
            raise TypeError(f"Cannot add Money with {type(other).__name__}")
        
        if self.currency != other.currency:
            raise CurrencyMismatchError(
                "addition",
                self.currency_code,
                other.currency_code
            )
        
        result: MoneyedMoney = self._money + other._money
        return Money._from_moneyed(result, frozen=self._frozen)
    
    def __radd__(self, other: Union['Money', int]) -> 'Money':
        """Right-hand addition (other + money)"""
        if other == 0:  # Support sum() function
            return self
        return self.__add__(other)  # type: ignore
    
    def __sub__(self, other: 'Money') -> 'Money':
        """Subtract two Money objects (money1 - money2)"""
        if not isinstance(other, Money):
            raise TypeError(f"Cannot subtract {type(other).__name__} from Money")
        
        if self.currency != other.currency:
            raise CurrencyMismatchError(
                "subtraction",
                self.currency_code,
                other.currency_code
            )
        
        result: MoneyedMoney = self._money - other._money
        return Money._from_moneyed(result, frozen=self._frozen)
    
    def __mul__(self, other: Union[int, float, Decimal]) -> 'Money':
        """Multiply Money by scalar (money * 2)"""
        if not isinstance(other, (int, float, Decimal)):
            raise TypeError(f"Cannot multiply Money by {type(other).__name__}")
        
        result: MoneyedMoney = self._money * other
        return Money._from_moneyed(result, frozen=self._frozen)
    
    def __rmul__(self, other: Union[int, float, Decimal]) -> 'Money':
        """Right-hand multiplication (2 * money)"""
        return self.__mul__(other)
    
    def __truediv__(self, other: Union[int, float, Decimal]) -> 'Money':
        """Divide Money by scalar (money / 2)"""
        if not isinstance(other, (int, float, Decimal)):
            raise TypeError(f"Cannot divide Money by {type(other).__name__}")
        
        if other == 0:
            raise ZeroDivisionError("Cannot divide money by zero")
        
        result: MoneyedMoney = self._money / other
        return Money._from_moneyed(result, frozen=self._frozen)
    
    def __floordiv__(self, other: Union[int, float, Decimal]) -> 'Money':
        """Floor divide Money by scalar (money // 2)"""
        if not isinstance(other, (int, float, Decimal)):
            raise TypeError(f"Cannot floor divide Money by {type(other).__name__}")
        
        if other == 0:
            raise ZeroDivisionError("Cannot divide money by zero")
        
        # py-moneyed doesn't support //, so we implement it manually
        result_amount: Decimal = self.amount // Decimal(str(other))
        return Money(result_amount, self.currency_code, frozen=self._frozen)
    
    def __pow__(self, exponent: Union[int, float, Decimal]) -> 'Money':
        """Raise Money amount to power (money ** 2)"""
        result_amount: Decimal = self.amount ** Decimal(str(exponent))
        return Money(result_amount, self.currency_code, frozen=self._frozen)
    
    # Comparison dunder methods
    
    def __eq__(self, other: object) -> bool:
        """Check equality (money1 == money2)"""
        if not isinstance(other, Money):
            return False
        return self._money == other._money
    
    def __lt__(self, other: 'Money') -> bool:
        """Less than comparison (money1 < money2)"""
        if not isinstance(other, Money):
            return NotImplemented
        
        if self.currency != other.currency:
            raise CurrencyMismatchError(
                "comparison",
                self.currency_code,
                other.currency_code
            )
        
        return self._money < other._money
    
    def __hash__(self) -> int:
        """Make Money hashable (for use in sets/dicts)"""
        return hash((self.amount, self.currency_code))
    
    # Unary operations
    
    def __neg__(self) -> 'Money':
        """Negate Money (-money)"""
        result: MoneyedMoney = -self._money
        return Money._from_moneyed(result, frozen=self._frozen)
    
    def __pos__(self) -> 'Money':
        """Positive Money (+money)"""
        return self
    
    def __abs__(self) -> 'Money':
        """Absolute value (abs(money))"""
        result: MoneyedMoney = abs(self._money)
        return Money._from_moneyed(result, frozen=self._frozen)
    
    # String representation
    
    def __repr__(self) -> str:
        """Developer-friendly representation"""
        return f"Money('{self.amount}', '{self.currency_code}')"
    
    def __str__(self) -> str:
        """User-friendly string (use format() for locale-aware)"""
        return f"{self.currency_code} {self.amount}"
    
    # Helper methods
    
    @classmethod
    def _from_moneyed(cls, moneyed_obj: MoneyedMoney, frozen: bool = True) -> 'Money':
        """Create Money from py-moneyed Money object"""
        instance = cls.__new__(cls)
        object.__setattr__(instance, '_money', moneyed_obj)
        object.__setattr__(instance, '_frozen', frozen)
        return instance
    
    @classmethod
    def zero(cls, currency_code: str, frozen: bool = True) -> 'Money':
        """Create zero money in given currency"""
        return cls('0', currency_code, frozen=frozen)
    
    @property
    def is_frozen(self) -> bool:
        """Check if Money object is frozen (immutable)"""
        return self._frozen  # type: ignore[attr-defined,no-any-return]

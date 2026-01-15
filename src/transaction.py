"""Transaction model for expense tracker."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    """Represent a transaction (income or expense)."""

    transaction_type: str  # 'income' or 'expense'
    amount: float
    category: str
    description: str
    date: str = None
    transaction_id: int = None

    def __post_init__(self):
        """Set default date if not provided."""
        if self.date is None:
            self.date = datetime.now().strftime("%Y-%m-%d")

    def __str__(self):
        """String representation of transaction."""
        return f"{self.date} | {self.type:8} | {self.category:12} | ${self.amount:8.2f} | {self.description}"

    def to_dict(self):
        """Convert transaction to dictionary."""
        return {
            "id": self.transaction_id,
            "date": self.date,
            "type": self.transaction_type,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
        }

    @classmethod
    def from_tuple(cls, data):
        """Create transaction from database tuple."""
        transaction_id, date, trans_type, amount, category, description = data
        return cls(
            transaction_type=trans_type,
            amount=amount,
            category=category,
            description=description,
            date=date,
            transaction_id=transaction_id,
        )

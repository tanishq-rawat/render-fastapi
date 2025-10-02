"""
Expense model for tracking user expenses.
"""
from sqlalchemy import Column, Integer, Float, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class Expense(Base):
    """
    Expense model for recording user expenses.
    
    Attributes:
        id: Primary key
        amount: Expense amount (float)
        category_id: Foreign key to Category table
        description: Brief description of the expense
        date: Date when the expense occurred
        notes: Additional notes about the expense
        user_id: Foreign key to User table
        created_at: Timestamp when expense was created
        updated_at: Timestamp when expense was last updated
    """
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False, index=True)
    description = Column(Text, nullable=False)
    date = Column(Date, nullable=False, index=True)
    notes = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", backref="expenses")
    category = relationship("Category", back_populates="expenses")

    def __repr__(self):
        return f"<Expense(id={self.id}, amount={self.amount}, user_id={self.user_id}, date={self.date})>"

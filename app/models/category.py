"""
Category model for expense categorization.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class Category(Base):
    """
    Category model for organizing expenses.
    
    Attributes:
        id: Primary key
        name: Category name (e.g., Food, Transport, Entertainment)
        description: Optional description of the category
        icon: Optional icon identifier for UI
        color: Optional color code for UI (e.g., #FF5733)
        is_active: Whether the category is active
        created_at: Timestamp when category was created
        updated_at: Timestamp when category was last updated
    """
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(String(255), nullable=True)
    icon = Column(String(50), nullable=True)
    color = Column(String(7), nullable=True)  # Hex color code
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relationship with expenses
    expenses = relationship("Expense", back_populates="category")

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name})>"

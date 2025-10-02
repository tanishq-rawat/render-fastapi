"""
Pydantic schemas for expense and category endpoints.
Defines request and response models.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
import datetime as dt


# ==================== Category Schemas ====================

class CategoryBase(BaseModel):
    """Base schema for category."""
    name: str = Field(..., min_length=1, max_length=100, description="Category name")
    description: Optional[str] = Field(None, max_length=255, description="Category description")
    icon: Optional[str] = Field(None, max_length=50, description="Icon identifier")
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$", description="Hex color code")


class CategoryCreate(CategoryBase):
    """Schema for creating a category."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Food",
                "description": "Food and dining expenses",
                "icon": "restaurant",
                "color": "#FF5733"
            }
        }
    )


class CategoryResponse(CategoryBase):
    """Schema for category response."""
    id: int
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ==================== Expense Schemas ====================

class ExpenseBase(BaseModel):
    """Base schema for expense."""
    amount: float = Field(..., gt=0, description="Expense amount (must be positive)")
    category_id: int = Field(..., gt=0, description="Category ID")
    description: str = Field(..., min_length=1, max_length=500, description="Expense description")
    date: dt.date = Field(..., description="Date of expense")
    notes: Optional[str] = Field(None, max_length=1000, description="Additional notes")


class ExpenseCreate(ExpenseBase):
    """Schema for creating an expense."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "amount": 45.50,
                "category_id": 1,
                "description": "Lunch at restaurant",
                "date": "2025-10-02",
                "notes": "Business lunch with client"
            }
        }
    )


class ExpenseUpdate(BaseModel):
    """Schema for updating an expense (all fields optional)."""
    amount: Optional[float] = Field(None, gt=0, description="Expense amount")
    category_id: Optional[int] = Field(None, gt=0, description="Category ID")
    description: Optional[str] = Field(None, min_length=1, max_length=500, description="Expense description")
    date: Optional[dt.date] = Field(None, description="Date of expense")
    notes: Optional[str] = Field(None, max_length=1000, description="Additional notes")


class ExpenseResponse(ExpenseBase):
    """Schema for expense response."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)


class ExpenseWithCategory(ExpenseResponse):
    """Schema for expense response with category details."""
    category: CategoryResponse
    
    model_config = ConfigDict(from_attributes=True)

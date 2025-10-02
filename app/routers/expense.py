"""
Expense router handling expense creation, retrieval, update, and deletion.
"""
from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.expense import Expense
from app.models.category import Category
from app.schemas.expense import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse,
    ExpenseWithCategory
)
from app.utils.deps import get_current_user

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def create_expense(
    expense_data: ExpenseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new expense for the authenticated user.
    
    Creates an expense record with amount, category, description, date, and notes.
    The user_id is automatically set from the authenticated user's token.
    
    Args:
        expense_data: Expense creation data
        current_user: Currently authenticated user
        db: Database session
        
    Returns:
        Created expense data
        
    Raises:
        HTTPException: If category doesn't exist or is inactive
    """
    # Verify category exists and is active
    category = db.query(Category).filter(Category.id == expense_data.category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {expense_data.category_id} not found"
        )
    
    if not category.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create expense with inactive category"
        )
    
    # Create new expense
    new_expense = Expense(
        amount=expense_data.amount,
        category_id=expense_data.category_id,
        description=expense_data.description,
        date=expense_data.date,
        notes=expense_data.notes,
        user_id=current_user.id
    )
    
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    
    return new_expense


@router.get("", response_model=List[ExpenseWithCategory])
async def get_user_expenses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records to return"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    start_date: Optional[date] = Query(None, description="Filter expenses from this date"),
    end_date: Optional[date] = Query(None, description="Filter expenses until this date"),
    min_amount: Optional[float] = Query(None, ge=0, description="Minimum expense amount"),
    max_amount: Optional[float] = Query(None, ge=0, description="Maximum expense amount")
):
    """
    Get all expenses for the authenticated user with optional filters.
    
    Retrieves expenses for the current user with support for pagination and filtering
    by category, date range, and amount range.
    
    Args:
        current_user: Currently authenticated user
        db: Database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        category_id: Optional filter by category ID
        start_date: Optional filter for expenses from this date onwards
        end_date: Optional filter for expenses until this date
        min_amount: Optional filter for minimum expense amount
        max_amount: Optional filter for maximum expense amount
        
    Returns:
        List of expenses with category details
    """
    # Build query
    query = db.query(Expense).filter(Expense.user_id == current_user.id)
    
    # Apply filters
    if category_id:
        query = query.filter(Expense.category_id == category_id)
    
    if start_date:
        query = query.filter(Expense.date >= start_date)
    
    if end_date:
        query = query.filter(Expense.date <= end_date)
    
    if min_amount is not None:
        query = query.filter(Expense.amount >= min_amount)
    
    if max_amount is not None:
        query = query.filter(Expense.amount <= max_amount)
    
    # Order by date (most recent first) and apply pagination
    expenses = query.order_by(Expense.date.desc()).offset(skip).limit(limit).all()
    
    return expenses


@router.get("/{expense_id}", response_model=ExpenseWithCategory)
async def get_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific expense by ID.
    
    Retrieves a single expense if it belongs to the authenticated user.
    
    Args:
        expense_id: ID of the expense to retrieve
        current_user: Currently authenticated user
        db: Database session
        
    Returns:
        Expense data with category details
        
    Raises:
        HTTPException: If expense not found or doesn't belong to user
    """
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()
    
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    return expense


@router.put("/{expense_id}", response_model=ExpenseResponse)
async def update_expense(
    expense_id: int,
    expense_data: ExpenseUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing expense.
    
    Updates expense fields. Only provided fields will be updated.
    User can only update their own expenses.
    
    Args:
        expense_id: ID of the expense to update
        expense_data: Fields to update
        current_user: Currently authenticated user
        db: Database session
        
    Returns:
        Updated expense data
        
    Raises:
        HTTPException: If expense not found or doesn't belong to user
    """
    # Get expense
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()
    
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    # If category_id is being updated, verify it exists and is active
    if expense_data.category_id is not None:
        category = db.query(Category).filter(Category.id == expense_data.category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {expense_data.category_id} not found"
            )
        if not category.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot update expense with inactive category"
            )
    
    # Update fields
    update_data = expense_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(expense, field, value)
    
    db.commit()
    db.refresh(expense)
    
    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete an expense.
    
    Permanently deletes an expense. User can only delete their own expenses.
    
    Args:
        expense_id: ID of the expense to delete
        current_user: Currently authenticated user
        db: Database session
        
    Raises:
        HTTPException: If expense not found or doesn't belong to user
    """
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()
    
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    db.delete(expense)
    db.commit()
    
    return None

"""
Category router handling category creation and retrieval.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.category import Category
from app.schemas.expense import CategoryCreate, CategoryResponse
from app.utils.deps import get_current_user

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Create a new expense category.
    
    Creates a new category that can be used for organizing expenses.
    Requires authentication.
    
    Args:
        category_data: Category creation data
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        Created category data
        
    Raises:
        HTTPException: If category name already exists
    """
    # Check if category name already exists
    existing = db.query(Category).filter(Category.name == category_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category '{category_data.name}' already exists"
        )
    
    # Create new category
    new_category = Category(
        name=category_data.name,
        description=category_data.description,
        icon=category_data.icon,
        color=category_data.color
    )
    
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    return new_category


@router.get("", response_model=List[CategoryResponse])
async def get_categories(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    include_inactive: bool = False
):
    """
    Get all expense categories.
    
    Retrieves all categories available for expense tracking.
    By default, only active categories are returned.
    
    Args:
        db: Database session
        current_user: Currently authenticated user
        include_inactive: Whether to include inactive categories
        
    Returns:
        List of categories
    """
    query = db.query(Category)
    
    if not include_inactive:
        query = query.filter(Category.is_active == True)
    
    categories = query.order_by(Category.name).all()
    return categories


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get a specific category by ID.
    
    Args:
        category_id: ID of the category to retrieve
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        Category data
        
    Raises:
        HTTPException: If category not found
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    return category

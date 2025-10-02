"""
Script to seed the database with default categories.
Run this script to populate initial categories for expense tracking.
"""
from app.database import SessionLocal
from app.models.category import Category


def seed_categories():
    """Seed default expense categories."""
    db = SessionLocal()
    
    try:
        # Check if categories already exist
        existing_count = db.query(Category).count()
        if existing_count > 0:
            print(f"✅ Database already has {existing_count} categories. Skipping seed.")
            return
        
        # Default categories
        default_categories = [
            {
                "name": "Food & Dining",
                "description": "Groceries, restaurants, and food delivery",
                "icon": "restaurant",
                "color": "#FF5733"
            },
            {
                "name": "Transportation",
                "description": "Fuel, public transport, taxi, and vehicle maintenance",
                "icon": "directions_car",
                "color": "#3498DB"
            },
            {
                "name": "Shopping",
                "description": "Clothing, electronics, and general shopping",
                "icon": "shopping_cart",
                "color": "#9B59B6"
            },
            {
                "name": "Entertainment",
                "description": "Movies, games, hobbies, and leisure activities",
                "icon": "movie",
                "color": "#E74C3C"
            },
            {
                "name": "Bills & Utilities",
                "description": "Electricity, water, internet, and phone bills",
                "icon": "receipt",
                "color": "#F39C12"
            },
            {
                "name": "Healthcare",
                "description": "Medical expenses, pharmacy, and health insurance",
                "icon": "local_hospital",
                "color": "#1ABC9C"
            },
            {
                "name": "Education",
                "description": "Courses, books, and educational materials",
                "icon": "school",
                "color": "#34495E"
            },
            {
                "name": "Travel",
                "description": "Vacation, hotel, and travel expenses",
                "icon": "flight",
                "color": "#16A085"
            },
            {
                "name": "Personal Care",
                "description": "Salon, spa, and personal grooming",
                "icon": "face",
                "color": "#E91E63"
            },
            {
                "name": "Other",
                "description": "Miscellaneous expenses",
                "icon": "more_horiz",
                "color": "#95A5A6"
            }
        ]
        
        # Create categories
        for cat_data in default_categories:
            category = Category(**cat_data)
            db.add(category)
        
        db.commit()
        print(f"✅ Successfully seeded {len(default_categories)} categories")
        
        # Display created categories
        print("\nCreated categories:")
        for cat in default_categories:
            print(f"  - {cat['name']} ({cat['color']})")
        
    except Exception as e:
        print(f"❌ Error seeding categories: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("🌱 Seeding database with default categories...")
    seed_categories()

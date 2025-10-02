"""
User model for authentication and user management.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, timezone
from app.database import Base


class User(Base):
    """
    User model representing registered users in the system.
    
    Attributes:
        id: Primary key
        email: Unique email address for login
        username: Unique username for display
        hashed_password: Bcrypt hashed password
        is_active: Whether the user account is active
        is_verified: Whether the user email is verified
        created_at: Timestamp when user was created
        updated_at: Timestamp when user was last updated
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"

# Expense Tracker PWA - Backend

A FastAPI backend for a Progressive Web App (PWA) expense tracking application with JWT authentication.

## 🚀 Features

- **User Authentication**: Register, login, and JWT token management
- **Access & Refresh Tokens**: Secure token-based authentication with token refresh capability
- **Expense Tracking**: Create, read, update, and delete expenses
- **Category Management**: Organize expenses with customizable categories
- **Advanced Filtering**: Filter expenses by category, date range, and amount
- **User Isolation**: Each user can only access their own data
- **SQLite Database**: Lightweight database for development
- **Password Hashing**: Secure password storage using bcrypt
- **Input Validation**: Pydantic schemas for request/response validation
- **API Documentation**: Auto-generated Swagger UI and ReDoc

## 📁 Project Structure

```
PWA-Backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration and settings
│   ├── database.py          # Database setup and session management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User database model
│   │   ├── category.py      # Category database model
│   │   └── expense.py       # Expense database model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py          # Pydantic schemas for auth
│   │   └── expense.py       # Pydantic schemas for expenses
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── category.py      # Category endpoints
│   │   └── expense.py       # Expense endpoints
│   └── utils/
│       ├── __init__.py
│       ├── security.py      # JWT and password utilities
│       └── deps.py          # FastAPI dependencies
├── seed_categories.py       # Script to populate default categories
├── requirements.txt         # Python dependencies
├── .env.example            # Example environment variables
├── README.md
└── EXPENSE_API_GUIDE.md    # Complete API documentation
```

## 🛠️ Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

**Important**: Change the `SECRET_KEY` in `.env` to a secure random string:

```bash
# Generate a secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Update your `.env` file with the generated key.

### 4. Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### 5. Seed Default Categories (Optional but Recommended)

```bash
python seed_categories.py
```

This will populate the database with 10 default expense categories.

## 📚 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/register` | Register a new user | No |
| POST | `/api/v1/auth/login` | Login and get tokens | No |
| POST | `/api/v1/auth/refresh` | Refresh access token | No |
| GET | `/api/v1/auth/me` | Get current user info | Yes |

### Category Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/categories` | Create a new category | Yes |
| GET | `/api/v1/categories` | Get all categories | Yes |
| GET | `/api/v1/categories/{id}` | Get category by ID | Yes |

### Expense Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/expenses` | Create a new expense | Yes |
| GET | `/api/v1/expenses` | Get user's expenses (with filters) | Yes |
| GET | `/api/v1/expenses/{id}` | Get expense by ID | Yes |
| PUT | `/api/v1/expenses/{id}` | Update an expense | Yes |
| DELETE | `/api/v1/expenses/{id}` | Delete an expense | Yes |

### Health Check Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |

## 🔐 Authentication Flow

### 1. Register a New User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "SecurePass123!"
  }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### 3. Create an Expense

```bash
curl -X POST "http://localhost:8000/api/v1/expenses" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 45.50,
    "category_id": 1,
    "description": "Lunch at restaurant",
    "date": "2025-10-02",
    "notes": "Business lunch"
  }'
```

### 4. Get Your Expenses

```bash
# Get all expenses
curl -X GET "http://localhost:8000/api/v1/expenses" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Filter by category and date range
curl -X GET "http://localhost:8000/api/v1/expenses?category_id=1&start_date=2025-10-01&end_date=2025-10-31" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 📖 API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔑 JWT Token Details

### Access Token
- **Purpose**: Authenticate API requests
- **Lifetime**: 30 minutes (configurable)
- **Usage**: Include in `Authorization: Bearer <token>` header

### Refresh Token
- **Purpose**: Obtain new access tokens
- **Lifetime**: 7 days (configurable)
- **Usage**: Send to `/api/v1/auth/refresh` endpoint

## 🗄️ Database Schema

### Users Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| email | String | Unique email address |
| username | String | Unique username |
| hashed_password | String | Bcrypt hashed password |
| is_active | Boolean | Account active status |
| is_verified | Boolean | Email verification status |
| created_at | DateTime | Account creation timestamp |
| updated_at | DateTime | Last update timestamp |

### Categories Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| name | String | Category name (unique) |
| description | String | Category description |
| icon | String | Icon identifier |
| color | String | Hex color code |
| is_active | Boolean | Category active status |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

### Expenses Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| amount | Float | Expense amount |
| category_id | Integer | Foreign key to categories |
| description | Text | Expense description |
| date | Date | Date of expense |
| notes | Text | Additional notes |
| user_id | Integer | Foreign key to users |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

## 🧪 Testing with cURL

### Register User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"Test1234!"}'
```

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test1234!"}'
```

### Get User Info
```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🔒 Security Best Practices

1. **Never commit `.env` file** - Contains sensitive information
2. **Use strong SECRET_KEY** - Generate using cryptographically secure method
3. **HTTPS in Production** - Always use HTTPS for API in production
4. **CORS Configuration** - Restrict allowed origins in production
5. **Token Storage** - Store tokens securely on client side (HTTPOnly cookies or secure storage)

## 📝 Next Steps

This backend now provides:
- ✅ Complete user authentication system
- ✅ Expense tracking with CRUD operations
- ✅ Category management
- ✅ Advanced filtering and pagination
- ✅ User data isolation

### Recommended Enhancements:
- Analytics and statistics endpoints
- Budget tracking and alerts
- Recurring expenses
- Export functionality (CSV/PDF)
- Multi-currency support
- Receipt attachment uploads
- Shared expenses for groups

## 📖 Additional Documentation

For detailed API usage, examples, and testing workflows, see:
- **[EXPENSE_API_GUIDE.md](./EXPENSE_API_GUIDE.md)** - Complete expense API documentation

## 🤝 Development Notes

- Code is well-documented with docstrings
- Type hints used throughout
- Follows FastAPI best practices
- Modular structure for easy expansion
- Environment-based configuration
- Comprehensive error handling

## 📄 License

This project is for educational purposes.

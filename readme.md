# Coding Challenge – Simple User Registration

A Flask-based web application that implements secure user registration, login, session management, and profile updates using PostgreSQL as the database.


##  Features

- **User Registration** (`/signup`)
  - Email, full name, and password storage
  - Password must be at least 8 characters with at least one letter and one number
  - Full name must be at least 5 characters
  - Email is unique (used as user identifier)
  - Success message on registration
  - Passwords hashed using bcrypt

- **User Login** (`/login`)
  - Email and password authentication
  - Account lockout after 3 failed attempts (2-hour duration)
  - Welcome message with user's full name and logout link
  - Single active session per user (prevents concurrent logins)
  - Session timeout after 15 minutes of inactivity

- **Profile Management** (`/profile`)
  - View and update full name
  

- **Dashboard** (`/dashboard`)
  - Welcome page with user's name
  - Link to edit profile and logout

- **Session Security**
  - HTTP-only cookies for session IDs
  - Session stored in database 
  - Automatic logout on inactivity

---

##  Tech Stack

- **Backend**: Python 3.10+, Flask 2.3.3
- **Database**: PostgreSQL 14+ with psycopg2-binary
- **ORM**: Flask-SQLAlchemy 3.1.1
- **Security**: bcrypt for password hashing, email-validator for email validation
- **Environment**: python-dotenv for configuration management
- **Version Control**: Git with Conventional Commits and dev/master branching strategy

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Josecruzangel5/SimpleUserRegistration
cd SUR
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate   # On Linux/ubuntu
# On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and configure PostgreSQL 


### 5. Create the database and user

---

## Configuration

Create a `.env` file in the project root with the following variables:

```env
SECRET_KEY=your_generated_secret_key_here
DATABASE_URL=postgresql://your_username:your_secure_password@localhost:5432/SUR
```

Generate a secure secret key:

```bash
openssl rand -hex 32
```

---

##  Database Setup

Initialize the database tables:

```bash
flask shell
```

Inside the Flask shell:

```python
>>> from app import db, create_app
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
...     print("✅ Tables created successfully")
... 
>>> exit()
```


##  Running the Application

```bash
python run.py
```

The application will be available at:
- http://localhost:5000
- http://127.0.0.1:5000
- http://192.168.0.x:5000 (your local IP)

---

## Project Structure

```
SUR/
├── app/
│   ├── __init__.py          # Flask application factory
│   ├── models.py            # User and Session models
│   ├── auth.py              # Authentication routes (signup, login, logout, profile, dashboard)
│   ├── middlewares.py       # Session validation and inactivity timeout
│   ├── utils.py             # Password hashing and validation utilities
│   └── templates/           # HTML templates
│       ├── base.html        # Base template with Bootstrap
│       ├── signup.html      # Registration form
│       ├── login.html       # Login form
│       ├── dashboard.html   # Welcome page
│       └── profile.html     # Profile update form
├── config.py                # Application configuration
├── .env                     # Environment variables (not in Git)
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── README.md                # Project documentation
```

---


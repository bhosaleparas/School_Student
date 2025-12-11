# School Management API

A simple FastAPI-based REST API for managing Students and Schools with a clean separation of concerns.

## Features

- **Student Management**: Create and retrieve students
- **School Management**: Create and retrieve schools
- **Relationships**: Get students with their school details and vice versa
- **Simple JSON API**: Clean request/response format
- **SQLite Database**: Lightweight and file-based

## Project Structure

```
school_api/
├── main.py          # FastAPI application and endpoints
├── models.py        # SQLAlchemy models (School, Student)
├── database.py      # Database configuration and session handling
├── requirements.txt # Python dependencies
└── school.db        # SQLite database (auto-generated)
```

## Installation

1. **Clone or create the project directory**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI server:
```bash
uvicorn main:app --reload
```

The API will be available at:
- **API Server**: `http://localhost:8000`
- **Interactive API Documentation (Swagger UI)**: `http://localhost:8000/docs`
- **Alternative Documentation (ReDoc)**: `http://localhost:8000/redoc`

## API Endpoints

### Root Endpoint
- **GET** `/` - Get API information and available endpoints

### School Endpoints
```bash
schools: {
                "create_school": "POST /schools/",
                "get_all_schools": "GET /schools/",
                "get_school": "GET /schools/{id}",
                "get_school_students": "GET /schools/{id}/students"
            }
```


### Student Endpoints

```bash
students: {
                "create_student": "POST /students/",
                "get_all_students": "GET /students/",
                "get_student_with_school": "GET /students/{id}"
            }
```
## Request/Response Examples

### 1. Create a School
**Request:**
```bash
curl -X POST "http://localhost:8000/schools/?name=Greenwood High&address=456 Oak Ave&email=contact@greenwood.edu"
```

**Response:**
```json
{
  "id": 1,
  "name": "Greenwood High",
  "address": "456 Oak Ave",
  "email": "contact@greenwood.edu",
  "message": "School created successfully"
}
```

### 2. Create a Student
**Request:**
```bash
curl -X POST "http://localhost:8000/students/?name=Alice Johnson&age=16&email=alice@example.com&school_id=1"
```

**Response:**
```json
{
  "id": 1,
  "name": "Alice Johnson",
  "age": 16,
  "email": "alice@example.com",
  "school_id": 1,
  "message": "Student created successfully"
}
```

### 3. Get All Schools
**Request:**
```bash
curl "http://localhost:8000/schools/"
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Greenwood High",
    "address": "456 Oak Ave",
    "email": "contact@greenwood.edu",
    "student_count": 3
  }
]
```

### 4. Get Student with School Details
**Request:**
```bash
curl "http://localhost:8000/students/1"
```

**Response:**
```json
{
  "id": 1,
  "name": "Alice Johnson",
  "age": 16,
  "email": "alice@example.com",
  "school": {
    "id": 1,
    "name": "Greenwood High",
    "address": "456 Oak Ave",
    "email": "contact@greenwood.edu"
  }
}
```

### 5. Get All Students of a School
**Request:**
```bash
curl "http://localhost:8000/schools/1/students"
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Alice Johnson",
    "age": 16,
    "email": "alice@example.com"
  },
  {
    "id": 2,
    "name": "Bob Smith",
    "age": 17,
    "email": "bob@example.com"
  }
]
```
## Error Handling

The API returns appropriate HTTP status codes:

- **200**: Success
- **400**: Bad Request (e.g., duplicate email)
- **404**: Not Found (e.g., school/student not found)

Example error response:
```json
{
  "detail": "School not found"
}
```

## Dependencies

- **FastAPI**: Web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Lightweight database engine

## Development

### Creating Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```
## License

This is a sample project for educational purposes.

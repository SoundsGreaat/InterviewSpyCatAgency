# Spy Cat Agency Management System

A RESTful API for managing spy cats, their missions, and targets. Built with FastAPI and PostgreSQL.

## Features

- **Spy Cats Management**: Create, read, update, and delete spy cats
- **Missions Management**: Create missions with 1-3 targets, assign cats, track completion
- **Targets Management**: Update notes and completion status, automatic mission completion
- **Breed Validation**: Integration with TheCatAPI for breed validation
- **Business Logic**:
    - One cat can only have one active mission at a time
    - Missions cannot be deleted if assigned to a cat
    - Notes are frozen when target or mission is complete

## Project Tree

```
├── app
│   ├── __init__.py
│   ├── crud.py                 Database operations
│   ├── database.py             Database configuration
│   ├── main.py                 FastAPI application entry point
│   ├── models.py               SQLAlchemy models
│   ├── routers
│   │   ├── __init__.py
│   │   ├── cats.py             Spy cats endpoints
│   │   ├── missions.py         Missions & targets endpoints
│   ├── schemas.py              Pydantic schemas
│   └── services
│       ├── __init__.py
│       ├── cat_api.py          TheCatAPI integration
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```

## Setup Instructions

### Prerequisites

- Docker and Docker Compose installed on your machine

### Installation

1. **Clone the repository**

2. **Create `.env` file in the root directory**:

```env
DATABASE_URL=postgresql://user:password@postgres:5432/spy_cat_agency
CAT_API_URL=https://api.thecatapi.com/v1
```

3. **Run with Docker Compose**:

```bash
docker-compose up -d
```

- The API will be available at http://localhost:8000
- Documentation will be available at http://localhost:8000/docs

### API Documentation

Once the server is running, visit:

- [**Swagger UI**](http://localhost:8000/docs)
- [**Postman Collection**](https://www.postman.com/descent-module-geoscientist-86082184/interview/collection/0jcuuwc/interviewspycatagency?action=share&source=copy-link&creator=30837098)

## Business Rules

1. **Breed Validation**: All cat breeds are validated with TheCatAPI
2. **Mission Assignment**:
    - A cat can only have one active (incomplete) mission at a time
    - Missions can only be deleted if not assigned to any cat
3. **Target Management**:
    - Each mission must have 1-3 targets
    - Notes are frozen once a target is marked complete
    - Notes are frozen if the mission is marked complete
4. **Mission Completion**:
    - When all targets are marked complete, the mission is automatically marked complete

## Database Schema

### Tables

**spy_cats**

- id (Primary Key)
- name (String)
- years_of_experience (Integer)
- breed (String)
- salary (Float)

**missions**

- id (Primary Key)
- cat_id (Foreign Key → spy_cats.id, nullable)
- is_complete (Boolean, default: False)

**targets**

- id (Primary Key)
- mission_id (Foreign Key -> missions.id)
- name (String)
- country (String)
- notes (Text)
- is_complete (Boolean, default: False)

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK` - Successful GET/PATCH requests
- `201 Created` - Successful POST requests
- `204 No Content` - Successful DELETE requests
- `400 Bad Request` - Invalid input or business rule violation
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error

## Development Notes

- The application uses SQLAlchemy ORM for database operations
- Pydantic models handle request/response validation
- Async HTTP client (httpx) for TheCatAPI integration
- Database tables are created automatically on startup
- The API follows RESTful conventions
# Inventory Management System - Backend API

### Built with Django Rest Framework (DRF)

## Overview

This project provides a backend API for managing inventory items, supporting full CRUD operations. It secures endpoints using JWT authentication, caches frequently accessed items with Redis, and utilizes PostgreSQL as the database. The project includes logging for debugging and monitoring and unit tests to ensure functionality.

---

## Features

- **CRUD operations** for inventory items
- **JWT-based authentication** for secure API access
- **Redis caching** for frequently accessed items
- **Django ORM** for database interactions with PostgreSQL
- **Logging** of all significant events and errors

## Technologies

- **Django** and **Django Rest Framework (DRF)**
- **PostgreSQL** for database management
- **Redis** for caching
- **JWT** for secure user authentication
- **Logging** for monitoring and debugging

---

## Setup and Installation

### Prerequisites

- Python 3.8+
- PostgreSQL
- Redis
- Git (for cloning the repository)

### Installation Steps

1. **Clone the repository**:

   ```bash
   git clone https://github.com/jawaharmuthukumaran/inventory-management.git
   cd inventory_management
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the PostgreSQL Database**:

   - Create a PostgreSQL database and a user.
   - Update the database settings in `settings.py`:
     ```python
     DATABASES = {
         "default": {
             "ENGINE": "django.db.backends.postgresql_psycopg2",
             "NAME": "<database_name>",
             "USER": "<database_user>",
             "PASSWORD": "<database_password>",
             "HOST": "localhost",
             "PORT": "5432",
         }
     }
     ```

4. **Run Migrations**:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Configure Redis for Caching**:
   Ensure Redis is running locally and configured in `settings.py`:

   ```python
   CACHES = {
       "default": {
           "BACKEND": "django_redis.cache.RedisCache",
           "LOCATION": "redis://127.0.0.1:6379/1",
           "OPTIONS": {
               "CLIENT_CLASS": "django_redis.client.DefaultClient",
           },
       }
   }
   ```

6. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

---

## API Endpoints

### Authentication

- **User Registration**:

  - **URL**: `/auth/register/`
  - **Method**: `POST`
  - **Request Body**: `{ "username": "user", "password": "pass" }`

- **User Login**:
  - **URL**: `/auth/login/`
  - **Method**: `POST`
  - **Request Body**: `{ "username": "user", "password": "pass" }`
  - **Response**: JWT token for authentication

### Inventory Management

- **Create Item**:

  - **URL**: `/items/`
  - **Method**: `POST`
  - **Request Body**: `{ "item_name": "item name", "item_code": "item_code", "description": "item description", "quantity": "quantity of items", "price": "price of the item }`
  - **Response**: Details of the created item

- **Read Items**:

  - **URL**: `/items/`
  - **Method**: `GET`
  - **Response**: All item details
  - **Caching**: Results are cached in Redis

- **Read Item**:

  - **URL**: `/items/{item_id}/`
  - **Method**: `GET`
  - **Response**: Item details
  - **Caching**: Results are cached in Redis

- **Update Item**:

  - **URL**: `/items/{item_id}/`
  - **Method**: `PUT`
  - **Request Body**: `{ "item_name": "new item name", "item_code": "new_item_code", "description": "new item description", "quantity": "updated quantity of items", "price": "updated price of the item }`
  - **Response**: Updated item details

- **Delete Item**:
  - **URL**: `/items/{item_id}/`
  - **Method**: `DELETE`
  - **Response**: Success message

**Error Codes**:

- `400`: Bad Request (e.g., item already exists)
- `404`: Not Found (e.g., item or user not found)
- `401`: Unauthorized (e.g., missing or invalid JWT)

---

## Testing

Run unit tests to verify all functionalities:

```bash
python manage.py test
```

---

## Logging

The application logs all major events and errors to `inventory.log`. Logs are stored in the project root directory and provide a detailed view of the API operations and any errors encountered.

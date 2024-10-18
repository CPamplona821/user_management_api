# User Management REST API

This is a basic implementation of the User Management REST API using Python, FastAPI, and MongoDB.

## Features

- User Registration
- User Login
- Email Verification
- Profile Management (CRUD)
- Role-Based Access Control (RBAC)
- Error Handling

## Running the Project

1. Clone the repository: `git clone https://github.com/your-username/user-management-api.git`
2. Navigate to the project directory: `cd user-management-api`
3. Create a `.env` file and configure your MongoDB connection and other settings.
4. Install the required dependencies: `pip install -r requirements.txt`
5. Run the application: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
6. Open your web browser and navigate to `http://localhost:8000/docs` to access the API documentation.

## API Endpoints

- **POST /register**: Register a new user.
- **POST /login**: Login a user and receive a JWT token.
- **GET /users/me**: Get the current user's profile.
- **GET /users/**: Retrieve all user profiles (Admin-only).
- **GET /users/{user_id}**: Retrieve a single user profile.
- **PUT /users/{user_id}**: Update a user profile.
- **DELETE /users/{user_id}**: Delete a user profile.

## Running Tests

To run the tests, make sure you have `pytest` installed, then run:

```bash
pytest tests/test_main.py

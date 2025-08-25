# OpenManus Backend API

This is the backend API for the OpenManus AI Agent application.

## Features

- RESTful API for chat functionality
- SQLite database for persistent storage
- Conversation and message management
- CORS enabled for frontend integration
- Production-ready with Gunicorn

## API Endpoints

### GET /api/status
Returns the API status and information.

### POST /api/chat
Send a message and receive an AI response.

**Request Body:**
```json
{
  "message": "Your message here",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "AI response",
  "task": "Identified task",
  "tools": ["list", "of", "tools"],
  "conversation_id": 1,
  "message_id": 2
}
```

### GET /api/conversations
Retrieve conversation history for a session.

**Query Parameters:**
- `session_id`: Session identifier (optional, defaults to "default")

## Deployment

### Railway
1. Connect your GitHub repository
2. Set environment variables
3. Deploy

### Heroku
1. Create a new Heroku app
2. Connect to GitHub repository
3. Set environment variables
4. Deploy

### Render
1. Create a new web service
2. Connect to GitHub repository
3. Set build and start commands
4. Deploy

## Environment Variables

- `SECRET_KEY`: Flask secret key for sessions
- `DATABASE_URL`: Database connection string
- `PORT`: Port number (default: 5000)

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`


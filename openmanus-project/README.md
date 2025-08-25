# OpenManus - AI Agent for Any Task

A modern, open-source AI agent interface inspired by the original Manus, built with React and Flask. OpenManus provides a clean, intuitive interface for interacting with AI agents capable of web browsing, coding, file editing, data analysis, and more.

## 🚀 Features

- **Modern UI**: Clean, responsive interface built with React and Tailwind CSS
- **Persistent Chat**: SQLite database for storing conversations and chat history
- **Multi-Tool Support**: Simulated support for various AI agent tools:
  - 🌐 Web Browsing
  - 💻 Code Execution
  - 🖥️ Shell Commands
  - 📝 File Editing
  - 🎨 Image Generation
  - 📊 Data Analysis
- **Session Management**: Automatic session handling and conversation tracking
- **Real-time Responses**: Dynamic response generation based on user input
- **Mobile Responsive**: Works seamlessly on desktop and mobile devices

## 🛠️ Tech Stack

### Frontend
- **React 18** - Modern React with hooks
- **Vite** - Fast build tool and development server
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - High-quality UI components
- **Lucide Icons** - Beautiful, customizable icons

### Backend
- **Flask** - Lightweight Python web framework
- **SQLite** - Embedded database for data persistence
- **Flask-CORS** - Cross-origin resource sharing support
- **SQLAlchemy** - Python SQL toolkit and ORM

## 📦 Installation

### Prerequisites
- Node.js 18+ and npm/pnpm
- Python 3.11+
- Git

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd openmanus-project
   ```

2. **Install frontend dependencies**
   ```bash
   npm install
   ```

3. **Set up backend environment**
   ```bash
   cd api
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Start the development servers**
   
   Backend (in one terminal):
   ```bash
   cd api
   source venv/bin/activate
   python main.py
   ```
   
   Frontend (in another terminal):
   ```bash
   npm run dev
   ```

5. **Open your browser**
   Navigate to `http://localhost:5173` to see the application.

## 🚀 Deployment

### Netlify Deployment (Frontend)
1. Build the project: `npm run build`
2. Deploy the `dist` folder to Netlify
3. Configure redirects for SPA routing

### Backend Hosting
The backend can be deployed to:
- **Heroku**: Use the included `Procfile`
- **Railway**: Direct deployment from Git
- **DigitalOcean App Platform**: Container or buildpack deployment
- **AWS/GCP/Azure**: Various deployment options available

## 📁 Project Structure

```
openmanus-project/
├── src/                    # React frontend source
│   ├── components/         # React components
│   ├── hooks/             # Custom React hooks
│   ├── lib/               # Utility functions
│   └── assets/            # Static assets
├── api/                   # Flask backend
│   ├── models/            # Database models
│   ├── routes/            # API routes
│   ├── static/            # Static files
│   └── database/          # SQLite database
├── dist/                  # Built frontend (production)
├── public/                # Public assets
└── package.json           # Frontend dependencies
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
# Backend Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///app.db

# Frontend Configuration (optional)
VITE_API_URL=http://localhost:5000
```

### Database
The application uses SQLite by default. The database is automatically created on first run with the following tables:
- `conversations` - Chat conversation metadata
- `messages` - Individual chat messages
- `agent_sessions` - User session tracking

## 🎯 Usage

1. **Start a Conversation**: Type your message in the input field
2. **Agent Response**: The AI agent will analyze your request and respond appropriately
3. **Tool Selection**: Based on your request, the agent will indicate which tools it would use
4. **Persistent History**: All conversations are saved and can be resumed later

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📝 API Documentation

### Endpoints

#### `POST /api/chat`
Send a message to the AI agent.

**Request Body:**
```json
{
  "message": "Help me create a website"
}
```

**Response:**
```json
{
  "response": "I'll help you create a website!...",
  "task": "Website development and design",
  "tools": ["code", "file", "browser"],
  "conversation_id": 1,
  "message_id": 2
}
```

#### `GET /api/conversations`
Get all conversations for the current session.

#### `GET /api/conversations/{id}/messages`
Get all messages for a specific conversation.

#### `GET /api/status`
Check API status and configuration.

## 🔒 Security

- Session-based authentication
- CORS protection
- Input validation and sanitization
- SQL injection prevention through ORM

## 📊 Database Schema

### Conversations
- `id` - Primary key
- `session_id` - User session identifier
- `title` - Conversation title
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

### Messages
- `id` - Primary key
- `conversation_id` - Foreign key to conversations
- `message_type` - 'user' or 'assistant'
- `content` - Message content
- `timestamp` - Message timestamp
- `task_description` - Agent task description
- `tools_used` - JSON array of tools used

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `main.py` or kill the existing process
2. **Database errors**: Delete the database file to reset
3. **CORS errors**: Ensure Flask-CORS is properly configured
4. **Build failures**: Clear node_modules and reinstall dependencies

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the original Manus AI agent
- Built with modern web technologies
- UI components from shadcn/ui
- Icons from Lucide

## 🔗 Links

- [Live Demo](https://your-netlify-url.netlify.app)
- [GitHub Repository](https://github.com/your-username/openmanus-project)
- [Issues](https://github.com/your-username/openmanus-project/issues)

---

**OpenManus** - Making AI agents accessible to everyone. 🤖✨


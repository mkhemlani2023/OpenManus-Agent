import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///openmanus.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
CORS(app, origins=['*'])  # Allow all origins for now

# Database Models
class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    messages = db.relationship('Message', backref='conversation', lazy=True, cascade='all, delete-orphan')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    tools_used = db.Column(db.Text)  # JSON string of tools used

# Create tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        'status': 'online',
        'message': 'OpenManus API is running',
        'version': '1.0.0',
        'database': 'SQLite',
        'features': ['chat', 'conversations', 'persistent_storage']
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Find or create conversation
        conversation = Conversation.query.filter_by(session_id=session_id).first()
        if not conversation:
            conversation = Conversation(session_id=session_id)
            db.session.add(conversation)
            db.session.commit()
        
        # Save user message
        user_msg = Message(
            conversation_id=conversation.id,
            role='user',
            content=user_message
        )
        db.session.add(user_msg)
        
        # Generate AI response based on user input
        response_content = generate_response(user_message)
        task = determine_task(user_message)
        tools = determine_tools(user_message)
        
        # Save assistant response
        assistant_msg = Message(
            conversation_id=conversation.id,
            role='assistant',
            content=response_content,
            tools_used=json.dumps(tools) if tools else None
        )
        db.session.add(assistant_msg)
        
        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'response': response_content,
            'task': task,
            'tools': tools,
            'conversation_id': conversation.id,
            'message_id': assistant_msg.id
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/conversations', methods=['GET'])
def get_conversations():
    try:
        session_id = request.args.get('session_id', 'default')
        conversation = Conversation.query.filter_by(session_id=session_id).first()
        
        if not conversation:
            return jsonify({'messages': []})
        
        messages = Message.query.filter_by(conversation_id=conversation.id).order_by(Message.timestamp).all()
        
        message_list = []
        for msg in messages:
            message_data = {
                'id': msg.id,
                'role': msg.role,
                'content': msg.content,
                'timestamp': msg.timestamp.isoformat(),
                'tools': json.loads(msg.tools_used) if msg.tools_used else []
            }
            message_list.append(message_data)
        
        return jsonify({
            'conversation_id': conversation.id,
            'messages': message_list
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_response(user_message):
    """Generate AI response based on user input"""
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in ['wordpress', 'theme', 'website', 'site']):
        return "I understand your request! I'm a versatile AI agent that can help with web browsing, coding, file editing, data analysis, image generation, and much more. Let me work on this task for you."
    
    elif any(word in message_lower for word in ['code', 'programming', 'develop']):
        return "I'll help you create a website! Let me start by understanding your requirements and then build the HTML, CSS, and any necessary JavaScript. I can create responsive designs, add interactive features, and ensure your site looks professional."
    
    elif any(word in message_lower for word in ['data', 'analysis', 'chart', 'graph']):
        return "I can help you analyze data and create visualizations! I'll process your data, identify patterns, and create insightful charts and graphs to help you understand your information better."
    
    elif any(word in message_lower for word in ['image', 'picture', 'photo', 'generate']):
        return "I can generate and edit images for you! Whether you need original artwork, photo editing, or visual content creation, I'll help you create exactly what you're looking for."
    
    else:
        return "I understand your request! I'm a versatile AI agent that can help with web browsing, coding, file editing, data analysis, image generation, and much more. Let me work on this task for you."

def determine_task(user_message):
    """Determine the main task based on user input"""
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in ['wordpress', 'theme', 'website', 'site']):
        return "Website development and design"
    elif any(word in message_lower for word in ['code', 'programming', 'develop']):
        return "Code development and programming"
    elif any(word in message_lower for word in ['data', 'analysis', 'chart']):
        return "Data analysis and visualization"
    elif any(word in message_lower for word in ['image', 'picture', 'photo']):
        return "Image generation and editing"
    else:
        return "Processing your request using available tools"

def determine_tools(user_message):
    """Determine which tools to use based on user input"""
    message_lower = user_message.lower()
    tools = []
    
    if any(word in message_lower for word in ['website', 'site', 'web', 'html', 'css']):
        tools.extend(['code', 'file', 'browser'])
    elif any(word in message_lower for word in ['code', 'programming', 'script']):
        tools.extend(['code', 'file', 'terminal'])
    elif any(word in message_lower for word in ['data', 'analysis', 'chart']):
        tools.extend(['code', 'database', 'file'])
    elif any(word in message_lower for word in ['image', 'picture', 'photo']):
        tools.extend(['image', 'file'])
    else:
        tools.extend(['terminal', 'code', 'file'])
    
    return tools

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)


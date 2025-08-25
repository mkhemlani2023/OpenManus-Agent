from flask import Blueprint, request, jsonify, session
from flask_cors import cross_origin
from datetime import datetime
import uuid
import time
import random

from src.models.user import db
from src.models.chat import Conversation, Message, AgentSession

chat_bp = Blueprint('chat', __name__)

def get_or_create_session():
    """Get or create a session ID for the user"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

def get_or_create_agent_session(session_id, user_agent=None, ip_address=None):
    """Get or create an agent session record"""
    agent_session = AgentSession.query.filter_by(session_id=session_id).first()
    if not agent_session:
        agent_session = AgentSession(
            session_id=session_id,
            user_agent=user_agent,
            ip_address=ip_address
        )
        db.session.add(agent_session)
    else:
        agent_session.last_active = datetime.utcnow()
    
    db.session.commit()
    return agent_session

def generate_agent_response(user_message, conversation_id):
    """Generate an appropriate agent response based on user input"""
    start_time = time.time()
    
    # Analyze user message and determine response
    user_message_lower = user_message.lower()
    
    if any(keyword in user_message_lower for keyword in ['website', 'web', 'browse', 'url', 'html', 'css']):
        response_data = {
            "content": "I'll help you create a website! Let me start by understanding your requirements and then build the HTML, CSS, and any necessary JavaScript. I can create responsive designs, add interactive features, and ensure your site looks professional.",
            "task": "Website development and design",
            "tools": ["code", "file", "browser"]
        }
    elif any(keyword in user_message_lower for keyword in ['code', 'program', 'script', 'python', 'javascript', 'app']):
        response_data = {
            "content": "I'll help you with coding! I can write, debug, and optimize code in various programming languages. Let me analyze your requirements and create the solution you need.",
            "task": "Code development and programming",
            "tools": ["code", "terminal", "file"]
        }
    elif any(keyword in user_message_lower for keyword in ['file', 'document', 'edit', 'write', 'text']):
        response_data = {
            "content": "I'll help you work with files and documents. I can create, edit, organize, and manage various types of files. Let me handle the file operations for you.",
            "task": "File management and document editing",
            "tools": ["file", "terminal"]
        }
    elif any(keyword in user_message_lower for keyword in ['data', 'analyze', 'chart', 'graph', 'database', 'csv', 'excel']):
        response_data = {
            "content": "I'll help you analyze data and create visualizations! I can process datasets, generate insights, create charts and graphs, and help you understand your data better.",
            "task": "Data analysis and visualization",
            "tools": ["database", "code", "image"]
        }
    elif any(keyword in user_message_lower for keyword in ['image', 'picture', 'generate', 'create', 'photo', 'design']):
        response_data = {
            "content": "I'll help you work with images! I can generate new images, edit existing ones, create designs, and handle various image processing tasks.",
            "task": "Image generation and processing",
            "tools": ["image", "file"]
        }
    elif any(keyword in user_message_lower for keyword in ['search', 'find', 'lookup', 'research', 'information']):
        response_data = {
            "content": "I'll help you research and find information! I can browse the web, search for specific topics, gather data, and provide you with comprehensive research results.",
            "task": "Web research and information gathering",
            "tools": ["browser", "file"]
        }
    else:
        # General response
        response_data = {
            "content": "I understand your request! I'm a versatile AI agent that can help with web browsing, coding, file editing, data analysis, image generation, and much more. Let me work on this task for you.",
            "task": "Processing your request using available tools",
            "tools": ["terminal", "code", "file"]
        }
    
    processing_time = time.time() - start_time
    
    # Create and save the assistant message
    assistant_message = Message(
        conversation_id=conversation_id,
        message_type='assistant',
        content=response_data["content"],
        task_description=response_data["task"],
        tools_used=response_data["tools"],
        processing_time=processing_time
    )
    
    db.session.add(assistant_message)
    db.session.commit()
    
    return assistant_message

@chat_bp.route('/chat', methods=['POST'])
@cross_origin()
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get session information
        session_id = get_or_create_session()
        user_agent = request.headers.get('User-Agent')
        ip_address = request.remote_addr
        
        # Get or create agent session
        agent_session = get_or_create_agent_session(session_id, user_agent, ip_address)
        
        # Get or create conversation for this session
        conversation = Conversation.query.filter_by(session_id=session_id).order_by(Conversation.updated_at.desc()).first()
        
        if not conversation:
            # Create new conversation
            conversation = Conversation(
                session_id=session_id,
                title=user_message[:50] + "..." if len(user_message) > 50 else user_message
            )
            db.session.add(conversation)
            db.session.commit()
            agent_session.total_conversations += 1
        
        # Save user message
        user_msg = Message(
            conversation_id=conversation.id,
            message_type='user',
            content=user_message
        )
        db.session.add(user_msg)
        db.session.commit()
        
        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        agent_session.total_messages += 1
        db.session.commit()
        
        # Simulate processing time (1-3 seconds)
        time.sleep(random.uniform(1, 2))
        
        # Generate agent response
        assistant_message = generate_agent_response(user_message, conversation.id)
        agent_session.total_messages += 1
        db.session.commit()
        
        return jsonify({
            'response': assistant_message.content,
            'task': assistant_message.task_description,
            'tools': assistant_message.tools_used,
            'conversation_id': conversation.id,
            'message_id': assistant_message.id,
            'processing_time': assistant_message.processing_time
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@chat_bp.route('/conversations', methods=['GET'])
@cross_origin()
def get_conversations():
    """Get all conversations for the current session"""
    try:
        session_id = get_or_create_session()
        conversations = Conversation.query.filter_by(session_id=session_id).order_by(Conversation.updated_at.desc()).all()
        
        return jsonify({
            'conversations': [conv.to_dict() for conv in conversations]
        })
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@chat_bp.route('/conversations/<int:conversation_id>/messages', methods=['GET'])
@cross_origin()
def get_conversation_messages(conversation_id):
    """Get all messages for a specific conversation"""
    try:
        session_id = get_or_create_session()
        conversation = Conversation.query.filter_by(id=conversation_id, session_id=session_id).first()
        
        if not conversation:
            return jsonify({'error': 'Conversation not found'}), 404
        
        messages = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.timestamp.asc()).all()
        
        return jsonify({
            'conversation': conversation.to_dict(),
            'messages': [msg.to_dict() for msg in messages]
        })
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@chat_bp.route('/status', methods=['GET'])
@cross_origin()
def status():
    return jsonify({
        'status': 'online',
        'message': 'OpenManus API is running',
        'version': '1.0.0',
        'database': 'SQLite',
        'features': ['chat', 'conversations', 'persistent_storage']
    })


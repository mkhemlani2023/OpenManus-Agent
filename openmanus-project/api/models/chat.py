from datetime import datetime
from src.models.user import db

class Conversation(db.Model):
    """Model for chat conversations"""
    __tablename__ = 'conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), nullable=False, index=True)
    title = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to messages
    messages = db.relationship('Message', backref='conversation', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'title': self.title,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'message_count': len(self.messages)
        }

class Message(db.Model):
    """Model for individual chat messages"""
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    message_type = db.Column(db.String(20), nullable=False)  # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Additional fields for assistant messages
    task_description = db.Column(db.String(1000), nullable=True)
    tools_used = db.Column(db.JSON, nullable=True)  # Store as JSON array
    processing_time = db.Column(db.Float, nullable=True)  # Time taken to process
    
    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'type': self.message_type,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'task': self.task_description,
            'tools': self.tools_used or [],
            'processing_time': self.processing_time
        }

class AgentSession(db.Model):
    """Model for tracking agent sessions and capabilities"""
    __tablename__ = 'agent_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), nullable=False, unique=True, index=True)
    user_agent = db.Column(db.String(500), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Session statistics
    total_messages = db.Column(db.Integer, default=0)
    total_conversations = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'created_at': self.created_at.isoformat(),
            'last_active': self.last_active.isoformat(),
            'total_messages': self.total_messages,
            'total_conversations': self.total_conversations
        }


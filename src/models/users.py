from ..utils.utils import db
from flask_login import UserMixin
from .Timestamp import TimestampMixin
from decouple import config
import uuid
from sqlalchemy.dialects.postgresql import UUID


class User(UserMixin, TimestampMixin ,db.Model):
    """User model"""

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    user_code = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    user_name = db.Column(db.String(150), nullable = False)
    user_email = db.Column(db.String(120), unique=True, nullable = False)
    password = db.Column(db.Text, nullable = False)
    phone_number = db.Column(db.String(100), unique=True, nullable = False)
    agent_code = db.Column(db.String(150), nullable = True)
    is_active = db.Column(db.Boolean, default=True)
    is_agent = db.Column(db.Boolean, default=False)
    messages_sent = db.Column(db.Integer, default=0)
    messeges_allocated = db.Column(db.Integer, default=0)
    messages = db.relationship('Message', backref='user', lazy=True)
    
   

   
    
    def __repr__(self):
        return 'User %r' % self.agent_name

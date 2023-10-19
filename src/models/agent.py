from ..utils.utils import db
from flask_login import UserMixin
from .Timestamp import TimestampMixin
from decouple import config
import uuid
from sqlalchemy.dialects.postgresql import UUID


class Agent(UserMixin, TimestampMixin ,db.Model):
    """Agent model"""

    __tablename__ = 'agent'
    id = db.Column(db.Integer, primary_key = True)
    agent_code = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    agent_name = db.Column(db.String(150), nullable = False)
    is_active = db.Column(db.Boolean, default=True)
    messages = db.relationship('Message', backref='agent', lazy=True)
    
   

   
    
    def __repr__(self):
        return 'Agent %r' % self.agent_name

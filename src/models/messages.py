from re import U
from ..utils.utils import db
from flask_login import UserMixin
from .Timestamp import TimestampMixin
from decouple import config
import uuid
from sqlalchemy.dialects.postgresql import UUID


class Message(UserMixin, TimestampMixin ,db.Model):
    """Message model"""

    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key = True)
    text_query = db.Column(db.Text)
    text_reply = db.Column(db.Text)
    priority = db.Column(db.Integer)
    status = db.Column(db.String(100), default='Pending')
    agent_code = db.Column(UUID(as_uuid=True), default=None)
    agent_id = db.Column(db.Integer)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
   
    
    def __repr__(self):
        return 'Message %r' % self.id

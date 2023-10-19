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
    message_code = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    text = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'))

   
    
    def __repr__(self):
        return 'Message %r' % self.id

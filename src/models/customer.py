from ..utils.utils import db
from flask_login import UserMixin
from .Timestamp import TimestampMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from decouple import config
import uuid
from sqlalchemy.dialects.postgresql import UUID


class Customer(UserMixin, TimestampMixin ,db.Model):
   """Customer model"""

   __tablename__ = 'customer'
   id = db.Column(db.Integer, primary_key = True)
   customer_code = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
   username = db.Column(db.String(150), nullable = False)
   email = db.Column(db.String(120), unique=True, nullable = False)
   phone_number = db.Column(db.String(100), unique=True, nullable = True)
   password = db.Column(db.Text, nullable = True)
   active = db.Column(db.Boolean, default=True)
   messages = db.relationship('Message', backref='customer', lazy=True)
   
   def __repr__(self):
      return 'Customer %r' % self.username
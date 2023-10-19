from datetime import datetime
from ..utils.utils import db

class TimestampMixin(object):
    created_at = db.Column(db.DateTime(timezone = True), nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone = True), onupdate=datetime.utcnow)
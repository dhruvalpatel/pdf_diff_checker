from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class PDFMetadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(120))
    status = db.Column(db.String(120), default="Pending")
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    result_time = db.Column(db.DateTime)

    def __repr__(self):
        return f"<PDF {self.filename}>"

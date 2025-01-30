from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ScrapedData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    diff = db.Column(db.Text, nullable=True)  # New column to store differences
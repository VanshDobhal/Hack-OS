from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    alias = db.Column(db.String(64), default="Hacker")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to GameProgress
    progress = db.relationship('GameProgress', backref='user', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<User {self.username}>'


class GameProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    current_level = db.Column(db.Integer, default=1)
    completed_levels = db.Column(db.String(256), default="")  # Store as comma-separated list of level IDs
    current_directory = db.Column(db.String(128), default="/")
    last_played = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_completed_levels(self):
        """Convert the stored string of completed levels to a list of integers"""
        if not self.completed_levels:
            return []
        return [int(level) for level in self.completed_levels.split(',')]
    
    def set_completed_levels(self, levels):
        """Convert a list of level IDs to a comma-separated string for storage"""
        self.completed_levels = ','.join(str(level) for level in levels)
    
    def add_completed_level(self, level_id):
        """Add a level ID to the completed levels list"""
        levels = self.get_completed_levels()
        if level_id not in levels:
            levels.append(level_id)
            self.set_completed_levels(levels)
    
    def __repr__(self):
        return f'<GameProgress user_id={self.user_id} level={self.current_level}>'


class HighScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    level = db.Column(db.Integer, nullable=False)  # The level this score is for
    score = db.Column(db.Integer, default=0)
    completion_time = db.Column(db.Integer)  # Time in seconds
    date_achieved = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to User
    user = db.relationship('User', backref=db.backref('high_scores', lazy=True))
    
    def __repr__(self):
        return f'<HighScore user_id={self.user_id} level={self.level} score={self.score}>'
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
import os

db = SQLAlchemy()

class Terms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(100), unique=True, nullable=False)
    definition = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    
    # Simplified index that works across SQLite/PostgreSQL
    __table_args__ = (
        db.Index('ix_term', 'term'),
    )

def init_db(app):
    db.init_app(app)
    
    with app.app_context():
        try:
            # Create extension for PostgreSQL (Render)
            if 'postgresql' in app.config['SQLALCHEMY_DATABASE_URI']:
                db.session.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm')
            
            db.create_all()
            
            # Only seed if empty
            if not Terms.query.first():
                sample_terms = [
                    {"term": "code", "definition": " the block instruction ", "category": "General"},
                    
                ]
                for data in sample_terms:
                    if not Terms.query.filter_by(term=data['term']).first():
                        db.session.add(Terms(**data))
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Database initialization failed: {str(e)}")
            raise
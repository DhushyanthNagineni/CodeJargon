from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Terms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(100), unique=True, nullable=False)
    definition = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    
    # Simplified index for cross-database compatibility
    __table_args__ = (
        db.Index('ix_term', 'term'),
    )

def init_app(app):
    db.init_app(app)
    with app.app_context():
        # For Render's PostgreSQL
        if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgresql'):
            db.session.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm')
        db.create_all()
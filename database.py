from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Terms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(100), unique=True, nullable=False)
    definition = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    
    __table_args__ = (
        db.Index('ix_term_search', 'term', postgresql_using='gin', postgresql_ops={'term': 'gin_trgm_ops'}),
    )

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        if not Terms.query.first():
            sample_terms = [
            ]
            for data in sample_terms:
                db.session.add(Terms(**data))
            db.session.commit()
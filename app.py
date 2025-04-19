from flask import Flask, render_template, request
from database import db, Terms, init_db
from random import sample
from sqlalchemy import or_
import os

app = Flask(__name__)

# ======================
# 1. Configure database URI for Render's ephemeral storage
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///terms.db').replace(
    'postgres://', 'postgresql://')  # Fix for Render's PostgreSQL

# 2. Disable tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3. Required for session security
app.secret_key = os.environ.get('SECRET_KEY', 'dev-fallback-key') 

# Initialize database
init_db(app)

@app.route("/")
def home():
    search_query = request.args.get('q', '').strip()
    
    if search_query:
        terms = Terms.query.filter(
            or_(
                Terms.term.ilike(f'%{search_query}%'),
                Terms.definition.ilike(f'%{search_query}%')
            )
        ).all()
    else:
        all_terms = Terms.query.all()
        terms = sample(all_terms, min(6, len(all_terms))) if all_terms else []
    
    return render_template("index.html", 
                         terms=terms,
                         search_query=search_query,
                         results_count=len(terms))


# ======================
if __name__ == '__main__':
    # 4. Create tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # 5. Run with Render-compatible settings
    app.run(host='0.0.0.0', 
            port=int(os.environ.get('PORT', 5000)), 
            debug=os.environ.get('FLASK_DEBUG', False))
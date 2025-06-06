from flask import Flask, render_template, request
from database import db, Terms, init_app
from random import sample
from sqlalchemy import or_
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///terms.db').replace('postgres://', 'postgresql://')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY', 'dev-fallback-key')

# Initialize database
init_app(app)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
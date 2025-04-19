from flask import Flask, render_template, request
from database import db, Terms, init_db
from random import sample
from sqlalchemy import or_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///terms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)

@app.route("/")
def home():
    search_query = request.args.get('q', '').strip()
    
    if search_query:
        # Search in both term names and definitions
        terms = Terms.query.filter(
            or_(
                Terms.term.ilike(f'%{search_query}%'),
                Terms.definition.ilike(f'%{search_query}%')
            )
        ).all()
    else:
        # Get 6 random terms
        all_terms = Terms.query.all()
        terms = sample(all_terms, min(6, len(all_terms))) if all_terms else []
    
    return render_template("index.html", 
                         terms=terms,
                         search_query=search_query,
                         results_count=len(terms))

if __name__ == "__main__":
    app.run(debug=True)
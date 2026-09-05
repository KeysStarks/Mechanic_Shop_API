from application import create_app
from application.extensions import db
from config import ProductionConfig

app = create_app(ProductionConfig)

@app.route("/")
def index():
    return "Mechanic Shop API is running. Visit /api/docs. for documentation."

with app.app_context():
    db.create_all()
    
if __name__ == '__main__':
    app.run(debug=True)
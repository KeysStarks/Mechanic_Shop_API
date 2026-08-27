from application import create_app
from application.extensions import db
from config import Config

app = create_app(Config)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
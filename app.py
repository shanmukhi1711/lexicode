import os
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config
from models import db, User

csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['REPORTS_FOLDER'], exist_ok=True)

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from routes.auth import auth_bp
    from routes.main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        # Seed demo user
        demo = User.query.filter_by(email="demo@lexicode.com").first()
        if not demo:
            demo = User(email="demo@lexicode.com")
            demo.set_password("Demo@1234")
            db.session.add(demo)
            
            from models import Document
            doc1 = Document(title="Science History", content="Gravity is a fundamental force of nature. Isaac Newton discovered gravity when an apple fell on his head.", user_id=None)
            doc2 = Document(title="Tech Overview", content="Artificial intelligence is transforming the world. Machine learning models can analyze large amounts of data.", user_id=None)
            db.session.add_all([doc1, doc2])
            
            db.session.commit()
            print("Demo user and reference docs seeded.")
    app.run(debug=True, port=5000)

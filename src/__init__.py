from .utils.utils import db, migrate, login_manager, moment, socketio
from flask import Flask, session, render_template
from .config.config import Config
from .auth.views import auth
from .main.views import main
from .models import (
    Agent,
    Customer,
    Message,
    User
)



def create_app(config = Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db, compare_type=True, render_as_batch=True)
    login_manager.init_app(app)
    moment.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
   
    
    
    
    #register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(main)
   
    
    # create database tables
    with app.app_context():
        db.create_all()
        
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = "danger"

    @login_manager.user_loader
    def load_user(id):
       return User.query.get(int(id))
   
    # @login_manager.user_loader
    # def load_user(user_id):
    #     global record
    #     if 'user_type' in session:
    #         if session["user_type"] == "user":
    #             record = Customer.query.get(int(id))
    #         if session["user_type"] == "worker":
    #             record = Agent.query.get(int(id))
    #         return record

  

    return app

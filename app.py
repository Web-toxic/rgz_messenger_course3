from flask import Flask, Blueprint, render_template, request, make_response, abort
from flask_sqlalchemy import SQLAlchemy
from Db import db
from Db import models
from Db.models import User
from flask_login import LoginManager
from RGZ import RGZ

app = Flask(__name__)
app.register_blueprint(RGZ)

app.secret_key = "7414"
user_db = "polina_knowledge_base_orm"
host_ip = "127.0.0.1"
host_port = "5432"
database_name = "polina_messenger"
password = "7414"

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user_db}:{password}@{host_ip}:{host_port}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

login_manager = LoginManager()

login_manager.login_view = "RGZ.login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    try:
        user = User.query.get(int(id))
    except:
        return None
    return user

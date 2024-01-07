from flask import Flask
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, render_template, request, redirect, session
from Db import db
from Db.models import User, Message
from flask_login import login_user, login_required, current_user

RGZ=Blueprint('RGZ',__name__)

# @RGZ.route('/')
# def index():
#     return render_template('index.html')


@RGZ.route('/')
def index():
    return "result in console!"
from flask import Flask
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, render_template, request, redirect, session, flash
from Db import db
from RGZ import db
from Db.models import User, Message
from flask_login import login_user, login_required, current_user

RGZ=Blueprint('RGZ',__name__)

@RGZ.route('/')
def index():
    return render_template('index.html')


@RGZ.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        if User.query.filter_by(login=login).first():
            flash('Этот логин уже занят.')
            return render_template('register.html')

        user = User(login=login, password=password)
        db.session.add(user)
        db.session.commit()

        flash('Вы успешно зарегистрировались.')
        return redirect('/')
    

@RGZ.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        user = User.query.filter_by(login=login).first()

        if user is None or not user.check_password(password):
            flash('Неверный логин или пароль.')
            return render_template('login.html')

        session['user_id'] = user.id
        return redirect('/')
    

@RGZ.route('/users', methods=['GET'])
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)


@RGZ.route('/messages/<int:user_id>', methods=['GET'])
@login_required
def messages(user_id):
    messages = Message.query.filter_by(receiver_id=user_id).all()
    return render_template('messages.html', messages=messages)


@RGZ.route('/messages/send', methods=['POST'])
@login_required
def send_message():
    receiver_id = request.form['receiver_id']
    text = request.form['text']

    if not receiver_id:
        flash('Необходимо указать id получателя.')
        return redirect('/messages')

    message = Message(sender_id=session['user_id'], receiver_id=receiver_id, text=text)
    db.session.add(message)
    db.session.commit()

    flash('Сообщение отправлено.')
    return redirect('/messages')


@RGZ.route('/messages/delete/<int:message_id>', methods=['POST'])
@login_required
def delete_message():
    message_id = request.form['message_id']

    message = Message.query.get(message_id)

    if message is None:
        flash('Сообщение не найдено.')
        return redirect('/messages')

    if message.sender_id != session['user_id'] and message.receiver_id != session['user_id']:
        flash('У вас нет прав на удаление этого сообщения.')
        return redirect('/messages')

    db.session.delete(message)
    db.session.commit()

    flash('Сообщение удалено.')
    return redirect('/messages')



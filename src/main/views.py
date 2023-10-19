from flask import (Blueprint, redirect, render_template, request, flash, url_for, jsonify, current_app, abort, Response,
                   send_file)
from sqlalchemy import or_, desc
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from ..utils.utils import db
# import logging
from flask_login import current_user
from datetime import datetime
import uuid
import math
from loguru import logger
from flask_login import login_user, logout_user, login_required, current_user


main = Blueprint('main', __name__)


@main.route('/')
def homepage():
    return redirect(url_for('auth.login'))

@main.route('/home')
def home():
    return render_template('home.html')

@main.route('/support_page')
def client_support_page():
    return render_template('customer_page.html')

@main.route('/agent_support_page')
def agent_support_page():
    return render_template('agent_page.html')

# @main.route('/send_message', methods=['POST'])
# def send_message():
#     text = request.form['message']
#     customer_id = 1
#     agent_id = 1
#     message = Message(text=text, customer_id=customer_id, agent_id=agent_id)
#     db.session.add(message)
#     db.session.commit()
    
#     # Emit the new message to all connected clients
#     send({'text': text, 'customer_id': customer_id, 'agent_id': agent_id}, broadcast=True)
    
#     return 'Message sent'
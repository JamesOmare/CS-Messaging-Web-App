from crypt import methods
from flask import (Blueprint, redirect, render_template, request, flash, url_for, jsonify, current_app, abort, Response,
                   send_file)
from sqlalchemy import or_, desc
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from ..utils.utils import db
from flask_login import current_user
from datetime import datetime
from .. models import(
    User,
    Message
)
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

@main.route('/support_page', methods=['GET', 'POST'])
@login_required
def client_support_page():
    user = current_user.id
    
    messages = Message.query.filter_by(
                        user_id=user,
                        ).order_by(desc(Message.created_at)).all()
    
    
    return render_template('customer_page.html', messages = messages)

@main.route('/agent_support_page')
@login_required
def agent_support_page():
    if not current_user.is_agent:
        abort(403)
    
    return render_template('agent_page.html')

@main.route('/send_message', methods=['POST'])
@login_required
def send_message():
    if request.method == "POST":
        comment = request.form['comment']
        selected_option = request.form['selected_option']
        user_id = request.form['user_id']
        
        if selected_option:
            message_priority = {
            "Loan Application" : 1,
            "Payment Enquiries": 2,
            "Interest Rate and Terms": 3,
            "Account and Personal Information Update": 4,
            }

            # Get the message priority based on the selected choice
            # If the selected choice is not in the dictionary, it defaults to 0"(Other)"
            priority = message_priority.get(selected_option, 0)
            
            # Create a new message instance and commit to the database
            new_message = Message(
                text_query = comment,
                user_id = user_id,
                priority = priority
            )        
            
            db.session.add(new_message)
            db.session.commit()
            
            flash('Message sent successfully', 'success')
            
            # function to Assign the saved message to the agent with the fewest assigned messages
            def assign_message_to_agent(new_message):
                # Query agents sorted by the number of assigned messages in ascending order
                agents = User.query.filter_by(is_agent=True).order_by(User.messages_allocated).all()

                if not agents:
                    # Handle the case when no agents are available
                    logger.critical("No agents available")
                    flash('No agents are available right now, Please wait for the team to come online', 'warning')
                    return redirect(url_for('main.client_support_page'))
                    

                # Assign the message to the agent with the fewest assigned messages
                agent_to_assign = agents[0]
                new_message.agent_code = agent_to_assign.user_code

                # Update the agent's assigned message count
                agent_to_assign.messages_allocated += 1  

                db.session.commit()
            
            
            # Assign the new message to an agent
            assign_message_to_agent(new_message)

            return redirect(url_for('main.client_support_page'))
        
        
        else:
            flash('You Have Not Selected Any Category Option, Please try again', 'danger')
            return redirect(url_for('main.client_support_page'))

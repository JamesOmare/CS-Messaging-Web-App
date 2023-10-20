from crypt import methods
from hmac import new
from flask import (Blueprint, redirect, render_template, request, flash, url_for, jsonify, current_app, abort, Response,
                   send_file)
from sqlalchemy import desc, asc
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
    
    # load latest user messeges
    messages = Message.query.filter_by(
                        client_id=user,
                        ).order_by(desc(Message.created_at)).all()
    
    
    return render_template('customer_page.html', messages = messages)

@main.route('/agent_support_page')
@login_required
def agent_support_page():
    if not current_user.is_agent:
        abort(403)
        
    page = request.args.get('page', 1, type=int)
    
    pending_messages = Message.query.filter_by(
                        agent_code=current_user.user_code, status="Pending"
                        ).order_by(desc(Message.created_at)
                        ).paginate(page=page, per_page=5, error_out=False)
    
    resolved_messages = Message.query.filter_by(
                        agent_code=current_user.user_code, status="Resolved"
                        ).order_by(desc(Message.created_at)
                        ).paginate(page=page, per_page=5, error_out=False)
    
    # Order by priority in ascending order(1..5)
    # # Order by created_at in descending order (latest first)
    # messages = Message.query.filter_by(
    #         agent_code=current_user.user_code
    #         ).order_by(
    #             asc(Message.priority),  
    #             desc(Message.created_at)
    #             ).all()
    messages = {
        'pending_messages': pending_messages,
        'resolved_messages': resolved_messages
        
    }
    
    return render_template('agent_page.html', **messages)

@main.route('/send_message', methods=['POST'])
@login_required
def send_message():
    if request.method == "POST":
        comment = request.form['comment']
        selected_option = request.form['selected_option']
        client_id = request.form['user_id']
        
        client = User.query.filter_by(id=client_id, is_agent = False).first()
        
        if not client:
            # Handle the case when client id is invalid
            logger.critical("Client Id is invalid.")
            flash('Client Credentials are invalid', 'warning')
            return redirect(url_for('main.client_support_page'))
        
        
        if selected_option:
            message_priority = {
            "Loan Application" : 1,
            "Payment Enquiries": 2,
            "Interest Rate and Terms": 3,
            "Account and Personal Information Update": 4,
            "General": 5,
            }

            # Get the message priority based on the selected choice
            priority = message_priority.get(selected_option)
            
            # Create a new message instance and commit to the database
            new_message = Message(
                text_query = comment,
                client_id = client_id,
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
                new_message.agent_id = agent_to_assign.id
                
                # update message sent count to the user
                client.messages_sent += 1

                # Update the agent's assigned message count
                agent_to_assign.messages_allocated += 1  

                db.session.commit()
            
            
            # Assign the new message to an agent
            assign_message_to_agent(new_message)

            return redirect(url_for('main.client_support_page'))
        
        
        else:
            flash('You Have Not Selected Any Category Option, Please try again', 'danger')
            return redirect(url_for('main.client_support_page'))
        
        
@main.route('/reply_to_message', methods=['POST'])
@login_required
def reply_to_message():
    if request.method == "POST":
        agent_id = request.form['agent_id']
        message_id = request.form['message_id']  
        text_reply = request.form['text_reply']
        
        
        message = Message.query.filter_by(id=message_id).first()
        agent = User.query.filter_by(id=agent_id, is_agent=True).first()
        
        if message and agent:
            # update message with the reply and status
            message.text_reply = text_reply
            message.status = "Resolved"
            
            # update agent with the resolved message count
            agent.messages_resolved += 1
            
            # save to database
            db.session.commit()
            
            
            return redirect(url_for('main.agent_support_page'))
        
        else:
            flash('Message or Agent not found', 'danger')
            return redirect(url_for('main.agent_support_page'))
            

    
        


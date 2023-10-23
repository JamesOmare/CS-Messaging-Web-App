from flask import Blueprint, current_app, redirect, render_template, request, flash, url_for, abort, session, jsonify
from ..utils.utils import db
from loguru import logger
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, render_template, url_for, redirect, session
from flask_login import login_user, logout_user, login_required, current_user
from .. models import(
    Message, User
)
import random

from faker import Faker
fake = Faker()

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        phone_number = request.form['phone_number']

        # check if email exists
        email_exists = User.query.filter_by(user_email=email).first()

        #check if phone number exists
        phone_number_exists = User.query.filter_by(phone_number=phone_number).first()

        if email_exists:
            flash('Email already exists, choose another one.', 'primary')
        
        elif phone_number_exists:
            flash('The phone number provided already exists. Please enter another one!', 'primary')

        else:
            
            try:
                
                new_user = User(
                    user_name = username,
                    password = generate_password_hash(password, method='scrypt'),
                    user_email = email,
                    phone_number = phone_number,
                    )
                db.session.add(new_user)
                db.session.commit()
                
            except Exception as e:
                db.session.rollback()
                logger.critical(f'Failed to save new user instance to database: ', e)
                flash('Failed to save user data, Please Try Again. If issue persists Contact The Support Team', 'danger')
                return render_template('signup.html', **locals())
                        
            else:
                login_user(new_user, remember=True)
                flash('User created, you can log in with the registered credentials', 'success')
                

                return redirect(url_for('main.home'))

    
    return render_template('signup.html', **locals())

    
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Login successful', 'success')
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # check if user exists
        user = User.query.filter_by(user_email=email).first()

        if user:

            if user.is_active:
                if check_password_hash(user.password, password):
                    login_user(user, remember=True)
                    flash('Logged in Successfully!', 'success')
                    return redirect(url_for('main.home'))
                else:
                    flash('Username or Password is incorrect!', 'danger')

            elif not user.is_active:
                flash("Your personal account has been suspended for violating our terms of service. You can check your email for further information or call our support team.", "danger")
        
        else:
    
            flash('Username or Password is incorrect!', 'danger')

    return render_template('login.html', **locals())


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route("/generate_users_and_messages")
def generate_users_and_messages():
    fake_users = []
    try:
        for _ in range(40):
            username = fake.user_name()
            email = fake.email()
            phone_number = fake.random_int(min=7000000000, max=7999999999)
            # 'password' is the same for all users
            password = 'password'
            
            new_user = User(
                user_name=username,
                password=generate_password_hash(password, method='scrypt'),
                user_email=email,
                phone_number=f'07{phone_number:08}',  # Format phone number
            )
            db.session.add(new_user)
            fake_users.append(new_user)

        db.session.commit()
        
        
    except Exception as e:
        return {
            "message": "failed",
            "data": f"Failed to generate test users: {e}"
        }, 500
        
    else:
        
        try:
            for user in fake_users:
                # Generate 1 to 5 messages per user
                for _ in range(fake.random_int(min=1, max=5)): 
                    
                     # Adjust max_characters as needed
                    comment = fake.text(max_nb_chars=200) 
                    client_id = user.id
                    
                    # Generates random priority (1-5)
                    priority = fake.random_int(min=1, max=5)  

                    new_message = Message(
                        text_query=comment,
                        client_id=client_id,
                        priority=priority
                    )
                    db.session.add(new_message)
                    
                    # function to Assign the saved message to the agent with the fewest assigned messages
                    def assign_message_to_agent(new_message):
                        # Query agents sorted by the number of assigned messages in ascending order
                        agents = User.query.filter_by(is_agent=True).order_by(User.messages_allocated).all()

                            
                        # Assign the message to the agent with the fewest assigned messages
                        agent_to_assign = agents[0]
                        new_message.agent_code = agent_to_assign.user_code
                        new_message.agent_id = agent_to_assign.id
                        
                        # update message sent count to the user
                        user.messages_sent += 1

                        # Update the agent's assigned message count
                        agent_to_assign.messages_allocated += 1

                    # Assign the new message to an agent
                    assign_message_to_agent(new_message)

            db.session.commit()
            
        except Exception as e:
            return {
                "message": "failed",
                "data": f"Failed to generate test messages: {e}"
            }, 500
            
        else:
            return {
                "message": "successfully created test users and messages",
            }, 200
            

@auth.route("/generate_users")
def generate_users():
    fake_users = []
    try:
        for _ in range(55):
            username = fake.user_name()
            email = f"{fake.user_name()}@gmail.com"
            # Ensure email ends with @gmail.com
            if not email.endswith('@gmail.com'):
                email += '@gmail.com'
            phone_number = fake.random_int(min=70000000, max=79999999)
            # 'password' is the same for all users
            password = 'password'
            
            new_user = User(
                user_name=username,
                password=generate_password_hash(password, method='scrypt'),
                user_email=email,
                phone_number=f'07{phone_number:08}',  # Format phone number
            )
            db.session.add(new_user)
            fake_users.append(new_user)

        db.session.commit()
        
        
    except Exception as e:
        return {
            "message": "failed",
            "data": f"Failed to generate test users: {e}"
        }, 500
        
    else:
        return {
            "message": "successfully created test users and messages",
        }, 200
            

@auth.route('/get_message_api')
def get_message_api():
    
            texts = [
            "So it means if u pay ua loan before the due date is a disadvantage the last time I paid earlier it was still a problem",
            "The dates of payment are still indicated n no money sent",
            "Why was my application rejected",
            "Hi branch I requested my number to remain the one I was using there before 0720225243  I don't understand how it changed",
            "I said ill pay 5th esther camoon.. Infact you guys took a week to give me a loan and just cant wait 4days for me to pay back??",
            "I  will pay on sunday of 5th and i will pay all the amount.. If that is allowed??",
            "I have a late source of salary i expected but i will pay nexr",
            "I will clear my loan before 15nth,kindly bear with me.January was tough.",
            "Hi can i get the batch number",
            "Hi can i get the batch number pl",
            "I Still not satisfied. I am still asking for a review.  My number is 0723506931 or at least give me a clear reason.  Thanks",
            "My number is 0723506931. please have a review of my loan. I haven't defaulted and I have cleared my outstanding loan on the due date.",
            "Hi branch I have just cleared my  loan which was due today but unfortunately you have denied me. I haven't applied for a loan since December but your system says that I have applied for a loan last week. Please review my loan",
            "I got only this number please help me",
            "My number is 0790898526 help me to validate it please so i can be able to access the loan",
            "Hello,our salaries have been delayed but hopefully will be paid today or tomorrow.",
            "Thanks Branch for being understanding ..have cleared my loan....God bless you",
            "Hi, kindly can i have the batch number",
            "I have to clear by tomorrow please send me the batch number",
            "I was at CRB offices and they haven't received your clearance batch number. Please send it to me so I can clear with them.",
            "No need just expunge my details from the system",
            "Thank you for the loans I have benefitted from 'the branch'. Kindly expunge my details from your system. It's frustrating to be told to reapply in 7 days week in and week out....it makes me look like a criminal. I will not be applying again.",
            "My loan has been rejected because it was rejected recently, after 14 days suspension I am being suspended again for a further 7 days",
            "Hello. Why can't you make the loan payment options more... like say a choice between weekly and monthly.. someone to choose when applying for the loans..  regards",
            "Hi, sorry for the short text however someone used my I.D and did register a line and took mshwari loan but venye nili realize nilipigia safaricom customer care and I did the payment and cleared a bill of 299 now I don't have  any. What is the way forward.",
            "Any response to my above queries please???",
            "Kindly advise what SMS are not in my phone....",
            "And I have no current loan... I'm up to date...",
            "If there is a way you can check the M-Pesa SMS in my phone... Check and see all transactions SMS are available... and M-Pesa account is very active",
            "All my M-Pesa SMS are stored in the SIM card for a long period... and none has been deleted...",
            "What SMS should I accumulate on my phone?",
            "Why has my loan application been rejected and I have never defaulted on any repayments and I always pay on time?",
            "Why has loan been rejected?",
            "Ok",
            "Hi, sorry for the short text however someone used my I.D and did register a line and took mshwari loan but venye nili realize nilipigia safaricom customer care and I did the payment and cleared a bill of 299 now I don't have any. What is the way forward.",
            "Someone used",
            "What am I supposed to do after paying in order to re",
            "Another 7 days what! For the third time now.",
            "Hey Branch, I am sorry for being late in payment but I will pay on Monday 6/2/2017 but the reason for late repayment is due to maturing of a check because it was signed late but I apologize and hope it will never happen again.",
            "I'll pay the 32/= together with Monday's 566/=",
            "I appreciate for the follow-up you made, thanks a lot",
            "How long does it take for me to get the batch number because I cleared my loan on 31st?",
            "Within a week, specifically when please?",
            "72 hrs",
            "Hope the clearance lasts for 72 hours",
            "This is Keynan, did you share my details with CRB?",
            "Can I get batch number please",
            "Can I have direct contact thus I keep in touch with the concerned authorities",
            "I'm still getting from other financial institutions that I owe Branch 1068 and I have already paid that amount",
            "This is Keynan, can you kindly forward my details to CRB? I've got stuck somewhere",
            "Sorry for that but I am still searching for the money but will be paying the loan soon as the deadline I had set passed but I am doing all I can to settle the loan",
            "Alright. Thanks.",
            "Do I have any other loan that I didn't pay",
            "Why don't you want to give me a loan",
            "Sorry for the delay, I blocked my M-Pesa PIN but now it's okay, I will pay by the end of today",
            "Hi Branch, why do I have the text that my payment is late while it's due today? 3rd Feb 2017",
            "Thanks for understanding my situation. I look forward to settling my loans on the time I have promised",
            "I'm expecting to clear by date 8/2/2017",
            "I've settled many of your loans before. Please don't spoil my credit report",
            "Hi Branch, had missed this",
            "Am sorry nilichelewa kulipa loan. Guys siyo kawaida yangu kuchelewesha lakini ni accident nlioata na mtoto wangu akachomeka na maji moto, naomba msamaha mwanzo mmeniinua sana kibiashara na ni ombi langu mtaendelea kunikopesha loan na tena ningeomba tafadhali don't lower loan limit please. Will pay my loan on Friday, good day",
            "When am I qualified to get another loan",
            "Hi! Account details are correct. Have not received the loan yet...",
            "I require a feedback please",
            "Did sent the C Certificate",
            "Are you guys going to punish me forever?",
            "Meanings",
            "I cleared last year for how long",
            "Hi Branch, I am among your best beneficiaries of the Tala platform. However, I have hit a 'dead-end' situation on my payment which is late for almost 5 weeks after I took the loan. It has been caused by a temporal stagnation from my employment that was abruptly halted due to funding issues. Need to request for a little extra time as I commit myself to clear this loan I have. Kindly respond so we can agree on an amicable plan for payment. My Tel: 0723 496 592. Waiting for your feedback. Regards, Kenedy Sifuma",
            "It can't be 1264. I had paid 400 earlier. Please update your systems and give the right balance",
            "Hi Branch, Yes, I have a problem which I thought it could have been resolved by now but it's not. I have not been paid yet but kindly allow me to pay by next week, please",
            "I am sending the full amount today, just got busy",
            "Some lady from Branch calls me and starts to abuse me just because I said I've paid a total of 1000 which she claims from her side I've paid only 600. My loan is 18394 and yet it shows here clearly it's 17994. My question is, is this how people who have defaulted are addressed? Because surely I've started paying. And I've introduced people who are paying, so why look down on others",
            "Hi, I have paid my loan on time but my loan has been rejected. Why has it been rejected?",
            "Can't login",
            "The weekly text reminders are a nuisance",
            "The weekly text reminders",
            "Hi, please I can pay my loan in a month once. Adjust your payment schedule and give options whether to pay weekly or monthly",
            "OK, I have paid all of it",
            "Why can't I have a loan now yet I have cleared my previous loan",
            "How do I get a loan",
            "Dear Branch, sorry for the late payment of my loan. This is due to unavoidable circumstances but I strive to clear the loan before Wednesday 8th Feb next week",
            "Hi Branch, by 7th I promise to make some payment to reduce my loan",
            "So, in short, because I don't have the SMS that's the reason",
            "Why was my loan request rejected and I have been paying on time",
            "Dear Branch, I am experiencing difficulty in payments but will deposit tomorrow evening. Thank you",
            "Hi, what's the 7 more days penalty for? Be frank and specify. I paid the previous loan on time",
            "I have been trying this app for a long period. When I apply, I'm told to try again after 7 days. It has become a song. Is this app real or am I wasting my time and bundles for nothing?",
            "Will pay before 15th",
            "I have been with you for a long time and I made a mistake but I won't repeat it again. I was having an illness",
            "Sorry, I meant December 2016",
            "Hi Branch, now my application was rejected recently on 1st Feb 2017. I had borrowed Sh.25,000 in December 2015 of which I was slightly late in paying but I paid the whole loan today only to be disappointed when I apply for another. It says I reapply again in 7 days, which is too long for me at the moment because I desperately need the cash. How can you assist?"
        ]
    
        # Simulate API requests for users with client_id from 10 to 55
        

            # function to Assign the saved message to the agent with the fewest assigned messages
            def assign_message_to_agent(new_message):
                # Query agents sorted by the number of assigned messages in ascending order
                agents = User.query.filter_by(is_agent=True).order_by(User.messages_allocated).all()

                if not agents:
                    # Handle the case when no agents are available
                    logger.critical("No agents available")
                    return jsonify({"message": "No Agents Available."}), 400
                    


                # Assign the message to the agent with the fewest assigned messages
                agent_to_assign = agents[0]
                new_message.agent_id = agent_to_assign.id
                
                # update message sent count to the user
                client.messages_sent += 1

                # Update the agent's assigned message count
                agent_to_assign.messages_allocated += 1  

                db.session.commit()
                
        
            for client_id in range(10, 56):
                # Generate a random selected_option from 1 to 5
                selected_option = random.randint(1, 5)

            
                # Generate a random selected_option from 1 to 5
                selected_option = random.randint(1, 5)
                print(selected_option)
                # Select a random comment
                comment = random.choice(texts)
                
             
            
                # Find the client by client_id
                client = User.query.filter_by(id=client_id, is_agent=False).first()

                if not client:
                    # Handle the case when client_id is invalid
                    logger.critical("Client Id is invalid.")
                    return jsonify({"message": "Client Id is invalid."}), 400
                

                # Create a new message instance and commit it to the database
                message_priority = {
                    1: "Loan Application",
                    2: "Payment Enquiries",
                    3: "Interest Rate and Terms",
                    4: "Account and Personal Information Update",
                    5: "General",
                }

                priority = message_priority[selected_option]

                new_message = Message(
                    text_query=comment,
                    client_id=client_id,
                    priority=priority
                )

                db.session.add(new_message)
                
                
                # Assign the new message to an agent
                assign_message_to_agent(new_message)


            db.session.commit()
            
            return jsonify({
                "message": "Message added successfully."
                }), 200

            
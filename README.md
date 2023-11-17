# CS-Messaging-Web-App
A messaging web application that can be used to respond to incoming questions sent by  clients
# CS-Messaging-Web-App Application Setup Guide

Welcome to the CS-Messaging-Web-App application! This application is a demo illustration offering world-class customer service through an in-app chat.
This project address the challenge of handling a high volume of customer inquiries while flagging the most urgent issues. This guide will help you set up your development environment and run the application.

## Prerequisites

Before you begin, make sure you have the following installed on your system:

- Python 3.6 or higher
- pip (Python package manager)
- Virtual environment (optional but recommended)

## Getting Started

1. **Clone the Repository:**

- On terminal:

  ```
  git clone https://github.com/JamesOmare/CS-Messaging-Web-App.git
   cd CS-Messaging-Web-App
  ```



2. **Create a Virtual Environment (Optional):**

It's a good practice to create a virtual environment for your project to isolate dependencies. To create a virtual environment, run the following command:

- On macOS and Linux:

  ```
  python3 -m venv venv or python -m venv venv
  ```
  
Activate the virtual environment:

- On Windows:

  ```
  venv\Scripts\activate
  ```

- On macOS and Linux:

  ```
  source venv/bin/activate
  ```

3. **Install Dependencies:**

Install the required Python packages i.e Flask using pip and install the packages present in the requirements file located at the root directory:

- On terminal:

  ```
  pip install -r requirements.txt
  ```



4. **Configure Environment Variables:**

The application uses environment variables (e.g., for database connection), create a `.env` file in the root directory and add the following variables:

- In .env file:

  ```
  FLASK_APP = runserver.py
  FLASK_DEBUG = True
  SECRET_KEY = "enter a random varibale(even leaving this here can work)"
  POSTGRES_DATABASE_URL = "postgresql://<username>:<password>@localhost:5432/<database_name>"
  SQLITE_DATABASE_URL = "sqlite:///cs_messaging.db"
  DEBUG = True
  ```


5. **Database Setup:**



#### Alternative 1 - SQLITE
In the application root folder, there is an instance folder which has the sqlite database. This database contains user and messaging data(the one shared in the csv file). This is the default database i've used and will not require any additional set up once the app starts.

- All users have a password `password`.
 - There are 5 agents with the credentials agent1@gmail.com ... agent5@gmail.com 


#### Alternative 2 - POSTGRES
If your want to use postgres for any reason i.e the sqlite database did not work, you can follow the following instructions:

- Create a postgres database
- In the .env file, there is a the POSTGRES_DATABASE_URL key where you can add your configurations there
- In the src folder(root directory), go to the config folder. Go to config.py and uncomment SQLALCHEMY_DATABASE_URI that points to POSTGRES_DATABASE_URL and comment out the one that points to SQLALCHEMY_DATABASE_URI.
- You can either manually create users(fist run the application) by registering users in the register UI. After creating the users, you can go to the db and manually add agents by making the "is_agent" field in the users to be True.
- Alternatively, if you don't want to manaully create users and messages, In the src folder(root directory), go to the auth folder and go to views.py.
 Here, there are three flask function views that are located at the bottom of the file,generate_users_and_messages, generate_users and generate_messages. 
- To create a list of random users (all their passwords are "password"), first run the application, then go to postman or any similar software and run a GET request to the endpoint "http://127.0.0.1:5007/generate_users". This will create 50 random users with siilar passwords("password"). You can then manually add agents by changing the field "is_agent" to True.
- After creating users and adding agents(changing the is_agent field to True), you can then add messages by first updating the code in line 354 in the file `src/auth/views.py` to the following:
        users = User.query.filter(User.id >= (number of agents added preferrably in their id order i.e id 1-5 are agents so your clients start from id 6, so you'll input the int 6), User.id <= 50, User.is_agent == False).all()
- Then make a GET request to the endpoint "http://127.0.0.1:5007generate_messages". This will fill 100 messages shared from the csv file you shared to random client between the id specified to id 50. It will also assign each message to an agent systematically i.e agent 1 will have 20 messages, agent 2 will have 20 messages and so on.


6. **Run the Application:**

(The Database Setup connection has to be already made up before this point)Run the Flask development server:


  ```
  python3 runserver.py  or python runserver.py  
  ```


Your Flask application should now be running. Access it in your web browser at `http://localhost:5007`.


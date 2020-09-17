from typing import Optional

from fastapi import FastAPI
import connection
from bson import ObjectId
from schematics.models import Model
from schematics.types import StringType, EmailType


class User(Model):
    user_id = ObjectId()
    email = EmailType(required=True)
    name = StringType(required=True)
    password = StringType(required=True)

# An instance of class User
newuser = User()

# funtion to create and assign values to the instanse of class User created
def create_user(email, username, password):
    newuser.user_id = ObjectId()
    newuser.email = email
    newuser.name = username
    newuser.password = password
    return dict(newuser)

def email_exists(email):
    user_exist = True
    if connection.db.users.find(
        {'email': email}
    ).count() == 0:
        user_exist = False
        return user_exist

def check_login_creds(email, password):
    if email_exists(email):
        activeuser = connection.db.users.find(
            {'email': email}
        )
        activeuser = dict(activeuser)
        print(activeuser)
        return activeuser
    else:
        return "Invalid Email"


app = FastAPI()


# Our root endpoint
@app.get("/")
def index():
    return {"message": "Hello World"}

# Signup endpoint with the POST method
@app.post("/signup/{email}/{username}/{password}")
def signup(email, username: str, password: str):
    user_exists = False
    data = create_user(email, username, password)

    # Covert data to dict so it can be easily inserted to MongoDB
    dict(data)

    # Checks if an email exists from the collection of users
    if connection.db.users.find(
        {'email': data['email']}
        ).count() > 0:
        user_exists = True
        print("USer Exists")
        return {"message":"User Exists"}
    # If the email doesn't exist, create the user
    elif user_exists == False:
        connection.db.users.insert_one(data)
        return {"message":"User Created","email": data['email'], "name": data['name'], "pass": data['password']}

# Login endpoint
@app.get("/login/{email}/{password}")
def login(email, password):
    def log_user_in(creds):
        if creds['email'] == email and creds['password'] == password:
            return {"message": creds['name'] + 'successfully logged in'}
        else:
            return {"message":"Invalid credentials!!"}
    # Read email from database to validate if user exists and checks if password matches
    logger = check_login_creds(email, password)
    print(logger)
    if bool(logger) == True:
        return {"message":logger}
    else:
        status = log_user_in(logger)
        return {"Info":status}
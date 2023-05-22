from database import Database
from models import User

database = Database()
session = database.session

def create_user(username, password):
    user = User(username=username, password=password)
    session.add(user)
    session.commit()

def get_user(username):
    return session.query(User).filter(User.username == username).first()

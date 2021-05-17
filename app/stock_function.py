import re
from flask import session,request
from app.models import User
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


def is_valid_email(email):
    if re.search(regex,email):
        return True
    else:
        return False
def check_login():
    if 'email' in session:
        email = session['email']
        hashed = session['hashed']
    else:
        email =  request.cookies.get('Useremail')
        hashed = request.cookies.get('Hashed')
    user = User.query.filter((User.email == email)&(User.password==hashed)).first()
    if user is None:
        return False
    else:
        return user
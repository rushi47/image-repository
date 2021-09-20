from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

#using basic auth for now to test - 
# TODO: move auth to flask-login


auth = HTTPBasicAuth()
users = {
    "rushi": generate_password_hash("test@123"),
    "shopify": generate_password_hash("shopify@123")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username
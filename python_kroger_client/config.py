import base64
import os

# Get these 3 values from registering your developer account/application with https://developer.kroger.com/
client_id = os.environ['KROGER_CLIENT_ID']
client_secret = os.environ['KROGER_CLIENT_SECRET']
redirect_uri = os.environ['KROGER_REDIRECT_URI']

# Authentication requires base64 encoded id:secret, which is precalculated here
encoded_client_token = base64.b64encode(f"{client_id}:{client_secret}".encode('ascii')).decode('ascii')

# This is here to make testing the customer client easier.  Obviously we would never want to ask a user for 
# this information.
# FUTURE: Remove this in favor of using the standard authorization path
customer_username = os.environ['KROGER_USERNAME']
customer_password = os.environ['KROGER_PASSWORD']

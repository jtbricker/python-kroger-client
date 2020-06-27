import json

import requests
import simple_cache
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .config import (
    redirect_uri,
    client_id,
)

API_URL = 'https://api.kroger.com/v1'
AUTH_URL = "https://api.kroger.com/v1/connect/oauth2/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope=cart.basic:write product.compact"

@simple_cache.cache_it("access_token.cache", 1800)
def get_customer_access_token(encoded_client_token, redirect_uri, customer_username, customer_password):
    customer_auth_code = get_customer_authorization_code(customer_username, customer_password)
    url = API_URL + '/connect/oauth2/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {encoded_client_token}',
    }
    payload = {
        'grant_type':"authorization_code",
        'code': customer_auth_code,
        'redirect_uri': redirect_uri,
    }
    response = requests.post(url, headers=headers, data=payload)
    return json.loads(response.text).get('access_token')

@simple_cache.cache_it("access_token.cache", 1800)
def get_client_access_token(encoded_client_token):
    url = API_URL + '/connect/oauth2/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {encoded_client_token}',
    }
    payload = {
        'grant_type':"client_credentials",
        'scope':['product.compact'],
    }
    response = requests.post(url, headers=headers, data=payload)
    return json.loads(response.text).get('access_token')

def get_customer_authorization_code(customer_username, customer_password):
    chrome_options = Options()  
    chrome_options.add_argument("--headless")
    driver = Chrome(options=chrome_options)

    url = AUTH_URL.format(client_id=client_id, redirect_uri=redirect_uri)

    # Go to the authorization url, enter username and password and submit
    driver.get(url)
    username = driver.find_element_by_id('username')
    username.send_keys(customer_username)
    password = driver.find_element_by_id('password')
    password.send_keys(customer_password)
    driver.find_element_by_id('signin_button').click()
    
    # The first time you authorize, or change the scope of the authorization, there is a 2nd page 
    # where we need to click an "Authorize button".  
    try:
        auth_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "authorize")))
        if auth_button:
            auth_button.click()
    except:
        pass
    
    uri = driver.current_url

    # After submitting, the authorization page redirects to your apps `uri` with a query parameter
    # `code`, which is the customer authorization code used to authentication the customer client.
    return uri.split("code=")[1]

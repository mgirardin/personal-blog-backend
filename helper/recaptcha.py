import requests
import os

def handle_captcha_token(response):
    RECAPTCHA_KEY = os.environ.get('RECAPTCHA_KEY', "")
    GOOGLE_RECAPTCHA_URL = "https://www.google.com/recaptcha/api/siteverify"
    #TODO: Send user IP
    data = {"secret": RECAPTCHA_KEY, "response": response}
    ans = requests.post(GOOGLE_RECAPTCHA_URL, data=data)
    ans = ans.json()
    #TODO: Check hostname for production environment
    #if(not ans["success"] or ans["hostname"] != "matheusgirardin.com"):
    if(not ans["success"]):    
        return 0
    return ans["score"]
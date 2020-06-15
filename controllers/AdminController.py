import os
import json
from flask import Response
from datetime import datetime
from helper.authentication import create_employee_access_token
from helper.authentication import check_password, generate_salt, generate_password_hash
from helper.authentication import create_employee_refresh_token, validate_employee_refresh_token
from dal import User


DEFAULT_HEADERS = {
    "content-type" : "application/json",
}
PERMISSION_DENIED = json.dumps({"status": "error", "error" : "PermissionDenied"}),401,DEFAULT_HEADERS
NOT_AUTHORIZED = json.dumps({"status": "error", "error" : "WrongCredentials"}),401,DEFAULT_HEADERS
DEFAULT_RESPONSE = json.dumps({"status" : "success"}),200,DEFAULT_HEADERS
MISSING_PARAMETER = json.dumps({"status": "error", "error" : "MissingParameter"}),401,DEFAULT_HEADERS

class EmployeeSignup(object):
    def verify_password_strength(self, password):
        rules = [lambda s: any(x.isupper() for x in s), # must have at least one uppercase
                lambda s: any(x.islower() for x in s),  # must have at least one lowercase
                lambda s: any(x.isdigit() for x in s),  # must have at least one digit
                lambda s: len(s) >= 8                   # must be at least 7 characters
        ]
        return all(rule(password) for rule in rules)

class EmployeeSignin(object):
    def post(self, request):
        payload = request.get_json()
        needed_parameters = ["login", "passwd"]
        if(not all(elem in payload for elem in needed_parameters)):
            return MISSING_PARAMETER
        login = payload["login"]
        passwd = payload["passwd"]
        user = User.get(login)
        if((not user) or (not check_password(passwd, user["salt"], user["passwd"]))):
            return NOT_AUTHORIZED
        encoded_jwt = create_employee_access_token(user["login"])
        json_response = json.dumps({"status" : "success", "jwt": encoded_jwt.decode()})
        resp = Response(json_response)
        resp.set_cookie("refresh_token", value = create_employee_refresh_token(user["login"]), httponly = True, 
                        secure = True, domain=".matheusgirardin.com", samesite='Lax', max_age=24*60*60)
        return resp,200,DEFAULT_HEADERS

class EmployeeRefreshController(object):
    def get(self, request):
        refresh_token = request.cookies.get('refresh_token')
        is_valid, user = validate_employee_refresh_token(refresh_token)
        if(not is_valid):
            return json.dumps({"status": "error", "error" : "NotValidRefreshToken"}),401,DEFAULT_HEADERS
        encoded_jwt = create_employee_access_token(user)
        return json.dumps({"access_token": encoded_jwt.decode()}), 200, DEFAULT_HEADERS
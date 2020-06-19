import os
import json
from dal import Subscriber

DEFAULT_HEADERS = {
    "content-type" : "application/json",
}
PERMISSION_DENIED = json.dumps({"status": "error", "error" : "PermissionDenied"}),401,DEFAULT_HEADERS
NOT_AUTHORIZED = json.dumps({"status": "error", "error" : "WrongCredentials"}),401,DEFAULT_HEADERS
DEFAULT_RESPONSE = json.dumps({"status" : "success"}),200,DEFAULT_HEADERS
MISSING_PARAMETER = json.dumps({"status": "error", "error" : "MissingParameter"}),200,DEFAULT_HEADERS

class SubscriberController(object):
    def post(self, request):
        payload = request.get_json()
        needed_parameters = ["email"]
        if(not all(elem in payload for elem in needed_parameters)):
            return MISSING_PARAMETER
        email = payload["email"]
        try:
            Subscriber.create(email)
        except Exception as e:
            print(e)
            return json.dumps({"status": "error"}), 500, DEFAULT_HEADERS
        return json.dumps({"status": "ok"}), 200, DEFAULT_HEADERS


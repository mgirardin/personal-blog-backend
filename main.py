import json 
from helper import cors
from controllers.ArticleController import ArticleController, ArticlesController
from controllers.AdminController import EmployeeSignin, EmployeeRefreshController
from controllers.SubscriberController import SubscriberController
from controllers.ContactController import ContactController

DEFAULT_HEADERS = {
    "content-type" : "application/json",
}

def defined_routers():
    routers = {
    	"/article" : ArticleController,
        "/articles" : ArticlesController,
        "/contact": ContactController,
        "/signin": EmployeeSignin,
        "/subscribe": SubscriberController,
        "/refresh": EmployeeRefreshController
    }
    return routers

def router(request):
    if request.method == 'OPTIONS':
        headers, allowed = cors.write_headers(request.headers.get("origin"))
        if(allowed):
            return ('', 204, headers)
        return ('', 403, headers)
    if(request.path in defined_routers()):
        tmp_router = defined_routers()[request.path]
        tmp_object = tmp_router()
        response = {}
        if(request.method.lower() in dir(tmp_object)):
            if(request.method.upper() == "GET"):
                response, status, headers = tmp_object.get(request)
            elif(request.method.upper() == "POST"):
                response, status, headers = tmp_object.post(request)
            else:
                return json.dumps({ "error" : "MethodNotAllowed"}),405,DEFAULT_HEADERS
            cors_headers, _ = cors.write_headers(request.headers.get("origin"))
            headers.update(cors_headers)
            return response, status, headers
        else:
            return json.dumps({"error" : "MethodNotAllowed"}),405,DEFAULT_HEADERS
    else:
        return json.dumps({"error" : "Path {} not Found".format(request.path)}),404,DEFAULT_HEADERS
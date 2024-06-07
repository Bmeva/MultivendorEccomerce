from .import models


#this is a middleware which enables us access request object in models.py
def requestObjectMiddleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        models.request_object = request   #request_object i created it on the order model


        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware
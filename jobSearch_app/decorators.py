from functools import wraps
from django.http import HttpResponse
from login_reg_app.models import User
from jobSearch_app.models import *

def validate_request(func):
    @wraps(func)
    def func_wrapper(request, *args, **kwargs):
        try:
            logged_user = None if 'userid' not in request.session else User.objects.get(id=request.session['userid'])
            

        except Exception as ex:
            print(request.session['userid'])

        if logged_user:
            return func(request, logged_user, *args, **kwargs)

        return HttpResponse('Unauthorized', status=401)

    return func_wrapper
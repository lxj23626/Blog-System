from django.shortcuts import redirect

def check_login(func):
    def inner(request, *args, **kwargs):
        if request.session.get('userinfo'):
            return func(request, *args, **kwargs)
        return redirect(('/login.html'))
    return inner

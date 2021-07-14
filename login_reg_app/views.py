from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import User
import datetime as dt
import bcrypt

def sign_in(request):
    return render(request, "sign-in.html")

def log_in(request):
    if request.method == "POST":
        errors = User.objects.sign_in_validator(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        # LOGIN
        try:
            user = User.objects.filter(email = request.POST["email"])
            if user:
                logged_in_user = user[0]
                if bcrypt.checkpw(request.POST["password"].encode(), logged_in_user.password.encode()):
                    request.session['userid'] = logged_in_user.id
                    request.session['user'] = logged_in_user.first_name

                    return redirect('/job')
        except:
            print("No email was found")
        
    return redirect('/')


def get_email(request):
    try:
        user = User.objects.filter(email = request.POST["user-email"])
        if user:
            user_to_reset_pass = user[0]

            context = {
                'user':user_to_reset_pass
            }
            return render(request, 'reset-pass-modal.html', context)
        else:
            return HttpResponse("Email address not found. Please provide another.")
    except:
        return HttpResponse("Email address not found")
        
    return redirect('/')

def reset_password(request, user_id):
    user_to_reset_pass = User.objects.get(id = user_id)
    password = request.POST['password']
    confirm_pass = request.POST['confirm_password']

    if password == confirm_pass:
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        user_to_reset_pass.password = pw_hash
        user_to_reset_pass.save()

        request.session['userid'] = user_to_reset_pass.id
        request.session['user'] = user_to_reset_pass.first_name

        return HttpResponse("Success")
    else:
        return HttpResponse("Passwords don't match, please try again")


def register(request):
    return render(request, "register.html")

def reg_me(request):
    if request.method == "POST":
        errors = User.objects.reg_validator(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register')

        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        new_user = User.objects.create(
            first_name = request.POST["first_name"],
            last_name = request.POST["last_name"],
            email = request.POST["email"],
            birthday = dt.datetime.strptime(request.POST["birthday"], "%m/%d/%Y"),
            password = pw_hash
        )
        
        user_list = User.objects.all()
        if len(user_list) <= 1:
            new_user.user_type = "admin"
            new_user.save()

        request.session["user"] = new_user.first_name
        request.session["userid"] = new_user.id
        return redirect('/job')

def email(request):
    if request.method == "POST":
        found = False
        check_email = User.objects.filter(email=request.POST['email'])
        if check_email:
            found = True
        context = {
            "found": found
        }
    return render(request, 'email-snippet.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')
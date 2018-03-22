from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render_to_response
from django.core.context_processors import csrf

from forums.forms import UserLoginForm

def user_login(request):
    if request.user.is_anonymous():
        if request.method == 'POST':
            form = UserLoginForm(request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                user = cleaned_data.get("user")
                login(request, user)
                if 'next' in request.POST:
                    next_url = request.POST.get('next')
                    return HttpResponseRedirect(next_url)
                return HttpResponseRedirect('/')
        else:
            form = UserLoginForm()
        
        next_url = request.GET.get('next')
        resetpasssucs = request.GET.get('resetpass', False)
        context = {
            'form': form,
            'next': next_url,
            'resetpasssucs': resetpasssucs
        }
        context.update(csrf(request))
        return render_to_response('forums/templates/user-login.html', context)
    else:
        return HttpResponseRedirect('/')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def forgotpassword(request):
    context = {}
    user_emails = []
    context.update(csrf(request))
    if request.method == 'POST':
        users = User.objects.all()
        for user in users:
            user_emails.append(user.email)
        email = request.POST['email']
        if email == "":
            context['invalid_email'] = True
            return render_to_response("forums/templates/forgot-password.html", context)
        if email in user_emails:
            user = User.objects.get(email=email)
            password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            user.set_password(password)
            user.save()
            sender_name = "Spoken Forums"
            sender_email = "no-reply@spoken-tutorial.org"
            subject = "Spoken Forums - Password Reset"
            to = (user.email, )
	    url = settings.EMAIL_URL
            message = """Dear """+user.username+""",\nYour password for Spoken Forums has been reset. Your credentials are:\nUsername: """+user.username+"""\nPassword: """+password+"""\n\nWe recommend you to login with the given credentials & update your password immediately.\nLink to set new password: """+url+"""/accounts/login/?next=/accounts/update-password/\nThank You !\nRegards,\nSpoken Team,\n IIT Bombay."""
	    send_mail(subject, message, sender_email, to)
            form = UserLoginForm()
            context['form'] = form
            #context['password_reset'] = True
            return HttpResponseRedirect('/accounts/login/?next=/accounts/update-password/')
            #return render_to_response("forums/templates/user-login.html", context)
        else:
            context['invalid_email'] = True
            return render_to_response("forums/templates/forgot-password.html", context)
    else:
        return render_to_response('forums/templates/forgot-password.html', context)

def updatepassword(request):
    context = {}
    user = request.user
    context.update(csrf(request))
    if user.is_authenticated():
        if request.method == 'POST':
            new_password = request.POST['new_password']
            confirm = request.POST['confirm_new_password']
            if new_password == "" or confirm == "":
                context['empty'] = True
                return render_to_response("update-password.html", context)
            if new_password == confirm:
                user.set_password(new_password)
                user.save()
                context['password_updated'] = True
                logout(request)
                form = UserLoginForm()
                context['form'] = form
                #return render_to_response('website/templates/index.html', context)
		return HttpResponseRedirect('/')
            else:
                context['no_match'] = True
                return render_to_response("forums/templates/update-password.html", context)
        else:
            return render_to_response("forums/templates/update-password.html", context)
    else:
        form = UserLoginForm()
        context['form'] = form
        context['for_update_password'] = True
        return render_to_response('website/templates/index.html', context)


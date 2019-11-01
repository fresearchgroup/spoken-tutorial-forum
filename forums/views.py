from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout
from django.shortcuts import render_to_response
from django.template.context_processors import csrf

from forums.forms import UserLoginForm


def user_login(request):
    if request.user.is_anonymous:
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
                # return render_to_response('website/templates/index.html', context)
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

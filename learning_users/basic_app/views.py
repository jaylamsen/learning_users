from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request, *args, **kwargs):
    return render(request, 'basic_app/index.html')

def register_views(request, *args, **kwargs):

    registered = False

    if request.method == 'POST':

        user_form = UserForm(data = request.POST)

        profile_form = UserProfileInfoForm(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()


            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
            return HttpResponse("Error Registration")

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/register.html',
                            {'user_form':user_form,
                             'profile_form':profile_form,
                             'registered': registered})

def user_login_views(request, *args, **kwargs):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user:

            if user.is_active:

                login(request, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("User not Active")

        else:
            print("Someone attempted to login to your account.")
            print("Username: {} and Password: {}".format(username, password))
            return HttpResponse("Invalid Login Details")
    else:
        return render(request, 'basic_app/user_login.html', {})

@login_required
def logout_views(request, *args, **kwargs):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

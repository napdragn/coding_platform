from django.shortcuts import render

# Create your views here.
# user/views.py
from django.shortcuts import render
from user.forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json


def index(request):
    return render(request, 'user/index.html')


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def profile_save(request):
    if request.method == 'POST':
        profile_form = UserProfileInfoForm(data=request.POST)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            if 'resume' in request.FILES:
                profile.resume = request.FILES['resume']
            profile.save()
            return JsonResponse({'status': True, 'error': None})
        else:
            print(profile_form.errors)
        return JsonResponse({'status': True, 'error': 'profile data is not valid'})


def register(request):

    registered = False
    if request.method == 'POST':
        error_message = ''
        user_form = UserForm(data=json.loads(request.body))
        if user_form.is_valid():
            try:
                user = user_form.save()
                user.set_password(user.password)
                registered = True
                user.save()
            except Exception as ex:
                error_message = 'User already register.'

        else:
            print(user_form.errors)
    data = {'registered': registered, 'error_message': error_message, 'is_staff': 1, 'user_id': user.id}
    return JsonResponse(data)

    #     profile_form = UserProfileInfoForm(data=request.POST)
    #     if user_form.is_valid() and profile_form.is_valid():
    #         user = user_form.save()
    #         user.set_password(user.password)
    #         user.save()
    #         profile = profile_form.save(commit=False)
    #         profile.user = user
    #         if 'profile_pic' in request.FILES:
    #             print('found it')
    #         profile.save()
    #         registered = True
    #     else:
    #         print(user_form.errors,profile_form.errors)
    # else:
    #     user_form = UserForm()
    #     profile_form = UserProfileInfoForm()
    # return render(request, 'user/registration.html',
    #               {'user_form': user_form,
    #                'profile_form': profile_form,
    #                'registered': registered})


def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return JsonResponse({'user_id': user.id, 'status': True, 'error': ''})
            else:
                return JsonResponse({'status': True, 'error': 'Your account was inactive'})
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return JsonResponse({'status': True, 'error': "Invalid login details given"})
    else:
        return JsonResponse({'status': True, 'error': "Invalid login details given"})
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import messages
import logging
from .models import Room, User
from item.models import Category, Item
from .forms import SignUpForm
from django.contrib.auth import login, SESSION_KEY, BACKEND_SESSION_KEY


def set_auth(request, user):
    request.session['authenticated'] = True  # Optionally store an "authenticated" flag
    request.session[BACKEND_SESSION_KEY] = 'your_custom_auth_backend'
    request.session[SESSION_KEY] = user.pk

def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()
    authenticated = request.session.get('authenticated', False)

    return render(request, 'playground/index.html', {
        'categories': categories,
        'items': items,
        'authenticated': authenticated,
    })

def elements(request, path):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()
    return render(request, path, {
        'categories': categories,
        'items': items,
    })


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(name=username, password=password)
            set_auth(request, user)
            # if (request.session.get('authenticated', False)):
            #     print("yes")
            # else:
            #     print("no")
            return (elements(request, 'playground/user_logged.html'))
        except User.DoesNotExist:
            return render(request, 'playground/sign_in_failed.html')
    return render(request, 'playground/sign_in.html')    


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User(name=name, email=email, password=password)
            user.save()
            set_auth(request, user)
            # if (request.session.get('authenticated', False)):
            #     print("yes")
            # else:
            #     print("no")
            return (elements(request, 'playground/user_logged.html'))
        else:
            print(form.errors)
    return render(request, 'playground/sign_up.html')

def sign_out(request):
    if '_auth_user_id' in request.session:
        del request.session['_auth_user_id']
    if 'authenticated' in request.session:
        del request.session['authenticated']
    # if (request.session.get('authenticated', False)):
    #     print("yes")
    # else:
    #     print("no")
    return (elements(request, 'playground/index.html'))


def base(request):
    return render(request, 'playground/base.html')

def contact(request):
    return render(request, 'playground/contact.html')

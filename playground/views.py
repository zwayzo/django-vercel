from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import messages
import logging
from .models import Room, User
from item.models import Category, Item
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate


def index(request):
    if request.user.is_authenticated:
        print("i'm in")
    else:
        print("i'm out")
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()
    return render(request, 'playground/index.html', {
        'categories': categories,
        'items': items,
    })

def elements(request, path):
    if request.user.is_authenticated:
        print("i'm in")
    else:
        print("i'm out")
    items = Item.objects.filt
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()
    return render(request, path, {
        'categories': categories,
        'items': items,
    })


def sign_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print(" valid")
        else:
            print(form.errors)
        if form.is_valid():
            username = form.cleaned_data.get('name')
            password = form.cleaned_data.get('password')
            user = authenticate(request, name=username, password=password)
            print("before")
            if user is not None:
                print("in")
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('playground/user_logged.html')  # Redirect to the home page after login
            else:
                print("out")
                return redirect('playground/sign_in_failed.html')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'playground/sign_in.html')
    else:
        form = AuthenticationForm()
    return render(request, 'playground/sign_in.html', {'form': form})

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User(name=name, email=email, password=password)
            user.save()
            messages.success(request, "Account created successfully.")
            return (elements(request, 'playground/user_logged.html'))
        else:
            print(form.errors)
    return render(request, 'playground/sign_up.html')

def sign_out(request):
    return (elements(request, 'playground/index.html'))


def base(request):
    return render(request, 'playground/base.html')

def contact(request):
    return render(request, 'playground/contact.html')

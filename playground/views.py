from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import messages
import logging
# Create your views here.

from .models import Room, User
from .forms import SignUpForm


rooms = [
    {'id': 1, 'name': 'English'},
    {'id': 2, 'name': 'Spanish'},
    {'id': 3, 'name': 'Frensh'},
    {'id': 4, 'name': 'German'},
    {'id': 5, 'name': 'Portugais'},
    {'id': 6, 'name': 'Russe'},
    {'id': 7, 'name': 'Italien'},
    {'id': 8, 'name': 'Korean'},
]


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(name=username, password=password)
            return HttpResponse("GOOOOOOOOOD")
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
            return HttpResponse("GOOOO222222D")
        else:
            print(form.errors)
    return render(request, 'playground/sign_up.html')



def playground(request, pk=None):
    if pk is not None:
        room = get_object_or_404(Room, id=pk)
        context = {'room': room}
        return render(request, "playground/" + room.name + ".html")
    else:
        rooms = Room.objects.all()
        context = {'rooms': rooms}
    return render(request, 'playground/choice.html', context)

def welcome(request):
    return render(request, 'playground/welcome.html')

def index(request):
    return render(request, 'playground/index.html')


def base(request):
    return render(request, 'playground/base.html')

def contact(request):
    return render(request, 'playground/contact.html')

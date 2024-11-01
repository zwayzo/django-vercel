from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import messages
import logging
# Create your views here.

from .models import Room, User


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
        print("Received username:", username)
        print("Received password:", password)
        try:
            print("test")
            user = User.objects.get(name=username, password=password)
            # print("User found:", user.name)
            # print("Password in database:", user.password)
            return HttpResponse("GOOOOOOOOOD")
        except User.DoesNotExist:
            return render(request, 'playground/sign_in_failed.html')
    return render(request, 'playground/sign_in.html')    
            # return HttpResponse("GOOOOOOOOOD2")


def sign_up(request):
    return render(request, 'playground/sign_up.html')

def test(request):
    return HttpResponse('tegajhaahahahJAJDJDLK')


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

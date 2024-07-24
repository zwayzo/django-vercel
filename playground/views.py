from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
# Create your views here.

from .models import Room


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

def test(request):
    return HttpResponse('tegajhaahahahJAJDJDLK')

def english(request):
    return render(request, 'playground/English.html')

def spanish(request):
    return render(request, 'playground/Spanish.html')





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
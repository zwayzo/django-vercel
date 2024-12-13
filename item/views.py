from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, User
from .forms import NewItemForm
from django.contrib.auth import login, SESSION_KEY, BACKEND_SESSION_KEY
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import ItemSerializer


def get_google_user_info(request):
    if request.user.is_authenticated:
        # Get the SocialAccount linked to the logged-in user (Google account)
        social_account = SocialAccount.objects.get(user=request.user, provider='google')
        
        # Access the raw data (extra_data) returned by Google
        google_profile = social_account.extra_data
        
        # Extract details from the profile
        print(google_profile)
        name = google_profile.get('name')
        given_name = google_profile.get('given_name')
        family_name = google_profile.get('family_name')
        picture = google_profile.get('picture')
        sub = google_profile.get('sub')  # Unique user ID from Google
        email = google_profile.get('email', 'No Email Provided')
        
        # You can return this information, render in a template, etc.
        return {
            'name': name,
            'given_name': given_name,
            'family_name': family_name,
            'picture': picture,
            'google_id': sub,
            'email': email,
        }
    else:
        return None

# @login_required
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items,
    })



@login_required
def new(request):
    login_url = f"{reverse('sign_in')}?next={request.path}"
    
    if request.user.is_authenticated:
        user_id = request.session.get(SESSION_KEY)
        try:
            # Retrieve the user based on the session's stored user ID
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            user = None  # If the user doesn't exist, set to None
    else:
        return (redirect(login_url))  # No user is authenticated
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return render(request, 'item/detail.html', {
                'item' : item,
            })
    else:
        form = NewItemForm()
    return render(request, 'item/form.html',{
        'form': form,
        'title': 'New item',
    })



@api_view()
def Item_detail(request, id):
    item = get_object_or_404(Item, pk=id)
    serializer = ItemSerializer(item)
    return Response(serializer.data)

@api_view()
def Item_list(request):
    queryset = Item.objects.all()
    serializer = ItemSerializer(queryset, many=True)
    print(serializer.data)
    return Response(serializer.data)
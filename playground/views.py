from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, User, MyUser
from item.models import Category, Item
from .forms import SignUpForm
from django.contrib.auth import login, SESSION_KEY, BACKEND_SESSION_KEY, logout
from django.urls import reverse
from django.conf import settings
from allauth.socialaccount.models import SocialAccount
from django.http import HttpResponse


def set_auth(request, user):
    # Standard Django login for setting up the session correctly
    request.session[settings.SESSION_COOKIE_NAME] = user.pk
    request.session['_auth_user_id'] = user.pk  # Django's expected session key for the user's ID
    request.session['_auth_user_backend'] = 'django.contrib.auth.backends.ModelBackend'  # Specify the backend used
    # request.session['_auth_user_hash'] = user.get_session_auth_hash()  # Session hash for security
    
    # Optionally store additional user information
    request.session['user_name'] = user.name
    request.session['authenticated'] = True  # Optional flag for additional use

    # Update the last login time if desired
    # update_last_login(None, user)
    
    # Alternatively, use Django's login helper
    # login(request, user)


def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()
    if request.user.is_authenticated:
        return render(request, 'playground/user_logged.html', {
        'categories': categories,
        'items': items,
    })
    else:
        return render(request, 'playground/index.html', {
        'categories': categories,
        'items': items,
    })

def elements(request, path):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()
    return render(request, path, {
        'categories': categories,
        'items': items,
    })


def sign_in(request):
    # next_url = request.GET.get('next', reverse('index'))
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user2 = MyUser.objects.get(username=username, password=password)
            user = User.objects.get(username=username)
            # user.is_staff = False
            # user.is_superuser = False
            if request.user.is_authenticated:
                print("befor it's yes")
            else:
                print("befor it's no")
            # set_auth(request, user)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend') 
            if request.user.is_authenticated:
                print("after it's yes")
            else:
                print("after it's no")
            return (elements(request, 'playground/user_logged.html'))
        except User.DoesNotExist:
            return render(request, 'playground/sign_in_failed.html')
    return render(request, 'playground/sign_in.html')    


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # user = User.objects.(nam=nam, password=password, email=email)

            myuser = MyUser(username=username, email=email, password=password)
            user = User(username=username, email=email, password=password)
            user.set_password(password)
            user.is_staff = False
            user.is_superuser = False
            user.first_name = form.cleaned_data.get('first_name', 'DefaultFirstName')
            user.last_name = form.cleaned_data.get('last_name', 'DefaultLastName')
            
            user.save()
            myuser.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend') 
            if request.user.is_authenticated:
                print("yes loged")
            else:
                print("not loged")
            return (elements(request, 'playground/user_logged.html'))
        else:
            print(form.errors)
    return render(request, 'playground/sign_up.html')
# ksk@gmail.com
def sign_out(request):
    # request.session[settings.SESSION_COOKIE_NAME] = None
    # request.session['_auth_user_id'] = None  # Django's expected session key for the user's ID
    # # request.session['_auth_user_backend'] = 'django.contrib.auth.backends.ModelBackend'  # Specify the backend used
    # # request.session['_auth_user_hash'] = user.get_session_auth_hash()  # Session hash for security
    
    # # Optionally store additional user information
    # request.session['user_name'] = None
    # request.session['authenticated'] = False  # Optional flag for additional use
    # if '_auth_user_id' in request.session:
    #     del request.session['_auth_user_id']
    # if 'authenticated' in request.session:
    #     del request.session['authenticated']
    # if (request.session.get('authenticated', False)):
    #     print("yes")
    # else:
    #     print("no")
    if request.user.is_authenticated:
        print("befor it's yes")
    else:
        print("befor it's no")
    logout(request)
    if request.user.is_authenticated:
        print("after it's yes")
    else:
        print("after it's no")
    return (elements(request, 'playground/index.html'))


def base(request):
    return render(request, 'playground/base.html')

def contact(request):
    return render(request, 'playground/contact.html')



def profile_view(request):
    # Check if the user is authenticated and has a social account with Google
    if (request.session.get('authenticated', False)):
        try:
            # Get the Google social account data
            social_account = SocialAccount.objects.get(user=request.user, provider='google')
            extra_data = social_account.extra_data  # Dictionary containing user details
            email = extra_data.get('email')
            name = extra_data.get('name')
            profile_pic = extra_data.get('picture')

            print("email:", email)
            print("name:", name)


            # Render these details in a template or process them as needed
            return HttpResponse("gppppd")

        except SocialAccount.DoesNotExist:
            # Handle case where the user does not have a Google social account
            return HttpResponse("bad")

    return HttpResponse("gppppd")
from django.shortcuts import render, get_object_or_404, redirect
from .models import  User, MyUser, Profile
from item.models import Category, Item
from .forms import SignUpForm, ProfileForm
from django.contrib.auth import login, SESSION_KEY, BACKEND_SESSION_KEY, logout, authenticate
from django.conf import settings
from allauth.socialaccount.models import SocialAccount
from django.http import HttpResponse
from django.conf import settings
import requests
from django.contrib import messages
from django.contrib.auth.hashers import check_password

import secrets
import string


def generate_password(length=12):
    # Define the characters that can be used in the password
    characters = string.ascii_letters + string.digits + string.punctuation
    
    # Generate a secure random password
    password = ''.join(secrets.choice(characters) for _ in range(length))
    
    return password

# Genera

def loginView(request):
    # Redirect to 42 API's OAuth authorization URL
    auth_url = f"https://api.intra.42.fr/oauth/authorize"
    params = {
        "client_id": settings.CLIENT_ID,
        "redirect_uri": settings.REDIRECT_URI,
        "response_type": "code",
    }
    return redirect(f"{auth_url}?client_id={params['client_id']}&redirect_uri={params['redirect_uri']}&response_type=code")

def callback(request):
    # Get the authorization code from the URL
    code = request.GET.get('code')

    # Exchange the authorization code for an access token
    token_url = "https://api.intra.42.fr/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": settings.CLIENT_ID,
        "client_secret": settings.CLIENT_SECRET,
        "code": code,
        "redirect_uri": settings.REDIRECT_URI,
    }
    response = requests.post(token_url, data=data)
    response_data = response.json()

    # Save the access token (you may use sessions or a database)
    access_token = response_data.get("access_token")

    # Use the access token to fetch user data
    user_url = "https://api.intra.42.fr/v2/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_response = requests.get(user_url, headers=headers)
    user_data = user_response.json()
    mylogin = user_data["login"]
    email = user_data["email"]
    first_name = user_data["first_name"]
    last_name = user_data["last_name"]
    plain_password = generate_password(24)
    user, created = User.objects.get_or_create(username=mylogin, defaults={
    "email": email,
    "password": generate_password(12),
    "first_name": first_name,
    "last_name": last_name,
})
    # if created:
    #     user.set_password("1234")
    #     user.save()
    login(request, user, backend='django.contrib.auth.backends.ModelBackend') 

    # Render user data or save it to the database
    return elements(request, 'playground/user_logged.html')


# 'id': 115528, 'email': 'moazzedd@student.1337.ma', 'login': 'moazzedd', 'first_name': 'Mohammed', 
# 'last_name': 'Azzeddine', 'usual_full_name': 'Mohammed Azzeddine', 'usual_first_name': None, 
# 'url': 'https://api.intra.42.fr/v2/users/moazzedd', 'phone': 'hidden', 'displayname': 'Mohammed Azzeddine', 
# 'kind': 'student', 'image': {'link': 'https://cdn.intra.42.fr/users/945f2f5274ec3ca7c9b628cca163f770/moazzedd.JPG',
# 'versions': {'large': 'https://cdn.intra.42.fr/users/ed119ebc81460391dd65f79cda8b543f/large_moazzedd.JPG', 
# 'medium': 'https://cdn.intra.42.fr/users/82044492318e815bb8dadbc3c6378035/medium_moazzedd.JPG', 
# 'small': 'https://cdn.intra.42.fr/users/d36e0d2dd9decbbc214cee745ee6dbb5/small_moazzedd.JPG', 
# 'micro': 'https://cdn.intra.42.fr/users/dcd34853c48a43089d0f2d42d0069177/micro_moazzedd.JPG'}},
# 'staff?': False, 'correction_point': 3, 'pool_month': 'july', 'pool_year': '2022', 'location': 'e2r3p10',
# 'wallet': 145, 'anonymize_date': '2027-11-24T00:00:00.000+01:00', 'data_erasure_date': '2027-11-24T00:00:00.000+01:00', 
# 'created_at': '2022-06-29T11:20:29.739Z', 'updated_at': '2024-11-24T21:32:25.322Z', 'alumnized_at': None,
# 'alumni?': False, 'active?': True, 'groups': [], 'cursus_users': [{'id': 173092, 'begin_at': '2022-07-18T08:37:00.000Z',
#  'end_at': '2022-08-13T08:37:00.000Z', 'grade': None, 'level': 8.85, 'skills': [{'id': 4, 'name': 'Unix', 'level': 10.33},
#  {'id': 1, 'name': 'Algorithms & AI', 'level': 7.21}, {'id': 3, 'name': 'Rigor', 'level': 5.84}, 
#  {'id': 14, 'name': 'Adaptation & creativity', 'level': 5.07}], 'cursus_id': 9, 'has_coalition': True, 'blackholed_at': None,
# 'created_at': '2022-06-29T11:20:29.780Z', 'updated_at': '2022-06-29T11:20:29.780Z', 


def G_loginView(request):
    # Redirect to 42 API's OAuth authorization URL
    auth_url = f"https://github.com/login/oauth/authorize"
    params = {
        "client_id": settings.G_CLIENT_ID,
        "redirect_uri": settings.G_REDIRECT_URI,
        "response_type": "code",
    }
    return redirect(f"{auth_url}?client_id={params['client_id']}&redirect_uri={params['redirect_uri']}&response_type=code")


def G_callback(request):
    # Get the authorization code from the URL
    code = request.GET.get('code')
    # Exchange the authorization code for an access token
    token_url = "https://github.com/login/oauth/access_token"
    data = {
        "client_id": settings.G_CLIENT_ID,
        "client_secret": settings.G_CLIENT_SECRET,
        "code": code,
        "redirect_uri": settings.G_REDIRECT_URI,
    }
    headers = {"Accept": "application/json"}  # Important to specify JSON response
    response = requests.post(token_url, data=data, headers=headers)

    # Debug the raw response content
    print("Raw response from GitHub:", response.text)

    try:
        response_data = response.json()
    except requests.exceptions.JSONDecodeError:
        return JsonResponse({"error": "Failed to parse GitHub response as JSON."}, status=400)

    # Get the access token
    access_token = response_data.get("access_token")
    if not access_token:
        return JsonResponse({"error": "Access token not received."}, status=400)

    # Use the access token to fetch user data
    user_url = "https://api.github.com/user"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_response = requests.get(user_url, headers=headers)

    if user_response.status_code != 200:
        return JsonResponse({"error": "Failed to fetch user data."}, status=user_response.status_code)

    user_data = user_response.json()
    mylogin = user_data["login"]
    email = user_data["email"]
    print("data:",user_data.get("email"))
    user, created = User.objects.get_or_create(username=mylogin, defaults={"email": email})
    login(request, user, backend='django.contrib.auth.backends.ModelBackend') 

    # Example: Store in session or process the data
    request.session['github_user'] = {
        "username": user_data.get("login"),
        "email": user_data.get("email"),
    }

    # Redirect to the homepage or dashboard
    return render(request, "playground/user_logged.html", {"github_user": request.session.get('github_user')})


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
    user = request.user
    return render(request, path, {
        'categories': categories,
        'items': items,
        'user': user,
    })

def sign_in(request):
    # next_url = request.GET.get('next', reverse('index'))
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            # user2 = MyUser.objects.get(username=username, password=password)
            user = User.objects.get(username=username)
            if check_password(password, user.password) == False:
                return render(request, 'playground/sign_in_failed.html')
            login(request, user, backend='django.contrib.auth.backends.ModelBackend') 
            return (elements(request, 'playground/user_logged.html'))
        except :
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
            return (elements(request, 'playground/user_logged.html'))
        else:
            print(form.errors)
    return render(request, 'playground/sign_up.html')
# ksk@gmail.com
def sign_out(request):
    logout(request)
    return (elements(request, 'playground/index.html'))

def profile(request):
    user = request.user  # Get the logged-in user
    profile, created = Profile.objects.get_or_create(user=user)  # Fetch or create the profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after saving the form
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'playground/profile.html', {
        'form': form,
        'profile': profile,
        'user': user,
    })

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
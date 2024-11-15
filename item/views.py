from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, User
from .forms import NewItemForm
from django.contrib.auth import login, SESSION_KEY, BACKEND_SESSION_KEY
from django.urls import reverse
from django.contrib.auth.decorators import login_required

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
        print("authenticated")
    else:
        print("not authenticated")
    
    if request.user.is_authenticated:
        user_id = request.session.get(SESSION_KEY)
        print("user_id:", user_id)
        try:
            # Retrieve the user based on the session's stored user ID
            user = User.objects.get(username=user_id)
        except User.DoesNotExist:
            print("catch")
            user = None  # If the user doesn't exist, set to None
    else:
        print("redirect")
        return (redirect(login_url))  # No user is authenticated
    if request.method == 'POST':
        if User.DoesNotExist:
            print("does not exist")
        else:
            print("exist")
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            # print()
            item.created_by = request.user
            # print("created_by:", item.created_by)
            item.save()
            return render('item:detail')
    else:
        form = NewItemForm()
    return render(request, 'item/form.html',{
        'form': form,
        'title': 'New item',
    })

from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, User
from django.contrib.auth.decorators import login_required
from .forms import NewItemForm
from django.contrib.auth import login, SESSION_KEY, BACKEND_SESSION_KEY



def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    authenticated = request.session.get('authenticated', False)
    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items,
        'authenticated': authenticated,
    })


# @login_required
def new(request):
    authenticated = request.session.get('authenticated', False)
    if authenticated:
        user_id = request.session.get(SESSION_KEY)
        print("user_id:", user_id)
        try:
            # Retrieve the user based on the session's stored user ID
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            user = None  # If the user doesn't exist, set to None
    else:
        user = None  # No user is authenticated
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return render('item:detail',{
                'authenticated': authenticated
            })
    else:
        form = NewItemForm()
    return render(request, 'item/form.html',{
        'form': form,
        'title': 'New item',
        'authenticated': authenticated,
    })
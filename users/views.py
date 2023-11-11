from django.shortcuts import render, redirect
from . forms import UserRegisterForm
from django.contrib import messages 
from django.contrib.auth import user_logged_in


def logged_in_message(sender, user, request, **kwargs):
    """
    Add a welcome message when the user logs in
    """
    messages.info(request, f'Welcome {user.username}!')
user_logged_in.connect(logged_in_message)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) # get data from register form and clean it
        if form.is_valid():
            form.save()#
            messages.success(request, f'Your account has been created! Now you can log in')
            return redirect('login')
    else :
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'title': 'Register'})


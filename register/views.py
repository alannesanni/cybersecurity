from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


def register(response):
    if response.method == "POST":
        username = response.POST.get('username')
        password1 = response.POST.get('password1')
        password2 = response.POST.get('password2')
        if password1 != password2:
            pass
        else:
            # flaw 2
            user = User.objects.create_user(username=username, password=password1)
            user.save()
            return redirect("/login")
    return render(response, "register/register.html")

# fix 2 and 4:
#def register(response):
#    if response.method == "POST":
#        form = UserCreationForm(response.POST)
#        if form.is_valid():
#            form.save()
#        return redirect("/login")
#    else:
#        form = UserCreationForm()
#    return render(response, "register/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('/login')



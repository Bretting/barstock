from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

# Create your views here.


def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        next_url = request.POST.get('next')

        user = authenticate(request, username=username, password=password)
        if user is None:
            context = {"error": "Invalid username or password."}
            return render(request, "Accounts/login.html", context)
        login(request, user)

        if next_url:
            return HttpResponseRedirect(next_url)
        else:
            return redirect('/')    

    return render(request, "Accounts/login.html", {})


def logout_view(request):
    if request.method =='POST':
        logout(request)
        return redirect("/sign-in")

    return render(request,"Accounts/logout.html")
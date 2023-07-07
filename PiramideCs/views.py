from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .models import User

# Create your views here.
def index(request):
    if request.method == "GET":
        return render(request,"PiramideCs/index.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
    
def register(request):
    if request.method == "GET":
        return render(request,"PiramideCs/register.html")
    elif request.method == "POST":
        
        username = request.POST["username"]
        email = request.POST["email"]
        password = str(request.POST["password"])
        passwordConfirmation = str(request.POST["passwordconf"])
        fieldsNotFilled = not username or not email or not password or not passwordConfirmation
        
        if fieldsNotFilled:
            return render(request, "PiramideCs/register.html",{
                "message":"Todos os campos precisam ser preenchidos."
            })
        elif passwordConfirmation != password:
             return render(request, "PiramideCs/register.html",{
                "message":"A senha precisa coincidir com a senha de confirmação."
            })
        else:
            try:
                user = User.objects.create_user(username,email,password)
                user.save()
            except IntegrityError:
                return render(request, "PiramideCs/register.html", {
                "message": "Username já está em uso."
            })
        login(request,user)
        return HttpResponseRedirect(reverse("index"))
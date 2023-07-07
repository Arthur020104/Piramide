from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .models import User

# Create your views here.
@login_required(login_url="/Login")
def index(request):
    userId = request.user.id
    user = User.objects.get(pk = userId)
    if request.method == "GET":
        user.CanPlayIn()
        return render(request,"PiramideCs/index.html")
    elif request.method == "POST":
        try:
            betAmount = float(request.POST['betAmount'])
        except:
            return render(request,"PiramideCs/index.html", {
                "message": "Precisa fornecer um número."
            })
        jogada = user.Play(betAmount)
        print(jogada)
        if not jogada:
            return render(request,"PiramideCs/index.html", {
                "message": "Jogada inválida."
            })
        else:
            return render(request,"PiramideCs/index.html", {
                "message_sucess": jogada
            })

@login_required(login_url="/Login")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
    
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        passwordConfirmation = request.POST['passwordconf']

        if not username or not email or not password or not passwordConfirmation:
            return render(request, "PiramideCs/register.html", {
                "message": "Todos os campos precisam ser preenchidos."
            })
        if password != passwordConfirmation:
            return render(request, "PiramideCs/register.html", {
                "message": "Senhas precisam ser iguais."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "PiramideCs/register.html", {
                "message": "Username já está em uso."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    return render(request, "PiramideCs/register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, "PiramideCs/login.html",{
                "message":"Inválido username e/ou senha."
            })
        else:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

    return render(request, "PiramideCs/login.html")
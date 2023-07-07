from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .models import User
from django.utils import timezone

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
        print(user.Play(betAmount))
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
                user = User.objects.create_user(username = username,email = email,password = password,_saldo = 0.0,DateofPlay = timezone.now())
                user.save()
            except IntegrityError:
                return render(request, "PiramideCs/register.html", {
                "message": "Username já está em uso."
            })
        login(request,user)
        return HttpResponseRedirect(reverse("index"))
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

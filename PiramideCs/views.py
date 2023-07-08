from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .models import User
from django.core.exceptions import PermissionDenied
login_url= "/Login"
# Create your views here.
@login_required(login_url=login_url)
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
        print(user.CanPlayIn())
        print(jogada)
        
        if not jogada:
            return render(request,"PiramideCs/index.html", {
                "message": "Jogada inválida."
            })
        else:
            return render(request,"PiramideCs/index.html", {
                "message_sucess": jogada,"afthermatch": "SÓ PODE APOSTAR EM 12 HORAS"
            })
        
        

@login_required(login_url=login_url)
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
@login_required(login_url=login_url)
def carteira(request,message=None, message_sucess=None):
    user = User.objects.get(pk= request.user.id)
    if message:
        return render(request,"PiramideCs/carteira.html",{
                "user":user,
                "message":message["ERRO"]
                }) 
    elif message_sucess:
        return render(request,"PiramideCs/carteira.html",{
            "user":user,
            "message_sucess":message_sucess["Sucess"]
            })
    
    if request.method == "GET":
        return render(request,"PiramideCs/carteira.html",{
            "user":user
            })
    else:
        try:
            withdrawValue = float(request.POST["withdrawValue"])
        except:
            return render(request,"PiramideCs/carteira.html",{
            "user":user,
            "message":"Necessário fornecer um valor válido."
            })
        saldo = user.Withdraw(withdrawValue)
        
        if(saldo):
            return render(request,"PiramideCs/carteira.html",{
                "user":user,
                "message_sucess":f"Saque efetuado com sucesso."
                })
        else:
            return render(request,"PiramideCs/carteira.html",{
                "user":user,
                "message":"[ERRO] Saque inválido."
                })
@login_required(login_url=login_url)
def deposite(request):
    if request.method == "POST":
        try:
            depositeValue = float(request.POST["depositeValue"])
            user = User.objects.get(pk=request.user.id)
            user.deposite(depositeValue)
        except:
           carteira(request,{"ERRO":"Necessário fornecer um valor válido."})
        return carteira(request,None,{"Sucess":"Deposito efetuado com sucesso."})
    else:
        raise PermissionDenied()
    
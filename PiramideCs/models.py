from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random
from django.utils import timezone
from datetime import timedelta

# Create your models here.
def subtractTwelve():
    return (timezone.now()- timedelta(hours=12, minutes=0))
class User(AbstractUser):

    _saldo = models.FloatField(("Saldo"),default=0)
    DateofPlay = models.DateTimeField(("DateofPlay"), default=subtractTwelve)
    user_permissions = None
    groups =None
    def _returnedValue(self,betAmount):
        winPercentTableDays = [125, 75, -25]
        winPercentTableUsers = [100,25,-2000]
        accountDays = int((timezone.now() - self.date_joined).days)#days after account initiation
        accountDays = 0 if accountDays < 5 else 1 if accountDays < 12 else 2
        amountofUsers = int(User.objects.all().count())
        amountofUsers = 0 if amountofUsers < 3 else 1 if amountofUsers < 7 else 2
        totalPercent = winPercentTableDays[accountDays] + winPercentTableUsers[amountofUsers]
        totalPercent = random.randrange(totalPercent-10,totalPercent+ totalPercent *5)#variation +-10%
        if(totalPercent <= -100):
            return "[Erro]: Problema no saque, entre em contato com o nosso suporte na aba suporte."
        else:
            total = betAmount * (1+ (totalPercent/100) )
            newValue = self.getSaldo() + total
            self._setSaldo(newValue)
            if totalPercent > 0:
                return f"Você ganhou {totalPercent}% do seu valor inicial, totalizando em {total}."
            else:
                return f"Não foi dessa vez, seu total é {total}."
    def CanPlayIn(self):
        if self.DateofPlay != None:
            current_time = timezone.now()
            self.DateofPlay
            time_difference = current_time - self.DateofPlay
            hours_difference = time_difference.total_seconds() / 3600
            #print(hours_difference)
            hours_difference = 0 if hours_difference >= 12  else 12 - hours_difference
            #print(hours_difference,current_time,self.DateofPlay)
            return int(hours_difference)
    def Play(self,betAmount):
        if(self.CanPlayIn() == 0):
            try: 
                returnedV = self._returnedValue(betAmount)
                self.DateofPlay = timezone.now()
                self.save()
                return returnedV
            except:
                return False
        else:
            False

        
    def getSaldo(self):
        if self._saldo:   
            return self._saldo
        else:
            return False
    def _setSaldo(self,newValue):
        try:
            newValue = float(newValue)
        except:
            return False
        self._saldo = newValue
        self.save()
        return True
    def Withdraw(self,withdrawValue):
        isValidToWithdraw = None
        if self.getSaldo():
            isValidToWithdraw = self.getSaldo() > 0
        if(isValidToWithdraw):
            try:  
                newValue = self.getSaldo() - withdrawValue
            except:
                return False
            return self._setSaldo(newValue)
        else:
            return False
    def _str_(self):
        return f"{self.id}: {self.username}."

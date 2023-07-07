from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random
# Create your models here.

class User(AbstractUser):
    _saldo = models.FloatField(blank=True,null=True)
    user_permissions = models.ManyToManyField(
    "auth.Permission",
    verbose_name="user permissions",
    blank=True,
    related_name="custom_user_set"  # Add a unique related_name
    )
    groups = models.ManyToManyField( 
        "auth.Group",
        verbose_name="groups",
        blank=True,
        related_name="custom_user_set"  # Add a unique related_name
    )
    def returnedValue(self,betAmount):
        winPercentTableDays = {tuple(range(1, 6)):125,tuple(range(6,12)): 75, tuple(range(12, 30)): -25}
        winPercentTableUsers = {tuple(range(1, 10)):100,tuple(range(10,500)):25,tuple(range(500, 2000)):-2000}
        accountDays = int(timezone.now() - self.date_joined)#days after account initiation
        amountofUsers = int(self.objects.all().count())
        totalPercent = winPercentTableDays[accountDays] + winPercentTableUsers[amountofUsers]
        totalPercent = random.randrange(totalPercent-10,totalPercent+10)#variation +-10%
        if(totalPercent <= -100):
            return "[Erro]: Problema no saque, entre em contato com o nosso suporte na aba suporte."
        else:
            total = betAmount * (1+ (totalPercent/100) )
            newValue = self.getSaldo() + total
            self._setSaldo(self, newValue)
            if totalPercent > 0:
                return f"Você ganhou {totalPercent}% do seu valor inicial, totalizando em {total}."
            else:
                return f"Não foi dessa vez, seu total é {total}."
        
        
    def getSaldo(self):
        if self._saldo:   
            return self._saldo
        else:
            return False
    def _setSaldo(self,newValue):
        try:
            newValue = float(newValue)
            return True
        except:
            return False
    def Withdraw(self,withdrawValue):
        isValidToWithdraw = None
        if self.getSaldo():
            isValidToWithdraw = self.getSaldo() > 0
        if(isValidToWithdraw):
            try:  
                newValue = self.getSaldo() - withdrawValue
            except:
                return False
            return self._setSaldo(self, newValue)
        else:
            return False
    def _str_(self):
        return f""
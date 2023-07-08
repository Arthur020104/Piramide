from django.contrib import admin

# Register your models here.
from .models import User
class ListandoUsers(admin.ModelAdmin):
   list_display = ('id', 'username','DateofPlay','_saldo')
   list_display_links = ('id', 'username','DateofPlay','_saldo')
   search_fields = ['username']
admin.site.register(User,ListandoUsers)
#class ListandoUsers(admin.ModelAdmin):
 #   list_display = ('id', 'username','DateofPlay','_saldo')
 #   list_display_links = ('id', 'username','DateofPlay','_saldo')
 #   search_fields = ['username']
#admin.site.register(User,ListandoUsers)

import models
from django.contrib import admin
from myproject.geno.models import Nodo, NodoLog

class NodoAdmin(admin.ModelAdmin):
    list_display  = ('year_born','nombre','a_paterno','a_materno')
    search_fields = ('nombre','a_paterno','a_materno')

admin.site.register(Nodo,NodoAdmin)
admin.site.register(NodoLog)
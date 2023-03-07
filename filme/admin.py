from django.contrib import admin
from .models import Filme, Episodio, Usuario
from django.contrib.auth.admin import UserAdmin

#Para aparecer no admin o campo de Filmes Vistos
campos = list(UserAdmin.fieldsets) #Transformou os campos em lista
campos.append(
    ("Histórico", {'fields': ('filmes_vistos',)}) #colocou em histórico
)
UserAdmin.fieldsets = tuple(campos) #voltou para uma tupla

admin.site.register(Filme)
admin.site.register(Episodio)
admin.site.register(Usuario, UserAdmin)

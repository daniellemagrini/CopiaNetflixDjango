from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django import forms


class FormHomepage(forms.Form): #Criando um form do zero
    email = forms.EmailField(label=False)


class CriarContaForm(UserCreationForm): #Subclasse do UserCreationForm
    email = forms.EmailField()

    class Meta: #Classe obrigatória que diz qual o modelo que gerencia o modelo Usuário
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2') # Campos que serão exibidos no formulário na hora de criar uma conta (tupla)
from django.urls import path, include, reverse_lazy
from .views import Homepage, Homefilmes, Detalhesfilme, Pesquisafilme, Editarperfil, Criarconta
from django.contrib.auth import views as auth_view


app_name = 'filme'

urlpatterns = [
    #path('', homepage), #Aqui seria se fosse usada a funcao na view, mas usamos a classe, por isso as linhas de baixo
    #path('cursos/', homecursos),
    path('', Homepage.as_view(), name='homepage'),
    path('filmes/', Homefilmes.as_view(), name='homefilmes'),
    path('filmes/<int:pk>', Detalhesfilme.as_view(), name='detalhesfilme'), # Identifica a primary key do filme e abre aquele filme
    path('pesquisa/', Pesquisafilme.as_view(), name='pesquisafilme'),
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name='login'), #Função LoginView já existe no Django
    path('logout/', auth_view.LogoutView.as_view(template_name='logout.html'), name='logout'), #Função LogoutView já existe no Django
    path('editarperfil/<int:pk>', Editarperfil.as_view(), name='editarperfil'),
    path('criarconta/', Criarconta.as_view(), name='criarconta'),
    path('mudarsenha/', auth_view.PasswordChangeView.as_view(template_name='editarperfil.html', success_url=reverse_lazy('filme:homefilmes')), name='mudarsenha'),
]
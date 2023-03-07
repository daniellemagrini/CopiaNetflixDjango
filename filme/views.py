from django.shortcuts import render, redirect, reverse
from .models import Filme, Usuario
from .forms import CriarContaForm, FormHomepage
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

#Não vamos usar a função e sim a Classe
#def homepage(request): # request = GET ou POST
#    return render(request, "homepage.html")

#def homecursos(request):
#    context = {} #Dicionário python onde tem as informações
#    lista_cursos = filme.objects.all() #Pega todos os objetos do BD da classe filme
#    context['lista_cursos'] = lista_cursos
#    return render(request, "homecursos.html", context)


class Homepage(FormView): # único objetivo é renderizar um template
    template_name = "homepage.html" # Obrigatório
    form_class = FormHomepage

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated: #Se o usuário estiver autenticado, ou seja, já fez o login
            return redirect('filme:homefilmes')  # Redireciona para a homefilmes - redirecionando para outra view e não template
        else: #Se o usuário não estiver autenticado
            return super().get(request, *args, **kwargs) #Redireciona para a homepage

    def get_success_url(self): #Função Obrigatória - O que vai acontecer se o form for bem sucedido, espera um link no return
        email = self.request.POST.get("email")
        usuario = Usuario.objects.filter(email=email)
        if usuario:
            return reverse('filme:login')
        else:
            return reverse('filme:criarconta')


class Homefilmes(LoginRequiredMixin, ListView): # LoginRequiredMixin sempre tem que vir em primeiro dentro do parenteses
    template_name = "homefilmes.html"
    model = Filme # Nome da lista é padrão = object_list - Lista de itens do modelo


class Detalhesfilme(LoginRequiredMixin, DetailView):
    template_name = "detalhesfilme.html"
    model = Filme # Nome do item é padrão = object

    #Para fazer a contagem de vizualizações, conforme entra naquele filme
    def get(self, request, *args, **kwargs):
        filme = self.get_object()
        filme.visualizacoes += 1
        filme.save() #Salvando a informação no BD
        usuario = request.user
        usuario.filmes_vistos.add(filme) #não é append, pq não é adicionado em lista e sim no BD
        return super().get(request, *args, **kwargs) #Redireciona o usuário apra o link final

    #Lista de filmes relacionados
    def get_context_data(self, **kwargs):
        context = super(Detalhesfilme, self).get_context_data(**kwargs) # para garantir que executa essa funcao original que ja vem no DetailView
        #informaçoes que queremos adicionar a função (sem sobrescrever, pois já garantimos a original rodar na linha de cima)
        # self.get_object() - Pegar o filme que queremos
        filmes_relacionados = self.model.objects.filter(categoria=self.get_object().categoria)[0:5] #Pegando 5 filmes relacionados por categoria
        context['filmes_relacionados'] = filmes_relacionados #Criar essa variável filmes relacionados
        return context

class Pesquisafilme(LoginRequiredMixin, ListView):
    template_name = "pesquisa.html"
    model = Filme

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = self.model.objects.filter(titulo__icontains=termo_pesquisa)
            return object_list
        else:
            return None

class Editarperfil(LoginRequiredMixin, UpdateView):
    template_name = "editarperfil.html"
    model = Usuario
    fields = ['first_name', 'last_name', 'email'] #campos escritos do jeito que está no banco

    def get_success_url(self):
        return reverse('filme:homefilmes')

class Criarconta(FormView):
    template_name = "criarconta.html"
    form_class = CriarContaForm

    def form_valid(self, form): # Verifica se os campos foram preenchidos
        form.save() #para gravar no BD
        return super().form_valid(form)

    def get_success_url(self): #Função Obrigatória - O que vai acontecer se o form for bem sucedido, espera um link no return
        return reverse('filme:login') #Reverse para Link, redirect para página
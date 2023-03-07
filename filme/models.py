from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

#Lista de categorias dos filmes
LISTA_CATEGORIAS = ( #Como será armazenado no banco de dados e como será exibido no site (pode ser igual)
    ("ANALISES", "Análises"),
    ("PROGRAMACAO", "Programação"),
    ("APRESENTACAO", "Apresentação"),
    ("OUTROS", "Outros"),
)


#Cursos
class Filme(models.Model):
    titulo = models.CharField(max_length=100)
    thumb = models.ImageField(upload_to='thumb_cursos')
    descricao = models.TextField(max_length=1500)
    categoria = models.CharField(max_length=30, choices=LISTA_CATEGORIAS)
    visualizacoes = models.IntegerField(default=0)
    data_criacao = models.DateTimeField(default=timezone.now) #Sem () no final, pega a hora de agora e preenche, com o () chama uma função e pegaria a data e hora sempre que abrisse um filme

    def __str__(self): # Como esse valor vai ser exibido - Quando ele pedir em formato de string, volta essa função
        return self.titulo # Retorna o título do filme


#EPISÓDIOS
class Episodio(models.Model):
    filme = models.ForeignKey("Filme", related_name="episodios", on_delete=models.CASCADE) # Colocar sempre em primeiro, pois é uma chave estrangeira, assim evita possíveis problemas no BD
    titulo = models.CharField(max_length=100)
    link_video = models.URLField()

    def __str__(self): # Como esse valor vai ser exibido - Quando ele pedir em formato de string, volta essa função
        return self.titulo # Retorna o título do filme


#USUÁRIO
class Usuario(AbstractUser): #Esse Abstract já traz alguns campos, por exemplo, nome, email, etc
    filmes_vistos = models.ManyToManyField("Filme")

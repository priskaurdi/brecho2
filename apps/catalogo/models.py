from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.utils import timezone
from django.utils.text import slugify
import random
import string


user = get_user_model()

# Create your models here. 
class Catalogo(models.Model):   
    usuario = models.ForeignKey(user, 
								related_name="user_catalogo", on_delete=models.CASCADE) 
    #foto = models.ImageField(upload_to='catalogo/foto/', blank=True)  
    produto = models.CharField('Produto',max_length=100)
    descProduto = models.TextField('Descrição Produto',max_length=350)  
    categoria = models.CharField('Categoria', max_length=20)
    unidade = models.CharField('Unidade', max_length=20)
    valor = models.CharField('Valor', max_length=20)
    data_publicacao = models.DateField(blank=True, null=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    ativo = models.BooleanField('Publicar Produto?', default=False)
    
    slug = models.SlugField(unique=True, null=True, blank=True )  # Campo de slug
    
    def __str__(self):
        return "{} ({})".format(self.produto, self.data_publicacao)

    class Meta:
        verbose_name = "Catalogo"
        verbose_name_plural = "Catalogo"
        ordering = ['-data_criacao']

    def save(self, *args, **kwargs):
        if not self.slug:  # Executa apenas se o campo 'slug' estiver vazio
            slug_base = slugify(self.produto)  # Gera o slug com base no título
            random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))  # Gera uma string aleatória de 5 caracteres
            self.slug = f"{slug_base}-{random_string}"  # Adiciona a string aleatória ao slug base
        super().save(*args, **kwargs)

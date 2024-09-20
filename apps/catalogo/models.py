from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.text import slugify
import random
import string
from contas.models import MyUser


user = get_user_model()

# Create your models here. 
class Catalogo(models.Model):   
    usuario = models.ForeignKey(user, 
								related_name="usuario_catalogo", on_delete=models.CASCADE) 
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


class CatalogoImagem(models.Model):
    imagem = models.FileField('Imagem Anexo', upload_to='catalogo-catalogo/')
    catalogo = models.ForeignKey(Catalogo, 
					related_name='catalogo_imagens', on_delete=models.CASCADE)
 
    def __str__(self):
        return self.catalogo.produto
    
    def clean(self):
        super().clean()
        if self.catalogo.catalogo_imagens.count() >= 5: # Limitar somente 5 anexos
            raise ValidationError('Você só pode adicionar no máximo 5 anexos.')


class CatalogoComentario(models.Model):
    usuario = models.ForeignKey(user, on_delete=models.CASCADE, 
								related_name='usuario_comentario_catalogo')
    catalogo = models.ForeignKey(Catalogo, 
								on_delete=models.CASCADE, related_name="catalogo_comentario") 
    parent = models.ForeignKey('self', 
								on_delete=models.CASCADE, blank=True, null=True, related_name='+') 
    data_criacao = models.DateTimeField(auto_now_add=True)
    comentario = models.TextField(blank=True, null=True)     
   
    @property
    def children(self):
        return CatalogoComentario.objects.filter(parent=self).order_by('-data_criacao').all()

    @property
    def is_parent(self): 
        if self.parent is None:
            return True
        return False 
    
    def __str__(self):
        return '{} - {}'.format(self.usuario.email, self.catalogo.produto)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['-data_criacao']
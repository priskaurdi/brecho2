# Generated by Django 5.1 on 2024-09-19 10:11

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Catalogo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('produto', models.CharField(max_length=100, verbose_name='Produto')),
                ('descProduto', models.TextField(max_length=350, verbose_name='Descrição Produto')),
                ('categoria', models.CharField(max_length=20, verbose_name='Categoria')),
                ('unidade', models.CharField(max_length=20, verbose_name='Unidade')),
                ('valor', models.CharField(max_length=20, verbose_name='Valor')),
                ('data_publicacao', models.DateField(blank=True, null=True)),
                ('data_criacao', models.DateTimeField(default=django.utils.timezone.now)),
                ('ativo', models.BooleanField(default=False, verbose_name='Publicar Produto?')),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario_catalogo', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Catalogo',
                'verbose_name_plural': 'Catalogo',
                'ordering': ['-data_criacao'],
            },
        ),
        migrations.CreateModel(
            name='CatalogoComentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('comentario', models.TextField(blank=True, null=True)),
                ('catalogo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='catalogo_comentario', to='catalogo.catalogo')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='catalogo.catalogocomentario')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario_comentario_catalogo', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Comentário',
                'verbose_name_plural': 'Comentários',
                'ordering': ['-data_criacao'],
            },
        ),
        migrations.CreateModel(
            name='CatalogoImagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.FileField(upload_to='catalogo-catalogo/', verbose_name='Imagem Anexo')),
                ('catalogo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='catalogo_imagens', to='catalogo.catalogo')),
            ],
        ),
    ]

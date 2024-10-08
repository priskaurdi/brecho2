# Generated by Django 5.1 on 2024-09-18 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='bairro',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='perfil',
            name='cep',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='perfil',
            name='compEnd',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='perfil',
            name='cpf',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='perfil',
            name='dtNascimento',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='perfil',
            name='endereco',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='perfil',
            name='numCasa',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='perfil',
            name='rg',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]

# Generated by Django 5.1 on 2024-09-18 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_alter_blocos_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='conteudo',
            name='descricao_3',
            field=models.CharField(blank=True, help_text='Descrição mais curta até 200 caracteres', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='conteudo',
            name='descricao_4',
            field=models.CharField(blank=True, help_text='Descrição mais curta até 200 caracteres', max_length=200, null=True),
        ),
    ]

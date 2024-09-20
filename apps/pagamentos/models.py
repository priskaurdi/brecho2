from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from catalogo.models import Catalogo
from quadros.models import Quadros

user = get_user_model()

class PagamentoPIX(models.Model):
    usuario = models.ForeignKey(user, on_delete=models.CASCADE, related_name="pagamentos")
    chave_pix = models.CharField('Chave PIX', max_length=100)
    valor_total = models.DecimalField('Valor Total', max_digits=10, decimal_places=2)  # Valor total do pagamento
    status = models.CharField('Status', max_length=20, choices=[('pendente', 'Pendente'), ('pago', 'Pago')], default='pendente')
    data_pagamento = models.DateTimeField('Data do Pagamento', default=timezone.now)

    # Relacionamento com Catalogo e Quadros
    produto = models.ForeignKey(Catalogo, null=True, blank=True, on_delete=models.SET_NULL, related_name='pagamentos_produto')
    quadro = models.ForeignKey(Quadros, null=True, blank=True, on_delete=models.SET_NULL, related_name='pagamentos_quadro')

    def __str__(self):
        return f"Pagamento de {self.usuario} - Status: {self.status}"

    class Meta:
        verbose_name = 'Pagamento PIX'
        verbose_name_plural = 'Pagamentos PIX'
        ordering = ['-data_pagamento']

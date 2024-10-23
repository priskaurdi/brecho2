from django.contrib import admin
from .models import PagamentoPIX

class PagamentoPIXAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'valor_total', 'status', 'data_pagamento')
    list_filter = ('status', 'data_pagamento')
    search_fields = ('usuario__email', 'status', 'usuario__username', 'chave_pix')  # Pesquisa por email do usuário e status

admin.site.register(PagamentoPIX, PagamentoPIXAdmin)
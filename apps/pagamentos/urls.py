from django.urls import path
from .views import pagamentos_historico, pagamento_detalhes, pagamento_confirmado, pix_webhook, processar_pagamento

urlpatterns = [
    path('webhook/pix/', pix_webhook, name='pix_webhook'),
    path('pagamentos/', pagamentos_historico, name='pagamentos_historico'),
    path('pagamentos/<int:pagamento_id>/', pagamento_detalhes, name='pagamento_detalhes'),
    path('pagamento-confirmado/<int:pagamento_id>/', pagamento_confirmado, name='pagamento_confirmado'),
    path('processar-pagamento/<int:item_id>/<str:tipo_item>/', processar_pagamento, name='processar_pagamento'),
]
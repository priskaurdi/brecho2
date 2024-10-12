# apps/pagamentos/mercadopago_helper.py

import mercadopago
from django.conf import settings

def gerar_link_pagamento(item, item_tipo, usuario):
    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
    
    # Dados do pagamento
    payment_data = {
        "items": [{
            "id": str(item.id),
            "title": f"{item_tipo}: {item}",
            "quantity": 1,
            "currency_id": "BRL",  # Ajuste para o seu país
            "unit_price": float(item.valor)
        }],
        "payer": {
            "email": usuario.email
        },
        "back_urls": {
            "success": "https://seusite.com/pagamento-confirmado/",
            "failure": "https://seusite.com/compra-erro/",
            "pending": "https://seusite.com/compra-pendente/"
        },
        "auto_return": "approved"
    }
    
    # Cria a preferência de pagamento
    preference_response = sdk.preference().create(payment_data)
    
    # Obtém o link para iniciar o pagamento
    #init_point = preference_response["response"]["init_point"]
    
    return "https://www.mercadopago.com/payment_link_for_item"

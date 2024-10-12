from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import json
from .models import PagamentoPIX
from django.shortcuts import render, redirect
from catalogo.models import Catalogo
from quadros.models import Quadros
from .mercadopago_helper import gerar_link_pagamento



@csrf_exempt
@login_required  # Exige que o usuário esteja autenticado
def pix_webhook(request):
    if request.method == 'POST':
        try:
            # Carrega o JSON do corpo da requisição
            data = json.loads(request.body)
            user = request.user  # Obtém o usuário autenticado

            # Cria um novo pagamento baseado nos dados recebidos
            pagamento = PagamentoPIX.objects.create(
                user=user,
                valor=data.get('valor'),
                status=data.get('status'),
                chave_pix=data.get('chave_pix')
            )
            
            # Envia um e-mail de notificação para o usuário
            send_mail(
                'Confirmação de Pagamento PIX',
                f'Olá {user.username}, seu pagamento de {pagamento.valor} foi confirmado com sucesso!',
                'noreply@seusite.com',  # De
                [user.email],           # Para
                fail_silently=False,
            )
            
            return JsonResponse({"status": "success"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Method not allowed"}, status=405)


# apps/pagamentos/views.py

@csrf_exempt
def mercadopago_webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Aqui você pode processar o pagamento, verificando o status e outros detalhes.
        # A documentação da Mercado Pago explica o que será enviado no webhook.

        return JsonResponse({"status": "success"}, status=200)
    
    return JsonResponse({"error": "Método não permitido"}, status=405)



@login_required
def pagamentos_historico(request):
    pagamentos = PagamentoPIX.objects.filter(user=request.user)
    return render(request, 'pagamentos_historico.html', {'pagamentos': pagamentos})

@login_required
def pagamento_detalhes(request, pagamento_id):
    pagamento = PagamentoPIX.objects.get(id=pagamento_id, user=request.user)
    return render(request, 'pagamento_detalhes.html', {'pagamento': pagamento})

@login_required
def pagamento_confirmado(request, pagamento_id):
    pagamento = PagamentoPIX.objects.get(id=pagamento_id, user=request.user)
    return render(request, 'pagamento_confirmado.html', {'pagamento': pagamento})

@login_required
def processar_pagamento(request, item_id, tipo_item):
    # Verificar se o item é um produto ou um quadro
    try:
        if tipo_item == 'produto':
            item = get_object_or_404(Catalogo, id=item_id)
            valor = item.valor
        elif tipo_item == 'quadro':
            item = get_object_or_404(Quadros, id=item_id)
            valor = item.valor
        else:
            return render(request, 'pagamento_erro.html', {'mensagem': 'Tipo de item inválido'})

        # Criar um pagamento pendente no banco de dados
        pagamento = PagamentoPIX.objects.create(
            usuario=request.user,
            chave_pix="chave_pix_exemplo",  # Esta chave seria dinâmica com base na lógica de pagamento real
            valor_total=valor,
            status='pendente',
            produto=item if tipo_item == 'produto' else None,
            quadro=item if tipo_item == 'quadro' else None
        )

        # Gerar o link de pagamento do Mercado Pago
        link_pagamento = gerar_link_pagamento(item, tipo_item, request.user)

        # Redirecionar para o link de pagamento gerado
        return redirect(link_pagamento)
    
    except Catalogo.DoesNotExist:
        return render(request, 'pagamento_erro.html', {'mensagem': 'Produto não encontrado'})
    
    except Quadros.DoesNotExist:
        return render(request, 'pagamento_erro.html', {'mensagem': 'Quadro não encontrado'})

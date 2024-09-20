from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import json
from .models import PagamentoPIX
from django.shortcuts import render, redirect
from catalogo.models import Catalogo
from quadros.models import Quadros



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
    if tipo_item == 'produto':
        item = Catalogo.objects.get(id=item_id)
        valor = item.valor
    elif tipo_item == 'quadro':
        item = Quadros.objects.get(id=item_id)
        valor = item.valor
    else:
        return render(request, 'pagamento_erro.html', {'mensagem': 'Tipo de item inválido'})

    # Criar um pagamento pendente
    pagamento = PagamentoPIX.objects.create(
        usuario=request.user,
        chave_pix="chave_pix_exemplo",  # Esta chave seria dinâmica com base na lógica de pagamento real
        valor_total=valor,
        status='pendente',
        produto=item if tipo_item == 'produto' else None,
        quadro=item if tipo_item == 'quadro' else None
    )

    # Redirecionar para uma página de confirmação ou para a etapa seguinte do pagamento
    return redirect('pagamento_confirmado', pagamento_id=pagamento.id)
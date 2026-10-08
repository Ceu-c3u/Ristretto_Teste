from django.shortcuts import render
from ristretto.models import (Cliente, Servico_Adicional, Canal, Duracao, Categoria, Evento, Social, Corporativo, Bebidas)
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction


# Create your views here.

def index(request):
    return render(request, 'index.html')

def orcamento(request):
    return render(request, 'orcamento.html')

def servicos(request):
    return render(request, 'servicos.html')

def sobre(request):
    return render(request, 'sobre.html')


def salvar_orcamento(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            with transaction.atomic():
                # Salva ou procura um cliente
                cliente, _ = Cliente.objects.get_or_create(
                    Email=data.get('email'),
                    defaults={
                        'nome': data.get('nome'),
                        'telefone': data.get('telefone')
                    }
                )

                # Salva os serviços addicionais
                servico = Servico_Adicional.objects.create(
                    drip_station=data.get('drip_station', False),
                    impressora=data.get('impressora', False)
                )

                # Salva como foi a descoberta da empresa
                canal_valor = data.get('canal')
                if not canal_valor:
                    canal_valor = Canal.OpcoesCanal.OUTRO
                canal = Canal.objects.create(descoberta=canal_valor)

                # Salva o dia e hora do evento
                data_termino = data.get('data_termino') if data.get('duracao') == 'DIAS' else data.get('data_inicio')
                duracao = Duracao.objects.create(
                    duracao=data.get('duracao', 'DIA'),
                    data_inicio=data.get('data_inicio'),
                    data_termino=data_termino,
                    hora_inicio=data.get('hora_inicio'),
                    hora_termino=data.get('hora_termino')
                )

                # salva se é social ou corporativo
                tipo_categoria = data.get('tipo', 'SOCIAL')
                categoria = Categoria.objects.create(categoria=tipo_categoria)

                # Salva os campos comuns do evento
                evento = Evento.objects.create(
                    endereco=data.get('endereco'),
                    num_convidados=int(data.get('num_convidados') or 0),
                    mensagem=data.get('mensagem'),
                    observacao=data.get('observacao'),
                    FK_Servico=servico,
                    FK_Canal=canal,
                    FK_Duracao=duracao,
                    FK_Categoria=categoria,
                    FK_Cliente=cliente
                )

                # Salva campos do Social
                if tipo_categoria == 'SOCIAL':
                    social_data = data.get('social', {})
                    Social.objects.create(
                        tipo_evento=social_data.get('tipo_evento', 'OUTRO'),
                        outro_evento=social_data.get('outro_evento'),
                        bebida_alcoolica=social_data.get('bebida_alcoolica', 'NAO'),
                        FK_Evento=evento
                    )
                # Salva campos do corporativo
                else:
                    corp_data = data.get('corporativo', {})
                    corporativo = Corporativo.objects.create(
                        tipo_evento=corp_data.get('tipo_evento', 'OUTRO'),
                        outro_evento=corp_data.get('outro_evento'),
                        estimativa_doses=int(corp_data.get('estimativa_doses') or 200),
                        mais_doses=corp_data.get('mais_doses'),
                        copos_personalizados=corp_data.get('copos_personalizados', False),
                        detalhes=corp_data.get('detalhes'),
                        FK_Evento=evento,
                    )
                    # Faz a lista de bebidas e adiciona a corporativo
                    lista_bebidas_codigos = corp_data.get('bebidas', [])
                    for codigo in lista_bebidas_codigos:
                        bebida_obj, _ = Bebidas.objects.get_or_create(bebidas=codigo)
                        corporativo.FK_Bebidas.add(bebida_obj)
            # manda o json se tudo tiver ok, se nao tiver não manda
            return JsonResponse({'ok': True})
        except Exception as e:
            return JsonResponse({'ok': False, 'erro': str(e)}, status=400)

    return JsonResponse({'ok': False, 'erro': 'Método não permitido.'}, status=405)
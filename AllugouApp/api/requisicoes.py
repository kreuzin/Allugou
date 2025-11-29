from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import transaction
from decimal import Decimal
from ..models import RequisicaoLocacao, OfertaLocacao, Locatario


@method_decorator(csrf_exempt, name='dispatch')
class CreateRequisicaoView(APIView):
    """criar requisição de locação"""
    
    @transaction.atomic
    def post(self, request):
        try:
            # checa se ta logado
            if not request.user.is_authenticated:
                return Response({
                    'success': False,
                    'message': 'usuário não autenticado.'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            # ve se eh locatário
            try:
                locatario = Locatario.objects.get(user=request.user.username)
            except Locatario.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'apenas locatários podem criar requisições.'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # extrair dados
            oferta_id = request.data.get('oferta_id')
            data_inicio = request.data.get('data_inicio')
            data_fim = request.data.get('data_fim')
            opcao_entrega = request.data.get('opcao_entrega', 'retirada')
            valor_frete = request.data.get('valor_frete', 0)
            valor_total = request.data.get('valor_total')
            
            # valida os dados
            if not all([oferta_id, data_inicio, data_fim, valor_total]):
                return Response({
                    'success': False,
                    'message': 'dados incompletos.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # pega a oferta
            try:
                oferta = OfertaLocacao.objects.get(id=oferta_id)
            except OfertaLocacao.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'oferta não encontrada.'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # manda criar a requisição
            requisicao = RequisicaoLocacao.objects.create(
                ofertaLocacao=oferta,
                locatario=locatario,
                dataInicioLocacao=data_inicio,
                dataFimLocacao=data_fim,
                valorTotal=Decimal(str(valor_total)),
                valorFrete=Decimal(str(valor_frete)),
                retiradaNoLocal=(opcao_entrega == 'retirada')
            )
            
            return Response({
                'success': True,
                'message': 'requisição criada com sucesso!',
                'requisicao_id': requisicao.id
            }, status=status.HTTP_201_CREATED)
            
        except ValueError as e:
            return Response({
                'success': False,
                'message': f'erro de validação: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            import traceback
            print(f"erro ao criar requisição: {str(e)}")
            print(f"traceback: {traceback.format_exc()}")
            return Response({
                'success': False,
                'message': f'erro ao criar requisição: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

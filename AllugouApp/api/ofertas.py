from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction, models
from ..models import OfertaLocacao, ImagemOferta, Locador, Endereco
from .serializers import OfertaLocacaoSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class CreateOfertaView(APIView):
    """endpoint para criar oferta de locação com múltiplas imagens"""
    parser_classes = (MultiPartParser, FormParser)
    
    @transaction.atomic
    def post(self, request):
        try:
            # checa se ta logado
            if not request.user.is_authenticated:
                return Response({
                    'success': False,
                    'message': 'usuário não autenticado.'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            # pega o locador desse user
            try:
                locador = Locador.objects.get(user=request.user.username)
            except Locador.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'apenas locadores podem criar ofertas.'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # pega os dados da oferta
            titulo = request.data.get('titulo')
            descricao = request.data.get('descricao')
            valor_diaria = request.data.get('valorDiaria')
            oferece_entrega = request.data.get('ofereceEntrega', 'false').lower() == 'true'
            
            # confere se preencheu tudo
            if not all([titulo, descricao, valor_diaria]):
                return Response({
                    'success': False,
                    'message': 'título, descrição e valor da diária são obrigatórios.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # usa o endereço do locador como local da oferta
            localizacao = locador.endereco
            
            # cria a oferta no banco
            oferta = OfertaLocacao.objects.create(
                locador=locador,
                localizacao=localizacao,
                titulo=titulo,
                descricao=descricao,
                valorDiaria=float(valor_diaria),
                ofereceEntrega=oferece_entrega
            )
            
            # salva as imagens
            imagens_files = request.FILES.getlist('imagens')
            imagem_principal_index = int(request.data.get('imagemPrincipalIndex', 0))
            
            if not imagens_files:
                return Response({
                    'success': False,
                    'message': 'pelo menos uma imagem é obrigatória.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            for index, imagem_file in enumerate(imagens_files):
                ImagemOferta.objects.create(
                    ofertaLocacao=oferta,
                    imagem=imagem_file,
                    ehImagemPrincipal=(index == imagem_principal_index),
                    ordem=index
                )
            
            # serializar resposta
            serializer = OfertaLocacaoSerializer(oferta)
            
            return Response({
                'success': True,
                'message': 'oferta criada com sucesso!',
                'oferta': serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except ValueError as e:
            return Response({
                'success': False,
                'message': f'erro de validação: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            import traceback
            print(f"erro ao criar oferta: {str(e)}")
            print(f"traceback: {traceback.format_exc()}")
            return Response({
                'success': False,
                'message': f'erro ao criar oferta: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class ListMyOfertasView(APIView):
    """listar ofertas do locador autenticado"""
    
    def get(self, request):
        try:
            if not request.user.is_authenticated:
                return Response({
                    'success': False,
                    'message': 'usuário não autenticado.'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            try:
                locador = Locador.objects.get(user=request.user.username)
            except Locador.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'apenas locadores podem ver ofertas.'
                }, status=status.HTTP_403_FORBIDDEN)
            
            ofertas = OfertaLocacao.objects.filter(locador=locador).prefetch_related('imagens')
            serializer = OfertaLocacaoSerializer(ofertas, many=True)
            
            return Response({
                'success': True,
                'ofertas': serializer.data
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'erro ao buscar ofertas: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class OfertaDetailView(APIView):
    """obter detalhes de uma oferta específica"""
    
    def get(self, request, oferta_id):
        try:
            oferta = OfertaLocacao.objects.prefetch_related('imagens').select_related('locador', 'localizacao').get(id=oferta_id)
            serializer = OfertaLocacaoSerializer(oferta)
            
            # info extra do locador
            locador_data = {
                'nome': oferta.locador.nome,
                'user': oferta.locador.user,
            }
            
            # onde fica
            localizacao_data = {
                'cidade': oferta.localizacao.cidade,
                'estado': oferta.localizacao.estado,
                'bairro': oferta.localizacao.bairro,
            }
            
            return Response({
                'success': True,
                'oferta': serializer.data,
                'locador': locador_data,
                'localizacao': localizacao_data
            })
            
        except OfertaLocacao.DoesNotExist:
            return Response({
                'success': False,
                'message': 'oferta não encontrada.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'erro ao buscar oferta: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class ListAllOfertasView(APIView):
    """listar todas as ofertas disponíveis (público)"""
    
    def get(self, request):
        try:
            ofertas = OfertaLocacao.objects.all().prefetch_related('imagens').select_related('locador', 'localizacao').order_by('-dataCriacao')
            serializer = OfertaLocacaoSerializer(ofertas, many=True)
            
            return Response({
                'success': True,
                'ofertas': serializer.data
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'erro ao buscar ofertas: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class EditOfertaView(APIView):
    """endpoint para editar oferta de locação"""
    parser_classes = (MultiPartParser, FormParser)
    
    @transaction.atomic
    def put(self, request, oferta_id):
        try:
            # checa se tá logado
            if not request.user.is_authenticated:
                return Response({
                    'success': False,
                    'message': 'usuário não autenticado.'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            # pega o locador desse usuário
            try:
                locador = Locador.objects.get(user=request.user.username)
            except Locador.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'apenas locadores podem editar ofertas.'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # pega a oferta
            try:
                oferta = OfertaLocacao.objects.get(id=oferta_id, locador=locador)
            except OfertaLocacao.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'oferta não encontrada ou você não tem permissão.'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # atualiza o que mudou
            titulo = request.data.get('titulo')
            descricao = request.data.get('descricao')
            valor_diaria = request.data.get('valorDiaria')
            oferece_entrega = request.data.get('ofereceEntrega', 'false').lower() == 'true'
            
            if titulo:
                oferta.titulo = titulo
            if descricao:
                oferta.descricao = descricao
            if valor_diaria:
                oferta.valorDiaria = float(valor_diaria)
            oferta.ofereceEntrega = oferece_entrega
            
            oferta.save()
            
            # processa as imagens novas se tiver
            imagens_files = request.FILES.getlist('imagens')
            remover_imagens = request.data.get('removerImagens', '')
            imagem_principal_id = request.data.get('imagemPrincipalId')
            
            # deleta as imagens que marcou pra remover
            if remover_imagens:
                ids_remover = [int(id) for id in remover_imagens.split(',') if id]
                ImagemOferta.objects.filter(id__in=ids_remover, ofertaLocacao=oferta).delete()
            
            # adiciona as imagens novas
            if imagens_files:
                # descobre qual a maior ordem pra continuar a partir dela
                max_ordem = oferta.imagens.aggregate(max_ordem=models.Max('ordem'))['max_ordem'] or -1
                
                for index, imagem_file in enumerate(imagens_files):
                    ImagemOferta.objects.create(
                        ofertaLocacao=oferta,
                        imagem=imagem_file,
                        ehImagemPrincipal=False,
                        ordem=max_ordem + index + 1
                    )
            
            # muda qual é a imagem principal
            if imagem_principal_id:
                # tira o flag de principal das outras
                oferta.imagens.update(ehImagemPrincipal=False)
                # marca a nova como principal
                oferta.imagens.filter(id=int(imagem_principal_id)).update(ehImagemPrincipal=True)
            
            # monta a resposta
            oferta.refresh_from_db()
            serializer = OfertaLocacaoSerializer(oferta)
            
            return Response({
                'success': True,
                'message': 'oferta atualizada com sucesso!',
                'oferta': serializer.data
            })
            
        except ValueError as e:
            return Response({
                'success': False,
                'message': f'erro de validação: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            import traceback
            print(f"erro ao editar oferta: {str(e)}")
            print(f"traceback: {traceback.format_exc()}")
            return Response({
                'success': False,
                'message': f'erro ao editar oferta: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class DeleteOfertaView(APIView):
    """endpoint para excluir oferta de locação"""
    
    @transaction.atomic
    def delete(self, request, oferta_id):
        try:
            # checa se tá logado
            if not request.user.is_authenticated:
                return Response({
                    'success': False,
                    'message': 'usuário não autenticado.'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            # pega o locador desse usuário
            try:
                locador = Locador.objects.get(user=request.user.username)
            except Locador.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'apenas locadores podem excluir ofertas.'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # pega a oferta q vai ser deletada
            try:
                oferta = OfertaLocacao.objects.get(id=oferta_id, locador=locador)
            except OfertaLocacao.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'oferta não encontrada ou você não tem permissão.'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # não deixa deletar se tiver locação em andamento
            from ..models import Locacao
            locacoes_ativas = Locacao.objects.filter(
                requisicaoLocacao__ofertaLocacao=oferta,
                status__in=['ativa', 'em_uso', 'devolvida']
            ).exists()
            
            if locacoes_ativas:
                return Response({
                    'success': False,
                    'message': 'não é possível excluir uma oferta com locações em andamento.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # deleta as imagens primeiro por garantia
            oferta.imagens.all().delete()
            
            # agora sim deleta a oferta
            oferta.delete()
            
            return Response({
                'success': True,
                'message': 'oferta excluída com sucesso!'
            })
            
        except Exception as e:
            import traceback
            print(f"erro ao excluir oferta: {str(e)}")
            print(f"traceback: {traceback.format_exc()}")
            return Response({
                'success': False,
                'message': f'erro ao excluir oferta: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

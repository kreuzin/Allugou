from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Count
from ..models import RequisicaoLocacao, Locador, Locatario, OfertaLocacao, Mensagem


class NotificacoesLocadorView(APIView):
    """
    lista requisições feitas para ofertas do locador logado
    """
    def get(self, request):
        locador_id = request.session.get('locador_id')
        
        if not locador_id:
            return Response({
                'success': False,
                'message': 'Você precisa estar logado como locador'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            locador = Locador.objects.get(id=locador_id)
        except Locador.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Locador não encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # pega todas as requisições para ofertas deste locador
        requisicoes = RequisicaoLocacao.objects.filter(
            ofertaLocacao__locador=locador
        ).select_related(
            'ofertaLocacao', 
            'locatario',
            'locacao'  # inclui locação se existir
        ).prefetch_related('ofertaLocacao__imagens')
        
        # conta requisições não lidas
        nao_lidas = requisicoes.filter(vistoPeloLocador=False).count()
        
        # pega mensagens não lidas (enviadas por locatários para este locador)
        mensagens_nao_lidas_qs = Mensagem.objects.filter(
            requisicao__ofertaLocacao__locador_id=locador_id,
            remetente='locatario',
            lido=False
        ).select_related(
            'requisicao',
            'requisicao__ofertaLocacao',
            'requisicao__locatario',
            'requisicao__locacao'
        ).prefetch_related('requisicao__ofertaLocacao__imagens').order_by('-enviadoEm')[:10]
        
        # monta dados das mensagens não lidas
        mensagens_data = []
        for msg in mensagens_nao_lidas_qs:
            req = msg.requisicao
            imagem_principal = req.ofertaLocacao.imagens.filter(ehImagemPrincipal=True).first()
            imagem_url = imagem_principal.imagem.url if imagem_principal else None
            
            # ve se tem locacao
            locacao_id = None
            try:
                if hasattr(req, 'locacao') and req.locacao:
                    locacao_id = req.locacao.id
            except:
                pass
            
            mensagens_data.append({
                'id': msg.id,
                'texto': msg.texto[:50] + '...' if len(msg.texto) > 50 else msg.texto,
                'enviadoEm': msg.enviadoEm.isoformat(),
                'remetente': msg.remetente,
                'remetenteNome': req.locatario.nome,
                'requisicaoId': req.id,
                'locacaoId': locacao_id,
                'oferta': {
                    'id': req.ofertaLocacao.id,
                    'titulo': req.ofertaLocacao.titulo,
                    'imagemPrincipal': imagem_url
                }
            })
        
        mensagens_nao_lidas_count = Mensagem.objects.filter(
            requisicao__ofertaLocacao__locador_id=locador_id,
            remetente='locatario',
            lido=False
        ).count()
        
        # monta os dados pra retornar
        requisicoes_data = []
        for req in requisicoes:
            # pega imagem principal da oferta
            imagem_principal = req.ofertaLocacao.imagens.filter(ehImagemPrincipal=True).first()
            imagem_url = imagem_principal.imagem.url if imagem_principal else None
            
            # ve se tem locacao ja criada (foi pago)
            locacao_id = None
            locacao_status = None
            try:
                if hasattr(req, 'locacao') and req.locacao:
                    locacao_id = req.locacao.id
                    locacao_status = req.locacao.status
            except:
                pass
            
            requisicoes_data.append({
                'id': req.id,
                'dataCriacao': req.dataCriacao.isoformat(),
                'dataInicioLocacao': req.dataInicioLocacao.isoformat(),
                'valorTotal': str(req.valorTotal),
                'valorFrete': str(req.valorFrete),
                'retiradaNoLocal': req.retiradaNoLocal,
                'vistoPeloLocador': req.vistoPeloLocador,
                'status': req.status,
                'locacaoId': locacao_id,
                'locacaoStatus': locacao_status,
                'oferta': {
                    'id': req.ofertaLocacao.id,
                    'titulo': req.ofertaLocacao.titulo,
                    'valorDiaria': req.ofertaLocacao.valorDiaria,
                    'imagemPrincipal': imagem_url
                },
                'locatario': {
                    'id': req.locatario.id,
                    'nome': req.locatario.nome,
                    'email': req.locatario.email,
                    'tel': req.locatario.tel
                }
            })
        
        return Response({
            'success': True,
            'naoLidas': nao_lidas,
            'mensagensNaoLidas': mensagens_nao_lidas_count,
            'mensagens': mensagens_data,
            'requisicoes': requisicoes_data
        })


class NotificacoesLocatarioView(APIView):
    """
    lista requisições feitas pelo locatário logado
    """
    def get(self, request):
        locatario_id = request.session.get('locatario_id')
        
        if not locatario_id:
            return Response({
                'success': False,
                'message': 'Você precisa estar logado como locatário'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            locatario = Locatario.objects.get(id=locatario_id)
        except Locatario.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Locatário não encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # pega todas as requisições do locatário
        requisicoes = RequisicaoLocacao.objects.filter(
            locatario=locatario
        ).select_related(
            'ofertaLocacao', 
            'ofertaLocacao__locador',
            'locacao'  # inclui locação se existir
        ).prefetch_related('ofertaLocacao__imagens')
        
        # pega mensagens não lidas (enviadas por locadores para este locatário)
        mensagens_nao_lidas_qs = Mensagem.objects.filter(
            requisicao__locatario_id=locatario_id,
            remetente='locador',
            lido=False
        ).select_related(
            'requisicao',
            'requisicao__ofertaLocacao',
            'requisicao__ofertaLocacao__locador',
            'requisicao__locacao'
        ).prefetch_related('requisicao__ofertaLocacao__imagens').order_by('-enviadoEm')[:10]
        
        # monta dados das mensagens não lidas
        mensagens_data = []
        for msg in mensagens_nao_lidas_qs:
            req = msg.requisicao
            imagem_principal = req.ofertaLocacao.imagens.filter(ehImagemPrincipal=True).first()
            imagem_url = imagem_principal.imagem.url if imagem_principal else None
            
            # ve se tem locacao
            locacao_id = None
            try:
                if hasattr(req, 'locacao') and req.locacao:
                    locacao_id = req.locacao.id
            except:
                pass
            
            mensagens_data.append({
                'id': msg.id,
                'texto': msg.texto[:50] + '...' if len(msg.texto) > 50 else msg.texto,
                'enviadoEm': msg.enviadoEm.isoformat(),
                'remetente': msg.remetente,
                'remetenteNome': req.ofertaLocacao.locador.nome,
                'requisicaoId': req.id,
                'locacaoId': locacao_id,
                'oferta': {
                    'id': req.ofertaLocacao.id,
                    'titulo': req.ofertaLocacao.titulo,
                    'imagemPrincipal': imagem_url
                }
            })
        
        mensagens_nao_lidas_count = Mensagem.objects.filter(
            requisicao__locatario_id=locatario_id,
            remetente='locador',
            lido=False
        ).count()
        
        # monta os dados pra retornar
        requisicoes_data = []
        for req in requisicoes:
            imagem_principal = req.ofertaLocacao.imagens.filter(ehImagemPrincipal=True).first()
            imagem_url = imagem_principal.imagem.url if imagem_principal else None
            
            # ve se ja criou locacao (pagou)
            locacao_id = None
            locacao_status = None
            try:
                if hasattr(req, 'locacao') and req.locacao:
                    locacao_id = req.locacao.id
                    locacao_status = req.locacao.status
            except:
                pass
            
            requisicoes_data.append({
                'id': req.id,
                'dataCriacao': req.dataCriacao.isoformat(),
                'dataInicioLocacao': req.dataInicioLocacao.isoformat(),
                'valorTotal': str(req.valorTotal),
                'valorFrete': str(req.valorFrete),
                'retiradaNoLocal': req.retiradaNoLocal,
                'status': req.status,
                'locacaoId': locacao_id,
                'locacaoStatus': locacao_status,
                'oferta': {
                    'id': req.ofertaLocacao.id,
                    'titulo': req.ofertaLocacao.titulo,
                    'valorDiaria': req.ofertaLocacao.valorDiaria,
                    'imagemPrincipal': imagem_url
                },
                'locador': {
                    'id': req.ofertaLocacao.locador.id,
                    'nome': req.ofertaLocacao.locador.nome
                }
            })
        
        return Response({
            'success': True,
            'mensagensNaoLidas': mensagens_nao_lidas_count,
            'mensagens': mensagens_data,
            'requisicoes': requisicoes_data
        })


class MarcarRequisicaoVistaView(APIView):
    """
    marca uma requisição como vista pelo locador
    """
    def post(self, request, requisicao_id):
        locador_id = request.session.get('locador_id')
        
        if not locador_id:
            return Response({
                'success': False,
                'message': 'Não autorizado'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            requisicao = RequisicaoLocacao.objects.get(
                id=requisicao_id,
                ofertaLocacao__locador_id=locador_id
            )
            requisicao.vistoPeloLocador = True
            requisicao.save()
            
            return Response({
                'success': True,
                'message': 'Requisição marcada como vista'
            })
        except RequisicaoLocacao.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Requisição não encontrada'
            }, status=status.HTTP_404_NOT_FOUND)


class RequisicaoDetailView(APIView):
    """
    retorna detalhes de uma requisição específica
    só o locador da oferta ou locatario da requisição podem ver
    """
    def get(self, request, requisicao_id):
        locador_id = request.session.get('locador_id')
        locatario_id = request.session.get('locatario_id')
        
        print(f"[debug] RequisicaoDetail - locador_id: {locador_id}, locatario_id: {locatario_id}")
        
        if not locador_id and not locatario_id:
            return Response({
                'success': False,
                'message': 'Não autorizado'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            requisicao = RequisicaoLocacao.objects.select_related(
                'ofertaLocacao', 
                'ofertaLocacao__locador',
                'ofertaLocacao__localizacao',
                'locatario',
                'locatario__endereco'
            ).prefetch_related('ofertaLocacao__imagens', 'mensagens').get(id=requisicao_id)
        except RequisicaoLocacao.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Requisição não encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # checa se pode ver
        eh_locador = bool(locador_id) and int(requisicao.ofertaLocacao.locador_id) == int(locador_id)
        eh_locatario = bool(locatario_id) and int(requisicao.locatario_id) == int(locatario_id)
        
        print(f"[debug] eh_locador: {eh_locador}, eh_locatario: {eh_locatario}")
        print(f"[debug] req.oferta.locador_id: {requisicao.ofertaLocacao.locador_id}, req.locatario_id: {requisicao.locatario_id}")
        
        if not eh_locador and not eh_locatario:
            return Response({
                'success': False,
                'message': 'Você não tem permissão para ver esta requisição'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # se é locador vendo, marca como visto
        if eh_locador and not requisicao.vistoPeloLocador:
            requisicao.vistoPeloLocador = True
            requisicao.save()
        
        # marca mensagens do outro usuário como lidas
        if eh_locador:
            # locador visualizou, marca mensagens do locatário como lidas
            Mensagem.objects.filter(
                requisicao=requisicao,
                remetente='locatario',
                lido=False
            ).update(lido=True)
        elif eh_locatario:
            # locatário visualizou, marca mensagens do locador como lidas
            Mensagem.objects.filter(
                requisicao=requisicao,
                remetente='locador',
                lido=False
            ).update(lido=True)
        
        # pega imagens da oferta
        imagens = []
        for img in requisicao.ofertaLocacao.imagens.all():
            imagens.append({
                'id': img.id,
                'url': img.imagem.url,
                'ehPrincipal': img.ehImagemPrincipal
            })
        
        # pega mensagens
        mensagens = []
        for msg in requisicao.mensagens.all():
            mensagens.append({
                'id': msg.id,
                'remetente': msg.remetente,
                'texto': msg.texto,
                'enviadoEm': msg.enviadoEm.isoformat(),
                'lido': msg.lido
            })
        
        # dados do locatário
        locatario_data = {
            'id': requisicao.locatario.id,
            'nome': requisicao.locatario.nome,
            'email': requisicao.locatario.email,
            'tel': requisicao.locatario.tel,
            'endereco': None
        }
        if requisicao.locatario.endereco:
            locatario_data['endereco'] = {
                'rua': requisicao.locatario.endereco.rua,
                'numero': requisicao.locatario.endereco.numero,
                'bairro': requisicao.locatario.endereco.bairro,
                'cidade': requisicao.locatario.endereco.cidade,
                'estado': requisicao.locatario.endereco.estado
            }
        
        # dados da oferta
        localizacao = requisicao.ofertaLocacao.localizacao
        oferta_data = {
            'id': requisicao.ofertaLocacao.id,
            'titulo': requisicao.ofertaLocacao.titulo,
            'descricao': requisicao.ofertaLocacao.descricao,
            'valorDiaria': requisicao.ofertaLocacao.valorDiaria,
            'ofereceEntrega': requisicao.ofertaLocacao.ofereceEntrega,
            'imagens': imagens,
            'localizacao': f"{localizacao.bairro}, {localizacao.cidade} - {localizacao.estado}" if localizacao else None,
            'locador': {
                'id': requisicao.ofertaLocacao.locador.id,
                'nome': requisicao.ofertaLocacao.locador.nome,
                'tel': requisicao.ofertaLocacao.locador.tel
            }
        }
        
        # ve se tem locacao associada
        locacao_id = None
        try:
            if hasattr(requisicao, 'locacao'):
                locacao_id = requisicao.locacao.id
        except:
            pass
        
        return Response({
            'success': True,
            'requisicao': {
                'id': requisicao.id,
                'dataCriacao': requisicao.dataCriacao.isoformat(),
                'dataInicioLocacao': requisicao.dataInicioLocacao.isoformat(),
                'dataFimLocacao': requisicao.dataFimLocacao.isoformat() if requisicao.dataFimLocacao else None,
                'valorTotal': str(requisicao.valorTotal),
                'valorFrete': str(requisicao.valorFrete),
                'retiradaNoLocal': requisicao.retiradaNoLocal,
                'status': requisicao.status,
                'vistoPeloLocador': requisicao.vistoPeloLocador,
                'oferta': oferta_data,
                'locatario': locatario_data,
                'mensagens': mensagens,
                'locacaoId': locacao_id
            },
            'ehLocador': eh_locador,
            'ehLocatario': eh_locatario
        })


class AtualizarStatusRequisicaoView(APIView):
    """
    permite ao locador aceitar ou recusar uma requisição
    """
    def post(self, request, requisicao_id):
        locador_id = request.session.get('locador_id')
        
        if not locador_id:
            return Response({
                'success': False,
                'message': 'Não autorizado'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        novo_status = request.data.get('status')
        if novo_status not in ['aceita', 'recusada']:
            return Response({
                'success': False,
                'message': 'Status inválido'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            requisicao = RequisicaoLocacao.objects.get(
                id=requisicao_id,
                ofertaLocacao__locador_id=locador_id
            )
            requisicao.status = novo_status
            requisicao.save()
            
            return Response({
                'success': True,
                'message': f'Requisição {novo_status} com sucesso',
                'status': novo_status
            })
        except RequisicaoLocacao.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Requisição não encontrada'
            }, status=status.HTTP_404_NOT_FOUND)


class EnviarMensagemView(APIView):
    """
    envia uma mensagem na conversa da requisição
    """
    def post(self, request, requisicao_id):
        from ..models import Mensagem
        
        locador_id = request.session.get('locador_id')
        locatario_id = request.session.get('locatario_id')
        
        print(f"[debug] EnviarMensagem - locador_id: {locador_id}, locatario_id: {locatario_id}")
        
        if not locador_id and not locatario_id:
            return Response({
                'success': False,
                'message': 'Não autorizado'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        texto = request.data.get('texto', '').strip()
        if not texto:
            return Response({
                'success': False,
                'message': 'Mensagem não pode estar vazia'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            requisicao = RequisicaoLocacao.objects.select_related(
                'ofertaLocacao__locador'
            ).get(id=requisicao_id)
        except RequisicaoLocacao.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Requisição não encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # checa permissao e define quem ta mandando
        eh_locador = bool(locador_id) and int(requisicao.ofertaLocacao.locador_id) == int(locador_id)
        eh_locatario = bool(locatario_id) and int(requisicao.locatario_id) == int(locatario_id)
        
        print(f"[debug] EnviarMensagem - eh_locador: {eh_locador}, eh_locatario: {eh_locatario}")
        
        if not eh_locador and not eh_locatario:
            return Response({
                'success': False,
                'message': 'Você não tem permissão'
            }, status=status.HTTP_403_FORBIDDEN)
        
        remetente = 'locador' if eh_locador else 'locatario'
        print(f"[debug] EnviarMensagem - remetente definido: {remetente}")
        
        mensagem = Mensagem.objects.create(
            requisicao=requisicao,
            remetente=remetente,
            texto=texto
        )
        
        return Response({
            'success': True,
            'mensagem': {
                'id': mensagem.id,
                'remetente': mensagem.remetente,
                'texto': mensagem.texto,
                'enviadoEm': mensagem.enviadoEm.isoformat(),
                'lido': mensagem.lido
            }
        })

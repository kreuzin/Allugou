from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
from ..models import RequisicaoLocacao, Locacao, Locatario, Locador, Mensagem


@method_decorator(csrf_exempt, name='dispatch')
class PagarRequisicaoView(APIView):
    """
    Locatário paga a requisição aceita.
    Isso cria uma Locação no banco de dados.
    """
    def post(self, request, requisicao_id):
        locatario_id = request.session.get('locatario_id')
        
        if not locatario_id:
            return Response({
                'success': False,
                'message': 'você precisa estar logado como locatário'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            requisicao = RequisicaoLocacao.objects.select_related(
                'ofertaLocacao', 
                'locatario',
                'locatario__endereco'
            ).get(id=requisicao_id)
        except RequisicaoLocacao.DoesNotExist:
            return Response({
                'success': False,
                'message': 'requisição não encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if requisicao.locatario_id != int(locatario_id):
            return Response({
                'success': False,
                'message': 'você não tem permissão'
            }, status=status.HTTP_403_FORBIDDEN)
        
        if requisicao.status != 'aceita':
            return Response({
                'success': False,
                'message': 'a requisição precisa estar aceita para pagar'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # checa se já tem locação pra essa requisição
        if hasattr(requisicao, 'locacao'):
            return Response({
                'success': False,
                'message': 'já existe uma locação para esta requisição'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # manda criar a locacao no banco
        locacao = Locacao.objects.create(
            requisicaoLocacao=requisicao,
            enderecoEntrega=requisicao.locatario.endereco if not requisicao.retiradaNoLocal else None,
            titulo=requisicao.ofertaLocacao.titulo,
            descricao=requisicao.ofertaLocacao.descricao[:255],
            valorTotal=requisicao.valorTotal,
            valorFrete=requisicao.valorFrete,
            retiradaNoLocal=requisicao.retiradaNoLocal,
            # datas que o locatário escolheu na requisição
            dataInicioPrevista=requisicao.dataInicioLocacao,
            dataFimPrevista=requisicao.dataFimLocacao,
            # essas datas são preenchidas conforme o fluxo rola
            dataInicioReal=None,  # preenche quando locatário confirmar que pegou
            dataFimReal=None,     # preenche quando locador confirmar devolução
            status='ativa'
        )
        
        return Response({
            'success': True,
            'message': 'Pagamento realizado! Locação iniciada.',
            'locacao_id': locacao.id
        })


@method_decorator(csrf_exempt, name='dispatch')
class LocacaoDetailView(APIView):
    """
    Retorna detalhes de uma locação específica.
    """
    def get(self, request, locacao_id):
        locador_id = request.session.get('locador_id')
        locatario_id = request.session.get('locatario_id')
        
        if not locador_id and not locatario_id:
            return Response({
                'success': False,
                'message': 'Não autorizado'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            locacao = Locacao.objects.select_related(
                'requisicaoLocacao',
                'requisicaoLocacao__ofertaLocacao',
                'requisicaoLocacao__ofertaLocacao__locador',
                'requisicaoLocacao__ofertaLocacao__localizacao',
                'requisicaoLocacao__locatario',
                'requisicaoLocacao__locatario__endereco',
                'enderecoEntrega'
            ).prefetch_related(
                'requisicaoLocacao__ofertaLocacao__imagens',
                'requisicaoLocacao__mensagens'
            ).get(id=locacao_id)
        except Locacao.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Locação não encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # checa se pode ver
        eh_locador = bool(locador_id) and int(locacao.locador.id) == int(locador_id)
        eh_locatario = bool(locatario_id) and int(locacao.locatario.id) == int(locatario_id)
        
        if not eh_locador and not eh_locatario:
            return Response({
                'success': False,
                'message': 'Você não tem permissão para ver esta locação'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # marca as mensagens do outro como lidas
        if eh_locador:
            Mensagem.objects.filter(
                requisicao=locacao.requisicaoLocacao,
                remetente='locatario',
                lido=False
            ).update(lido=True)
        elif eh_locatario:
            Mensagem.objects.filter(
                requisicao=locacao.requisicaoLocacao,
                remetente='locador',
                lido=False
            ).update(lido=True)
        
        # pega as imagens da oferta
        imagens = []
        for img in locacao.oferta.imagens.all():
            imagens.append({
                'id': img.id,
                'url': img.imagem.url,
                'ehPrincipal': img.ehImagemPrincipal
            })
        
        # pega o histórico de mensagens
        mensagens = []
        for msg in locacao.requisicaoLocacao.mensagens.all():
            mensagens.append({
                'id': msg.id,
                'remetente': msg.remetente,
                'texto': msg.texto,
                'enviadoEm': msg.enviadoEm.isoformat(),
                'lido': msg.lido
            })
        
        # monta os dados do locatário
        locatario_data = {
            'id': locacao.locatario.id,
            'nome': locacao.locatario.nome,
            'email': locacao.locatario.email,
            'tel': locacao.locatario.tel,
            'endereco': None
        }
        if locacao.locatario.endereco:
            locatario_data['endereco'] = {
                'rua': locacao.locatario.endereco.rua,
                'numero': locacao.locatario.endereco.numero,
                'bairro': locacao.locatario.endereco.bairro,
                'cidade': locacao.locatario.endereco.cidade,
                'estado': locacao.locatario.endereco.estado
            }
        
        # monta os dados do locador
        locador_data = {
            'id': locacao.locador.id,
            'nome': locacao.locador.nome,
            'email': locacao.locador.email,
            'tel': locacao.locador.tel
        }
        
        # pega onde fica a oferta
        localizacao = locacao.oferta.localizacao
        
        return Response({
            'success': True,
            'locacao': {
                'id': locacao.id,
                'titulo': locacao.titulo,
                'descricao': locacao.descricao,
                'status': locacao.status,
                'valorTotal': str(locacao.valorTotal),
                'valorFrete': str(locacao.valorFrete),
                'retiradaNoLocal': locacao.retiradaNoLocal,
                # datas planejadas pelo locatário
                'dataInicioPrevista': locacao.dataInicioPrevista.isoformat(),
                'dataFimPrevista': locacao.dataFimPrevista.isoformat() if locacao.dataFimPrevista else None,
                # datas de quando realmente rolou
                'dataInicioReal': locacao.dataInicioReal.isoformat() if locacao.dataInicioReal else None,
                'dataFimReal': locacao.dataFimReal.isoformat() if locacao.dataFimReal else None,
                # outras datas do processo
                'dataCriacao': locacao.dataCriacao.isoformat(),
                'dataPagamento': locacao.dataPagamento.isoformat() if locacao.dataPagamento else None,
                'locatarioConfirmouRecebimento': locacao.locatarioConfirmouRecebimento,
                'dataConfirmacaoRecebimento': locacao.dataConfirmacaoRecebimento.isoformat() if locacao.dataConfirmacaoRecebimento else None,
                'fotoDevolucao': locacao.fotoDevolucao.url if locacao.fotoDevolucao else None,
                'dataDevolucao': locacao.dataDevolucao.isoformat() if locacao.dataDevolucao else None,
                'locadorConfirmouDevolucao': locacao.locadorConfirmouDevolucao,
                'dataConfirmacaoDevolucao': locacao.dataConfirmacaoDevolucao.isoformat() if locacao.dataConfirmacaoDevolucao else None,
                'dataConclusao': locacao.dataConclusao.isoformat() if locacao.dataConclusao else None,
                'oferta': {
                    'id': locacao.oferta.id,
                    'titulo': locacao.oferta.titulo,
                    'valorDiaria': locacao.oferta.valorDiaria,
                    'imagens': imagens,
                    'localizacao': f"{localizacao.bairro}, {localizacao.cidade} - {localizacao.estado}" if localizacao else None,
                },
                'locador': locador_data,
                'locatario': locatario_data,
                'mensagens': mensagens,
                'requisicaoId': locacao.requisicaoLocacao.id
            },
            'ehLocador': eh_locador,
            'ehLocatario': eh_locatario
        })


@method_decorator(csrf_exempt, name='dispatch')
class ConfirmarRecebimentoView(APIView):
    """
    Locatário confirma que recebeu o produto.
    """
    def post(self, request, locacao_id):
        locatario_id = request.session.get('locatario_id')
        
        if not locatario_id:
            return Response({
                'success': False,
                'message': 'você precisa estar logado como locatário'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            locacao = Locacao.objects.select_related('requisicaoLocacao').get(id=locacao_id)
        except Locacao.DoesNotExist:
            return Response({
                'success': False,
                'message': 'locação não encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if locacao.locatario.id != int(locatario_id):
            return Response({
                'success': False,
                'message': 'você não tem permissão'
            }, status=status.HTTP_403_FORBIDDEN)
        
        if locacao.status != 'ativa':
            return Response({
                'success': False,
                'message': 'a locação precisa estar ativa'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        locacao.status = 'em_uso'
        locacao.locatarioConfirmouRecebimento = True
        locacao.dataConfirmacaoRecebimento = timezone.now()
        # a locação começa de verdade quando o locatário confirma que pegou
        locacao.dataInicioReal = timezone.now()
        locacao.save()
        
        return Response({
            'success': True,
            'message': 'Recebimento confirmado!',
            'status': locacao.status
        })


@method_decorator(csrf_exempt, name='dispatch')
class EnviarFotoDevolucaoView(APIView):
    """
    Locatário envia foto do produto devolvido.
    """
    def post(self, request, locacao_id):
        locatario_id = request.session.get('locatario_id')
        
        if not locatario_id:
            return Response({
                'success': False,
                'message': 'você precisa estar logado como locatário'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            locacao = Locacao.objects.select_related('requisicaoLocacao').get(id=locacao_id)
        except Locacao.DoesNotExist:
            return Response({
                'success': False,
                'message': 'locação não encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if locacao.locatario.id != int(locatario_id):
            return Response({
                'success': False,
                'message': 'você não tem permissão'
            }, status=status.HTTP_403_FORBIDDEN)
        
        if locacao.status != 'em_uso':
            return Response({
                'success': False,
                'message': 'a locação precisa estar em uso'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        foto = request.FILES.get('foto')
        if not foto:
            return Response({
                'success': False,
                'message': 'envie uma foto'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        locacao.status = 'devolvida'
        locacao.fotoDevolucao = foto
        locacao.dataDevolucao = timezone.now()
        locacao.save()
        
        return Response({
            'success': True,
            'message': 'Foto de devolução enviada!',
            'status': locacao.status,
            'foto_url': locacao.fotoDevolucao.url if locacao.fotoDevolucao else None
        })


@method_decorator(csrf_exempt, name='dispatch')
class ConfirmarDevolucaoView(APIView):
    """
    Locador confirma que recebeu o produto de volta.
    """
    def post(self, request, locacao_id):
        locador_id = request.session.get('locador_id')
        
        if not locador_id:
            return Response({
                'success': False,
                'message': 'você precisa estar logado como locador'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            locacao = Locacao.objects.select_related(
                'requisicaoLocacao__ofertaLocacao'
            ).get(id=locacao_id)
        except Locacao.DoesNotExist:
            return Response({
                'success': False,
                'message': 'locação não encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if locacao.locador.id != int(locador_id):
            return Response({
                'success': False,
                'message': 'você não tem permissão'
            }, status=status.HTTP_403_FORBIDDEN)
        
        if locacao.status != 'devolvida':
            return Response({
                'success': False,
                'message': 'a locação precisa estar com status devolvida'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        locacao.status = 'concluida'
        locacao.locadorConfirmouDevolucao = True
        locacao.dataConfirmacaoDevolucao = timezone.now()
        locacao.dataConclusao = timezone.now()
        # a locação termina de verdade quando o locador confirma que recebeu de volta
        locacao.dataFimReal = timezone.now()
        locacao.save()
        
        return Response({
            'success': True,
            'message': 'Locação concluída com sucesso!',
            'status': locacao.status
        })


@method_decorator(csrf_exempt, name='dispatch')
class MinhasLocacoesLocatarioView(APIView):
    """
    Lista locações do usuário logado (locatário OU locador).
    Se for locatário: mostra locações onde ele alugou.
    Se for locador: mostra locações dos seus itens.
    """
    def get(self, request):
        locatario_id = request.session.get('locatario_id')
        locador_id = request.session.get('locador_id')
        
        if not locatario_id and not locador_id:
            return Response({
                'success': False,
                'message': 'você precisa estar logado'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # filtra dependendo de quem tá logado
        if locatario_id:
            locacoes = Locacao.objects.filter(
                requisicaoLocacao__locatario_id=locatario_id
            )
        else:
            locacoes = Locacao.objects.filter(
                requisicaoLocacao__ofertaLocacao__locador_id=locador_id
            )
        
        locacoes = locacoes.select_related(
            'requisicaoLocacao__ofertaLocacao',
            'requisicaoLocacao__ofertaLocacao__locador',
            'requisicaoLocacao__locatario'
        ).prefetch_related(
            'requisicaoLocacao__ofertaLocacao__imagens'
        ).order_by('-dataCriacao')
        
        locacoes_data = []
        for loc in locacoes:
            # pega a foto principal
            img_principal = loc.oferta.imagens.filter(ehImagemPrincipal=True).first()
            if not img_principal:
                img_principal = loc.oferta.imagens.first()
            
            locacoes_data.append({
                'id': loc.id,
                'titulo': loc.titulo,
                'status': loc.status,
                'valorTotal': str(loc.valorTotal),
                # datas planejadas e reais
                'dataInicioPrevista': loc.dataInicioPrevista.isoformat(),
                'dataFimPrevista': loc.dataFimPrevista.isoformat() if loc.dataFimPrevista else None,
                'dataInicioReal': loc.dataInicioReal.isoformat() if loc.dataInicioReal else None,
                'dataFimReal': loc.dataFimReal.isoformat() if loc.dataFimReal else None,
                'dataCriacao': loc.dataCriacao.isoformat(),
                'oferta': {
                    'id': loc.oferta.id,
                    'titulo': loc.oferta.titulo,
                    'imagemPrincipal': img_principal.imagem.url if img_principal else None
                },
                'locador': {
                    'id': loc.locador.id,
                    'nome': loc.locador.nome
                },
                'locatario': {
                    'id': loc.locatario.id,
                    'nome': loc.locatario.nome
                }
            })
        
        return Response({
            'success': True,
            'locacoes': locacoes_data,
            'ehLocador': bool(locador_id),
            'ehLocatario': bool(locatario_id)
        })


@method_decorator(csrf_exempt, name='dispatch')
class MinhasLocacoesLocadorView(APIView):
    """
    Lista locações do locador logado (itens que estão alugados).
    """
    def get(self, request):
        locador_id = request.session.get('locador_id')
        
        if not locador_id:
            return Response({
                'success': False,
                'message': 'você precisa estar logado como locador'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        locacoes = Locacao.objects.filter(
            requisicaoLocacao__ofertaLocacao__locador_id=locador_id
        ).select_related(
            'requisicaoLocacao__ofertaLocacao',
            'requisicaoLocacao__locatario'
        ).prefetch_related(
            'requisicaoLocacao__ofertaLocacao__imagens'
        ).order_by('-dataCriacao')
        
        locacoes_data = []
        for loc in locacoes:
            # pega a foto principal
            img_principal = loc.oferta.imagens.filter(ehImagemPrincipal=True).first()
            if not img_principal:
                img_principal = loc.oferta.imagens.first()
            
            locacoes_data.append({
                'id': loc.id,
                'titulo': loc.titulo,
                'status': loc.status,
                'valorTotal': str(loc.valorTotal),
                # datas planejadas e reais
                'dataInicioPrevista': loc.dataInicioPrevista.isoformat(),
                'dataFimPrevista': loc.dataFimPrevista.isoformat() if loc.dataFimPrevista else None,
                'dataInicioReal': loc.dataInicioReal.isoformat() if loc.dataInicioReal else None,
                'dataFimReal': loc.dataFimReal.isoformat() if loc.dataFimReal else None,
                'dataCriacao': loc.dataCriacao.isoformat(),
                'oferta': {
                    'id': loc.oferta.id,
                    'titulo': loc.oferta.titulo,
                    'imagemPrincipal': img_principal.imagem.url if img_principal else None
                },
                'locatario': {
                    'id': loc.locatario.id,
                    'nome': loc.locatario.nome
                }
            })
        
        return Response({
            'success': True,
            'locacoes': locacoes_data
        })


@method_decorator(csrf_exempt, name='dispatch')
class EnviarMensagemLocacaoView(APIView):
    """
    Envia mensagem no chat da locação (usa as mensagens da requisição).
    """
    def post(self, request, locacao_id):
        from ..models import Mensagem
        
        locador_id = request.session.get('locador_id')
        locatario_id = request.session.get('locatario_id')
        
        if not locador_id and not locatario_id:
            return Response({
                'success': False,
                'message': 'Não autorizado'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            locacao = Locacao.objects.select_related(
                'requisicaoLocacao__ofertaLocacao'
            ).get(id=locacao_id)
        except Locacao.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Locação não encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # checa se pode
        eh_locador = bool(locador_id) and int(locacao.locador.id) == int(locador_id)
        eh_locatario = bool(locatario_id) and int(locacao.locatario.id) == int(locatario_id)
        
        if not eh_locador and not eh_locatario:
            return Response({
                'success': False,
                'message': 'Você não tem permissão'
            }, status=status.HTTP_403_FORBIDDEN)
        
        texto = request.data.get('texto', '').strip()
        if not texto:
            return Response({
                'success': False,
                'message': 'Mensagem vazia'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        remetente = 'locador' if eh_locador else 'locatario'
        
        # salva a mensagem no chat da requisição
        mensagem = Mensagem.objects.create(
            requisicao=locacao.requisicaoLocacao,
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

"""
URL configuration for Allugou project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from rest_framework.routers import DefaultRouter

from AllugouApp import views
from AllugouApp.api.viewsets import *
from AllugouApp.api.authentication import LoginView, LogoutView, GetCSRFToken, RegisterView, PasswordResetView, CheckSessionView, MeuEnderecoView
from AllugouApp.api.ofertas import CreateOfertaView, ListMyOfertasView, OfertaDetailView, ListAllOfertasView, EditOfertaView, DeleteOfertaView
from AllugouApp.api.requisicoes import CreateRequisicaoView
from AllugouApp.api.notifications import (
    NotificacoesLocadorView, 
    NotificacoesLocatarioView, 
    MarcarRequisicaoVistaView,
    RequisicaoDetailView as RequisicaoDetailAPIView,
    AtualizarStatusRequisicaoView,
    EnviarMensagemView
)
from AllugouApp.api.locacoes import (
    PagarRequisicaoView,
    LocacaoDetailView,
    ConfirmarRecebimentoView,
    EnviarFotoDevolucaoView,
    ConfirmarDevolucaoView,
    MinhasLocacoesLocatarioView,
    MinhasLocacoesLocadorView,
    EnviarMensagemLocacaoView
)
from django.urls import re_path
from django.contrib.auth import views as auth_views

router = DefaultRouter()

router.register(r'enderecos', EnderecoViewSet, basename = 'Endereços')
router.register(r'locatarios', LocatarioViewSet, basename = 'Locatarios')
router.register(r'locadores', LocadorViewSet, basename = 'Locadores')
router.register(r'ofsloc', OfertaLocacaoViewSet, basename = 'Ofertas de Locação')
router.register(r'imagens-oferta', ImagemOfertaViewSet, basename = 'Imagens das Ofertas')
router.register(r'mensagens', MensagemViewSet, basename = 'Mensagens')
router.register(r'reqsloc', RequisicaoLocacaoViewSet, basename = 'Requisições de Locação')
router.register(r'locacoes', LocacaoViewSet, basename = 'Locações')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/login/', LoginView.as_view(), name='api_login'),
    path('api/logout/', LogoutView.as_view(), name='api_logout'),
    path('api/csrf/', GetCSRFToken.as_view(), name='api_csrf'),
    path('api/check-session/', CheckSessionView.as_view(), name='api_check_session'),
    path('api/meu-endereco/', MeuEnderecoView.as_view(), name='api_meu_endereco'),
    path('api/password-reset/', PasswordResetView.as_view(), name='api_password_reset'),
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('api/ofertas/create/', CreateOfertaView.as_view(), name='api_create_oferta'),
    path('api/ofertas/my/', ListMyOfertasView.as_view(), name='api_my_ofertas'),
    path('api/ofertas/all/', ListAllOfertasView.as_view(), name='api_all_ofertas'),
    path('api/ofertas/<int:oferta_id>/', OfertaDetailView.as_view(), name='api_oferta_detail'),
    path('api/ofertas/<int:oferta_id>/edit/', EditOfertaView.as_view(), name='api_edit_oferta'),
    path('api/ofertas/<int:oferta_id>/delete/', DeleteOfertaView.as_view(), name='api_delete_oferta'),
    path('api/requisicoes/create/', CreateRequisicaoView.as_view(), name='api_create_requisicao'),
    # Notifications
    path('api/notificacoes/locador/', NotificacoesLocadorView.as_view(), name='api_notificacoes_locador'),
    path('api/notificacoes/locatario/', NotificacoesLocatarioView.as_view(), name='api_notificacoes_locatario'),
    path('api/requisicoes/<int:requisicao_id>/', RequisicaoDetailAPIView.as_view(), name='api_requisicao_detail'),
    path('api/requisicoes/<int:requisicao_id>/marcar-vista/', MarcarRequisicaoVistaView.as_view(), name='api_marcar_vista'),
    path('api/requisicoes/<int:requisicao_id>/status/', AtualizarStatusRequisicaoView.as_view(), name='api_atualizar_status'),
    path('api/requisicoes/<int:requisicao_id>/mensagem/', EnviarMensagemView.as_view(), name='api_enviar_mensagem'),
    path('api/requisicoes/<int:requisicao_id>/pagar/', PagarRequisicaoView.as_view(), name='api_pagar'),
    # Locações
    path('api/locacoes/minhas/', MinhasLocacoesLocatarioView.as_view(), name='api_minhas_locacoes'),
    path('api/locacoes/locador/', MinhasLocacoesLocadorView.as_view(), name='api_locacoes_locador'),
    path('api/locacoes/<int:locacao_id>/', LocacaoDetailView.as_view(), name='api_locacao_detail'),
    path('api/locacoes/<int:locacao_id>/confirmar-recebimento/', ConfirmarRecebimentoView.as_view(), name='api_confirmar_recebimento'),
    path('api/locacoes/<int:locacao_id>/foto-devolucao/', EnviarFotoDevolucaoView.as_view(), name='api_foto_devolucao'),
    path('api/locacoes/<int:locacao_id>/confirmar-devolucao/', ConfirmarDevolucaoView.as_view(), name='api_confirmar_devolucao'),
    path('api/locacoes/<int:locacao_id>/mensagem/', EnviarMensagemLocacaoView.as_view(), name='api_mensagem_locacao'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
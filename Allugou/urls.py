"""
URL configuration for Allugou project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from rest_framework.routers import DefaultRouter

from AllugouApp import views
from AllugouApp.api.viewsets import *

router = DefaultRouter()

router.register(r'enderecos', EnderecoViewSet, basename = 'Endereços')
router.register(r'locatarios', LocatarioViewSet, basename = 'Locatarios')
router.register(r'locadores', LocadorViewSet, basename = 'Locadores')
router.register(r'ofsloc', OfertaLocacaoViewSet, basename = 'Ofertas de Locação')
router.register(r'imagens-oferta', ImagemOfertaViewSet, basename = 'Imagens das Ofertas')
router.register(r'chats', ChatViewSet, basename = 'Chats')
router.register(r'reqsloc', RequisicaoLocacaoViewSet, basename = 'Requisições de Locação')
router.register(r'locacoes', LocacaoViewSet, basename = 'Locações')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
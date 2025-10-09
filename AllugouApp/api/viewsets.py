from ..models import *
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response


class EnderecoViewSet(viewsets.ModelViewSet):
    
    serializer_class = EnderecoSerializer
    queryset = Endereco.objects.all()


class LocatarioViewSet(viewsets.ModelViewSet):
    
    serializer_class = LocatarioSerializer
    queryset = Locatario.objects.all()

class LocadorViewSet(viewsets.ModelViewSet):
    
    serializer_class = LocadorSerializer
    queryset = Locador.objects.all()


class OfertaLocacaoViewSet(viewsets.ModelViewSet):
    
    serializer_class = OfertaLocacaoSerializer
    queryset = OfertaLocacao.objects.all()


class ChatViewSet(viewsets.ModelViewSet):
    
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()


class RequisicaoLocacaoViewSet(viewsets.ModelViewSet):
    
    serializer_class = RequisicaoLocacaoSerializer
    queryset = RequisicaoLocacao.objects.all()


class LocacaoViewSet(viewsets.ModelViewSet):
    
    serializer_class = LocacaoSerializer
    queryset = Locacao.objects.all()

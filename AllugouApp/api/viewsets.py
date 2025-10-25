from ..models import *
from .serializers import *
from django.http import Http404
from rest_framework import viewsets, permissions
from rest_framework.response import Response



# class UserViewSet(viewsets.GenericViewSet):

#     queryset = 

class EnderecoViewSet(viewsets.ModelViewSet):
    
    # permission_classes = [permissions.IsAuthenticated] se nao tiver logado como admin: mort

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
    
    def get_queryset(self):
        queryset = OfertaLocacao.objects.all()
        locador_id = self.request.query_params.get('locador', None)
        if locador_id is not None:
            queryset = queryset.filter(locador_id=locador_id)
        return queryset.prefetch_related('imagens')


class ImagemOfertaViewSet(viewsets.ModelViewSet):
    serializer_class = ImagemOfertaSerializer
    queryset = ImagemOferta.objects.all()
    
    def create(self, request, *args, **kwargs):
        oferta_id = request.data.get('ofertaLocacao')
        eh_principal = request.data.get('ehImagemPrincipal', False)
        
        if eh_principal:
            # Se a nova imagem é principal, remove o status de principal das outras
            ImagemOferta.objects.filter(
                ofertaLocacao_id=oferta_id,
                ehImagemPrincipal=True
            ).update(ehImagemPrincipal=False)
        
        return super().create(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = ImagemOferta.objects.all()
        oferta_id = self.request.query_params.get('oferta', None)
        if oferta_id is not None:
            queryset = queryset.filter(ofertaLocacao_id=oferta_id)
        return queryset


class ChatViewSet(viewsets.ModelViewSet):
    
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()


class RequisicaoLocacaoViewSet(viewsets.ModelViewSet):
    
    serializer_class = RequisicaoLocacaoSerializer
    queryset = RequisicaoLocacao.objects.all()


class LocacaoViewSet(viewsets.ModelViewSet):
    
    serializer_class = LocacaoSerializer
    queryset = Locacao.objects.all()

from AllugouApp.models import *
from rest_framework import serializers

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        # lista de campos: ['cep', 'rua', 'numero', 'bairro','cidade', 'estado', 'complemento', 'observacao']
        fields = '__all__'

class LocatarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locatario
        fields = '__all__'

class LocadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locador
        fields = '__all__'

class ImagemOfertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagemOferta
        fields = '__all__'
        read_only_fields = ['dataCriacao']

class OfertaLocacaoSerializer(serializers.ModelSerializer):
    imagens = ImagemOfertaSerializer(many=True, read_only=True)
    imagem_principal = serializers.SerializerMethodField()

    class Meta:
        model = OfertaLocacao
        fields = '__all__'
        read_only_fields = ['dataCriacao']

    def get_imagem_principal(self, obj):
        imagem_principal = obj.imagens.filter(ehImagemPrincipal=True).first()
        if imagem_principal:
            return ImagemOfertaSerializer(imagem_principal).data
        return None


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class RequisicaoLocacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequisicaoLocacao
        fields = '__all__'


class LocacaoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Locacao
        fields = '__all__'




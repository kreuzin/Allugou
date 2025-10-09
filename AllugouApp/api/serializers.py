from AllugouApp.models import *
from rest_framework import serializers

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        # ['cep', 'rua', 'numero', 'bairro','cidade', 'estado', 'complemento', 'observacao']
        fields = '__all__'

class LocatarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locatario
        fields = '__all__'

class LocadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locador
        fields = '__all__'

class OfertaLocacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfertaLocacao
        fields = '__all__'


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




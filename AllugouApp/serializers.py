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
        fields = ['user', 'tel', 'cpf', 'nome', 'email', 'senha']

class LocadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locador
        fields = ['user', 'tel', 'cpf', 'nome', 'email', 'senha']

class OfertaLocacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfertaLocacao
        fields = ['valorDiaria', 'descricao', 'titulo', 'ofereceEntrega']


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['remetente', 'texto', 'data']


class RequisicaoLocacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequisicaoLocacao
        fields = ['dataConclusao']


class LocacaoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Locacao
        fields = ['foiEntregue', 'titulo', 'descricao', 'dataConclusao', 'preco', 'frete']




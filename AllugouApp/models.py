from django.db import models

class Locador(models.Model):

    user  = models.CharField(max_length=20 )
    tel   = models.CharField(max_length=11 )
    cpf   = models.CharField(max_length=11 )
    nome  = models.CharField(max_length=100)
    email = models.EmailField()
    senha = models.CharField(max_length=30 )

    #endereco fk


class Locatario(models.Model):

    user  = models.CharField(max_length=20 )
    tel   = models.CharField(max_length=11 )
    cpf   = models.CharField(max_length=11 )
    nome  = models.CharField(max_length=100)
    email = models.EmailField()
    senha = models.CharField(max_length=30, )

    #Endereco fk



class Endereco(models.Model):


    cep         = models.CharField(max_length=8  )
    rua         = models.CharField(max_length=30 )
    numero      = models.CharField(max_length=7  )
    bairro      = models.CharField(max_length=40 )
    cidade      = models.CharField(max_length=50 )
    estado      = models.CharField(max_length=2  ) 
    complemento = models.CharField(max_length=30 , null=True)
    observacao  = models.CharField(max_length=255, null=True)





class OfertaLocacao(models.Model):
    
    valorDiaria    = models.FloatField()
    descricao      = models.CharField(max_length=255)
    titulo         = models.CharField(max_length=50 )
    ofereceEntrega = models.BooleanField()

    #locador fk



class RequisicaoLocacao(models.Model):

    dataInicio    = models.DateTimeField(auto_now_add=True)
    dataConclusao = models.DateTimeField(null= True)  #vem depois

    #ofertalocacao_id 
    #ofertalocacao_locador_id 

    #locatario_id
    #Chat_id



class Locacao(models.Model):

    foiEntregue   = models.BooleanField()
    dataInicio    = models.DateTimeField(auto_now_add=True)
    titulo        = models.CharField(max_length=50)
    descricao     = models.CharField(max_length=255)
    dataConclusao = models.DateTimeField(null=True)
    preco         = models.FloatField()
    frete         = models.FloatField()

    # 6 estrangeiras... we cooked

class Chat(models.Model):
    remetente = models.CharField(max_field=10)
    mensagem  = models.CharField(max_field=255)
    data      = models.DateTimeField(auto_now_add=True)

from django.db import models


#botei on cascade em todos fk pq o django dava erro

class Endereco(models.Model):
    
    cep         = models.CharField(max_length=8  )
    rua         = models.CharField(max_length=30 )
    numero      = models.CharField(max_length=7  )
    bairro      = models.CharField(max_length=40 )
    cidade      = models.CharField(max_length=50 )
    estado      = models.CharField(max_length=2  ) 
    complemento = models.CharField(max_length=30 , null=True)
    observacao  = models.CharField(max_length=255, null=True)



class Locatario(models.Model):
    
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    user  = models.CharField(max_length=20 )
    tel   = models.CharField(max_length=11 )
    cpf   = models.CharField(max_length=11 )
    nome  = models.CharField(max_length=100)
    email = models.EmailField()
    senha = models.CharField(max_length=30 )

    

class Locador(models.Model):
    
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    user  = models.CharField(max_length=20 )
    tel   = models.CharField(max_length=11 )
    cpf   = models.CharField(max_length=11 )
    nome  = models.CharField(max_length=100)
    email = models.EmailField()
    senha = models.CharField(max_length=30 )




class OfertaLocacao(models.Model):
    locador = models.ForeignKey(Locador, on_delete=models.CASCADE)

    valorDiaria    = models.FloatField()
    descricao      = models.CharField(max_length=255)
    titulo         = models.CharField(max_length=50 )
    ofereceEntrega = models.BooleanField() #? esqueci oq e isso exatamente, eh se a pessoa entrega ou tem q ir buscar ne



class Chat(models.Model):
    
    remetente = models.CharField(max_length=10)
    texto  = models.CharField(max_length=255)
    data      = models.DateTimeField(auto_now_add=True)


class RequisicaoLocacao(models.Model):
    

    ofertaLocacao = models.ForeignKey(OfertaLocacao, on_delete=models.CASCADE)

    locatario = models.ForeignKey(Locatario, on_delete=models.CASCADE)

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    # locador = models.ForeignKey(Locador) se pa n precisa

    dataInicio    = models.DateTimeField(auto_now_add=True)
    dataConclusao = models.DateTimeField(null= True)  #vem depois
    



class Locacao(models.Model):
    

    requisicaoLocacao = models.ForeignKey(RequisicaoLocacao, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

    # 6 estrangeiras... we cooked --> na vdd aq so chamano as chave adjacente 

    foiEntregue   = models.BooleanField()
    dataInicio    = models.DateTimeField(auto_now_add=True)
    titulo        = models.CharField(max_length=50)
    descricao     = models.CharField(max_length=255)
    dataConclusao = models.DateTimeField(null=True)
    preco         = models.FloatField()
    frete         = models.FloatField()


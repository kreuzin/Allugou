from django.db import models
from django.contrib.auth.models import User



# coloquei on_delete=CASCADE em todos os ForeignKey porque o django dava erro sem

class Endereco(models.Model):

    cep         = models.CharField(max_length=8  )
    rua         = models.CharField(max_length=30 )
    numero      = models.CharField(max_length=7  )
    bairro      = models.CharField(max_length=40 )
    cidade      = models.CharField(max_length=50 )
    estado      = models.CharField(max_length=2  ) 
    complemento = models.CharField(max_length=30 , null=True)
    observacao  = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name_plural = 'Endereços' # página de admin retornaria endereços normalmente
    
    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.bairro}, {self.cidade} - {self.estado}, {self.cep}"



class Locatario(models.Model):
    
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    user  = models.CharField(max_length=20,unique=True)
    tel   = models.CharField(max_length=11 )
    cpf   = models.CharField(max_length=11, unique=True)
    nome  = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)

    class Meta:
       verbose_name_plural = 'Locatários' 

    def __str__(self):
        return self.user

class Locador(models.Model):
    
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    user  = models.CharField(max_length=20, unique=True)
    tel   = models.CharField(max_length=11 )
    cpf   = models.CharField(max_length=11, unique=True)
    nome  = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = 'Locadores' # página de admin retornaria locadores normalmente 

    def __str__(self):
        return self.user

class OfertaLocacao(models.Model):
    locador = models.ForeignKey(Locador, on_delete=models.CASCADE)
    localizacao = models.ForeignKey(Endereco, on_delete=models.CASCADE)

    valorDiaria    = models.FloatField()
    titulo         = models.CharField(max_length=50 )
    descricao      = models.CharField(max_length=255)
    ofereceEntrega = models.BooleanField() # se a pessoa oferece entrega ou se o cliente precisa buscar
    dataCriacao    = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Ofertas de Locação'
        ordering = ['-dataCriacao']

    def __str__(self):
        return self.titulo

class ImagemOferta(models.Model):
    ofertaLocacao = models.ForeignKey(OfertaLocacao, related_name='imagens', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='ofertas_imagens/')
    ehImagemPrincipal = models.BooleanField(default=False)
    ordem = models.IntegerField(default=0)
    dataCriacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Imagem da Oferta'
        verbose_name_plural = 'Imagens das Ofertas'
        ordering = ['ordem', 'dataCriacao']

    def __str__(self):
        return f"Imagem {self.ordem} - {self.ofertaLocacao.titulo}"

class Chat(models.Model):
    
    remetente = models.CharField(max_length=10)
    texto  = models.CharField(max_length=255)
    data      = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Chats'

    def __str__(self):
        return f"Chat de {self.remetente} em {self.data}"

class RequisicaoLocacao(models.Model):
    
    ofertaLocacao = models.ForeignKey(OfertaLocacao, on_delete=models.CASCADE)

    locatario = models.ForeignKey(Locatario, on_delete=models.CASCADE)

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    # locador = models.ForeignKey(Locador) se pa n precisa

    dataInicio    = models.DateTimeField(auto_now_add=True)
    dataConclusao = models.DateTimeField(null= True)  # vem depois

    class Meta:
        verbose_name_plural = 'Requisição de Locação'
    
    def __str__(self):
        return self.ofertaLocacao.titulo


class Locacao(models.Model):
    
    requisicaoLocacao = models.ForeignKey(RequisicaoLocacao, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)


    foiEntregue   = models.BooleanField()
    dataInicio    = models.DateTimeField(auto_now_add=True)
    titulo        = models.CharField(max_length=50)
    descricao     = models.CharField(max_length=255)
    dataConclusao = models.DateTimeField(null=True)
    preco         = models.FloatField()
    frete         = models.FloatField()

    # de 0 a 10
    notaParaLocador = models.IntegerField(null=True)
    notaParaLocatario = models.IntegerField(null=True)

    class Meta:
        verbose_name_plural = 'Locações'

    def __str__(self):
        return self.titulo


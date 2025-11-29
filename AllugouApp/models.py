from django.db import models
from django.contrib.auth.models import User



# precisa do on_delete=cascade em todos os foreignkey senão o django reclama

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
        verbose_name_plural = 'Endereços' # pro admin mostrar o nome certinho
    
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
        verbose_name_plural = 'Locadores' # pro admin mostrar o nome certinho

    def __str__(self):
        return self.user

class OfertaLocacao(models.Model):
    locador = models.ForeignKey(Locador, on_delete=models.CASCADE)
    localizacao = models.ForeignKey(Endereco, on_delete=models.CASCADE)

    valorDiaria    = models.FloatField()
    titulo         = models.CharField(max_length=50 )
    descricao      = models.TextField(max_length=1500)
    ofereceEntrega = models.BooleanField() # true = locador entrega, false = cliente busca
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


class RequisicaoLocacao(models.Model):
    """
    Requisição é a fase de negociação.
    Fluxo: pendente → aceita/recusada
    Quando aceita E paga, cria-se uma Locacao.
    """
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aceita', 'Aceita'),
        ('recusada', 'Recusada'),
    ]
    
    ofertaLocacao = models.ForeignKey(OfertaLocacao, on_delete=models.CASCADE, related_name='requisicoes')
    locatario = models.ForeignKey(Locatario, on_delete=models.CASCADE, related_name='requisicoes')

    dataInicioLocacao = models.DateField()  # quando o locatário quer começar
    dataFimLocacao = models.DateField(null=True)  # quando o locatário quer terminar
    valorTotal = models.DecimalField(max_digits=10, decimal_places=2)
    valorFrete = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    retiradaNoLocal = models.BooleanField(default=True)  # true = vai buscar, false = quer entrega
    dataCriacao = models.DateTimeField(auto_now_add=True)
    vistoPeloLocador = models.BooleanField(default=False)  # marca se o locador já viu isso
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')

    class Meta:
        verbose_name = 'Requisição de Locação'
        verbose_name_plural = 'Requisições de Locação'
        ordering = ['-dataCriacao']
    
    def __str__(self):
        return f"Requisição #{self.id} - {self.ofertaLocacao.titulo}"


class Mensagem(models.Model):
    REMETENTE_CHOICES = [
        ('locador', 'Locador'),
        ('locatario', 'Locatário'),
    ]
    
    requisicao = models.ForeignKey(
        RequisicaoLocacao, 
        on_delete=models.CASCADE, 
        related_name='mensagens'
    )
    remetente = models.CharField(max_length=10, choices=REMETENTE_CHOICES)
    texto = models.TextField()
    enviadoEm = models.DateTimeField(auto_now_add=True)
    lido = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Mensagem'
        verbose_name_plural = 'Mensagens'
        ordering = ['enviadoEm']
    
    def __str__(self):
        return f'{self.remetente}: {self.texto[:50]}...'


class Locacao(models.Model):
    """
    Locação é criada quando a requisição é aceita E o locatário paga.
    Representa o processo ativo de aluguel do produto.
    Fluxo: ativa → em_uso → devolvida → concluida
    """
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),           # pagou, só falta entregar
        ('em_uso', 'Em Uso'),          # locatário já pegou o produto
        ('devolvida', 'Devolvida'),    # locatário mandou foto devolvendo
        ('concluida', 'Concluída'),    # locador confirmou que recebeu de volta
        ('cancelada', 'Cancelada'),    # deu ruim por algum motivo
    ]
    
    requisicaoLocacao = models.OneToOneField(
        RequisicaoLocacao, 
        on_delete=models.CASCADE,
        related_name='locacao'
    )
    enderecoEntrega = models.ForeignKey(
        Endereco, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="Endereço de entrega (se não for retirada)"
    )
    
    # copia esses dados da requisição pra ter um histórico
    titulo = models.CharField(max_length=50)
    descricao = models.CharField(max_length=255)
    valorTotal = models.DecimalField(max_digits=10, decimal_places=2)
    valorFrete = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    retiradaNoLocal = models.BooleanField(default=True)
    
    # datas que o locatário planejou (vem da requisição)
    dataInicioPrevista = models.DateField(help_text="Data de início planejada (da requisição)")
    dataFimPrevista = models.DateField(null=True, blank=True, help_text="Data de fim planejada (da requisição)")
    
    # datas de quando realmente aconteceu
    dataInicioReal = models.DateTimeField(null=True, blank=True, help_text="Quando o locatário confirmou recebimento")
    dataFimReal = models.DateTimeField(null=True, blank=True, help_text="Quando o locador confirmou devolução")
    
    # controle do fluxo
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativa')
    dataCriacao = models.DateTimeField(auto_now_add=True)  # quando pagou e criou a locação
    dataPagamento = models.DateTimeField(auto_now_add=True)
    
    # quando o locatário confirma que pegou o produto
    locatarioConfirmouRecebimento = models.BooleanField(default=False)
    dataConfirmacaoRecebimento = models.DateTimeField(null=True, blank=True)
    
    # dados da devolução
    fotoDevolucao = models.ImageField(upload_to='devolucoes/', null=True, blank=True)
    dataDevolucao = models.DateTimeField(null=True, blank=True)
    
    # quando o locador confirma que recebeu de volta
    locadorConfirmouDevolucao = models.BooleanField(default=False)
    dataConfirmacaoDevolucao = models.DateTimeField(null=True, blank=True)
    dataConclusao = models.DateTimeField(null=True, blank=True)
    
    # notas e comentários (1 a 5 estrelas)
    notaParaLocador = models.IntegerField(null=True, blank=True)
    comentarioParaLocador = models.TextField(null=True, blank=True)
    notaParaLocatario = models.IntegerField(null=True, blank=True)
    comentarioParaLocatario = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Locação'
        verbose_name_plural = 'Locações'
        ordering = ['-dataCriacao']

    def __str__(self):
        return f"Locação #{self.id} - {self.titulo}"
    
    @property
    def locador(self):
        return self.requisicaoLocacao.ofertaLocacao.locador
    
    @property
    def locatario(self):
        return self.requisicaoLocacao.locatario
    
    @property
    def oferta(self):
        return self.requisicaoLocacao.ofertaLocacao


# Sistema de Criação de Ofertas de Locação

## Funcionalidades Implementadas

### Backend (Django)

1. **API Endpoint para Criar Ofertas** (`/api/ofertas/create/`)
   - Aceita multipart/form-data para upload de imagens
   - Valida se o usuário é um locador autenticado
   - Cria oferta com múltiplas imagens
   - Marca uma imagem como principal
   - Usa transações atômicas para garantir consistência

2. **API Endpoint para Listar Ofertas do Locador** (`/api/ofertas/my/`)
   - Retorna apenas as ofertas do locador autenticado
   - Inclui todas as imagens relacionadas
   - Serializa com imagem principal destacada

### Frontend (Vue.js)

1. **Página de Criação de Ofertas** (`/new-ad`)
   - Formulário completo com validação
   - Upload de múltiplas imagens com preview
   - Seleção de imagem principal via radio buttons
   - Remoção individual de imagens antes do envio
   - Feedback visual de loading e mensagens de erro/sucesso

2. **Página de Listagem de Ofertas** (`/ads`)
   - Grid responsivo com cards de ofertas
   - Exibição de imagem principal, título, descrição, preço
   - Contador de imagens
   - Badge de entrega disponível
   - Botões de editar e excluir (excluir ainda não implementado)

## Como Testar

### Pré-requisitos
1. Usuário cadastrado como **locador**
2. Backend Django rodando: `python manage.py runserver`
3. Frontend Vue rodando: `cd allugou_vue && npm run serve`

### Fluxo de Teste

1. **Login como Locador**
   ```
   - Acesse http://localhost:8080/login
   - Faça login com credenciais de um locador
   - Verifique que aparece "Seus anúncios" e "Anuncie agora" na navbar
   ```

2. **Criar Nova Oferta**
   ```
   - Clique em "Anuncie agora" ou "Seus anúncios" → "Criar novo anúncio"
   - Preencha todos os campos:
     * Título (máx 50 caracteres)
     * Descrição (máx 255 caracteres)
     * Valor da diária (número decimal)
     * Oferece entrega (Sim/Não)
   - Selecione uma ou mais imagens (obrigatório)
   - Veja preview das imagens selecionadas
   - Escolha qual será a imagem principal (radio button)
   - Remova imagens indesejadas com o botão X
   - Clique em "Publicar anúncio"
   - Aguarde redirecionamento para listagem
   ```

3. **Visualizar Ofertas Criadas**
   ```
   - Acesse "Seus anúncios"
   - Veja grid com todas as ofertas do locador
   - Cada card mostra:
     * Imagem principal
     * Título e descrição
     * Preço formatado
     * Badge de entrega (se aplicável)
     * Contador de imagens
   ```

4. **Validações Implementadas**
   - Apenas locadores podem acessar `/new-ad` e `/ads`
   - Locatários são redirecionados para home
   - Upload de pelo menos 1 imagem é obrigatório
   - Todos os campos do formulário são obrigatórios
   - Imagens são armazenadas em `media/ofertas_imagens/`

## Estrutura de Dados

### OfertaLocacao
- `locador`: FK para Locador (automaticamente o usuário logado)
- `localizacao`: FK para Endereco (usa o endereço do locador)
- `titulo`: CharField (max 50)
- `descricao`: CharField (max 255)
- `valorDiaria`: FloatField
- `ofereceEntrega`: BooleanField
- `dataCriacao`: DateTimeField (auto)

### ImagemOferta
- `ofertaLocacao`: FK para OfertaLocacao
- `imagem`: ImageField (upload_to='ofertas_imagens/')
- `ehImagemPrincipal`: BooleanField
- `ordem`: IntegerField
- `dataCriacao`: DateTimeField (auto)

## Endpoints API

### POST `/api/ofertas/create/`
```
Content-Type: multipart/form-data
Headers: X-CSRFToken, Cookie (sessionid)

Body:
- titulo: string
- descricao: string
- valorDiaria: float
- ofereceEntrega: boolean
- imagemPrincipalIndex: int
- imagens: File[] (múltiplos arquivos)

Response:
{
  "success": true,
  "message": "oferta criada com sucesso!",
  "oferta": {...}
}
```

### GET `/api/ofertas/my/`
```
Headers: Cookie (sessionid)

Response:
{
  "success": true,
  "ofertas": [
    {
      "id": 1,
      "titulo": "...",
      "descricao": "...",
      "valorDiaria": 50.0,
      "ofereceEntrega": true,
      "imagens": [...],
      "imagem_principal": {...}
    }
  ]
}
```

## Próximos Passos (Não Implementado)

- [ ] Edição de ofertas existentes
- [ ] Exclusão de ofertas
- [ ] Validação de tamanho/formato de imagens no frontend
- [ ] Compressão automática de imagens
- [ ] Reordenação de imagens por drag-and-drop
- [ ] Paginação na listagem de ofertas
- [ ] Filtros e busca na listagem

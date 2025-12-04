"""
tentando criar um middleware para adicionar o header ngrok-skip-browser-warning em todas as respostas
para evitar a página de aviso do ngrok q ta enchendo o saco
"""
#nem tamo usano eu ach
class NgrokHeaderMiddleware:
    """
    Adiciona header ngrok-skip-browser-warning em todas as respostas
    para evitar a página de aviso do ngrok
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['ngrok-skip-browser-warning'] = 'true'
        return response

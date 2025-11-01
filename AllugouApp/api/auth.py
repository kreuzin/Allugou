from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if username and password:
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Get associated Locador if exists
            from AllugouApp.models import Locador
            try:
                locador = Locador.objects.get(user=username)
                return Response({
                    'success': True,
                    'user': {
                        'username': user.username,
                        'email': user.email,
                        'nome': locador.nome,
                        'id': locador.id
                    }
                })
            except Locador.DoesNotExist:
                return Response({
                    'success': True,
                    'user': {
                        'username': user.username,
                        'email': user.email
                    }
                })
        else:
            return Response(
                {'error': 'Credenciais inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )
    return Response(
        {'error': 'Por favor, forneça usuário e senha'},
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'success': True})
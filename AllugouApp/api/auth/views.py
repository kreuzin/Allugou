from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username is None or password is None:
        return Response({
            'success': False,
            'message': 'Por favor, forneça nome de usuário e senha'
        }, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return Response({
            'success': True,
            'user': {
                'username': user.username,
                'email': user.email
            }
        })
    else:
        return Response({
            'success': False,
            'message': 'Nome de usuário ou senha inválidos'
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({
        'success': True,
        'message': 'Sessão encerrada com sucesso'
    })
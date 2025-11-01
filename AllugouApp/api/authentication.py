from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from django.db import transaction
from .user_serializer import UserSerializer
from ..models import Locador, Locatario, Endereco

@method_decorator(ensure_csrf_cookie, name='post')
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if username is None or password is None:
            return Response({
                'success': False,
                'message': 'Por favor, forneça nome de usuário e senha.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return Response({
                'success': True,
                'user': UserSerializer(user).data
            })
        else:
            return Response({
                'success': False,
                'message': 'Nome de usuário ou senha incorretos.'
            }, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({
                'success': False,
                'message': 'Você não está conectado.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        logout(request)
        return Response({'success': True})

class GetCSRFToken(APIView):
    def get(self, request):
        return Response({'csrfToken': get_token(request)})

class RegisterView(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            # Extract common data
            user_type = request.data.get('user_type')  # 'locador' or 'locatario'
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password1')
            
            # Extract address data
            endereco_data = {
                'cep': request.data.get('cep'),
                'rua': request.data.get('rua'),
                'numero': request.data.get('numero'),
                'bairro': request.data.get('bairro'),
                'cidade': request.data.get('cidade'),
                'estado': request.data.get('estado'),
                'complemento': request.data.get('complemento'),
                'observacao': request.data.get('observacao')
            }

            # Extract user-specific data
            user_data = {
                'user': username,
                'tel': request.data.get('tel'),
                'cpf': request.data.get('cpf'),
                'nome': request.data.get('nome'),
                'email': email,
                'senha': password  # Note: We'll use Django's auth user for actual authentication
            }

            # Validate required fields
            required_fields = ['username', 'email', 'password1', 'tel', 'cpf', 'nome', 
                             'cep', 'rua', 'numero', 'bairro', 'cidade', 'estado']
            
            for field in required_fields:
                if not request.data.get(field):
                    return Response({
                        'success': False,
                        'message': f'O campo {field} é obrigatório.'
                    }, status=status.HTTP_400_BAD_REQUEST)

            # Create Django auth user
            if User.objects.filter(username=username).exists():
                return Response({
                    'success': False,
                    'message': 'Nome de usuário já está em uso.'
                }, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(email=email).exists():
                return Response({
                    'success': False,
                    'message': 'E-mail já está em uso.'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Create the auth user
            auth_user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Create address
            endereco = Endereco.objects.create(**endereco_data)

            # Create specific user type
            user_data['endereco'] = endereco
            if user_type == 'locador':
                if Locador.objects.filter(cpf=user_data['cpf']).exists():
                    raise ValueError('CPF já cadastrado como locador.')
                user_model = Locador.objects.create(**user_data)
            elif user_type == 'locatario':
                if Locatario.objects.filter(cpf=user_data['cpf']).exists():
                    raise ValueError('CPF já cadastrado como locatário.')
                user_model = Locatario.objects.create(**user_data)
            else:
                raise ValueError('Tipo de usuário inválido.')

            # Log the user in
            login(request, auth_user)

            return Response({
                'success': True,
                'message': 'Usuário registrado com sucesso!',
                'user': UserSerializer(auth_user).data,
                'user_type': user_type
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
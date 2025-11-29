from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
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
            
            # determinar tipo de usuário e salvar ID na sessão
            user_type = None
            try:
                locador = Locador.objects.filter(user=username).first()
                if locador:
                    user_type = 'locador'
                    request.session['locador_id'] = locador.id
                    request.session['locatario_id'] = None
                else:
                    locatario = Locatario.objects.filter(user=username).first()
                    if locatario:
                        user_type = 'locatario'
                        request.session['locatario_id'] = locatario.id
                        request.session['locador_id'] = None
            except Exception as e:
                print(f"erro ao determinar tipo de usuário: {e}")
            
            return Response({
                'success': True,
                'user': UserSerializer(user).data,
                'user_type': user_type
            })
        else:
            return Response({
                'success': False,
                'message': 'Nome de usuário ou senha incorretos.'
            }, status=status.HTTP_401_UNAUTHORIZED)

@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    """logout sem csrf para protótipo: evita falhas de csrf durante logout"""
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({
                'success': False,
                'message': 'Você não está conectado.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        logout(request)
        return Response({'success': True})

@method_decorator(ensure_csrf_cookie, name='get')
class GetCSRFToken(APIView):
    """retorna o token csrf e garante que o cookie csrf seja definido"""
    def get(self, request):
        return Response({'csrfToken': get_token(request)})

@method_decorator(ensure_csrf_cookie, name='post')
class RegisterView(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            print(f"requisição de registro recebida com dados: {request.data}")
            
            # extrair dados comuns
            user_type = request.data.get('user_type')  # 'locador' ou 'locatario'
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password1')
            
            print(f"user_type: {user_type}, username: {username}, email: {email}")
            
            # extrair dados de endereço
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

            # extrair dados específicos do usuário
            user_data = {
                'user': username,
                'tel': request.data.get('tel'),
                'cpf': request.data.get('cpf'),
                'nome': request.data.get('nome'),
                'email': email,
                'senha': password  # nota: nois vai usar o User do django para autenticação
            }

            # confere os campos obrigatorios
            required_fields = ['user_type', 'username', 'email', 'password1', 'tel', 'cpf', 'nome', 
                             'cep', 'rua', 'numero', 'bairro', 'cidade', 'estado']
            
            for field in required_fields:
                if not request.data.get(field):
                    return Response({
                        'success': False,
                        'message': f'o campo {field} é obrigatório.'
                    }, status=status.HTTP_400_BAD_REQUEST)

            # cria o user de login no django
            if User.objects.filter(username=username).exists():
                return Response({
                    'success': False,
                    'message': 'nome de usuário já está em uso.'
                }, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(email=email).exists():
                return Response({
                    'success': False,
                    'message': 'e-mail já está em uso.'
                }, status=status.HTTP_400_BAD_REQUEST)

            # criar o usuário de autenticação
            auth_user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # criar endereço
            endereco = Endereco.objects.create(**endereco_data)

            # criar tipo específico de usuário
            user_data['endereco'] = endereco
            if user_type == 'locador':
                if Locador.objects.filter(cpf=user_data['cpf']).exists():
                    raise ValueError('cpf já cadastrado como locador.')
                user_model = Locador.objects.create(**user_data)
                request.session['locador_id'] = user_model.id
                request.session['locatario_id'] = None
            elif user_type == 'locatario':
                if Locatario.objects.filter(cpf=user_data['cpf']).exists():
                    raise ValueError('cpf já cadastrado como locatário.')
                user_model = Locatario.objects.create(**user_data)
                request.session['locatario_id'] = user_model.id
                request.session['locador_id'] = None
            else:
                raise ValueError('tipo de usuário inválido.')

            # fazer login do usuário
            login(request, auth_user)

            return Response({
                'success': True,
                'message': 'usuário registrado com sucesso!',
                'user': UserSerializer(auth_user).data,
                'user_type': user_type
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            import traceback
            print(f"erro no registro: {str(e)}")
            print(f"traceback: {traceback.format_exc()}")
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    """endpoint simples para solicitar redefinição de senha via email"""
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'success': False, 'message': 'e-mail é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        from django.contrib.auth.forms import PasswordResetForm

        form = PasswordResetForm({'email': email})
        if form.is_valid():
            # envia email usando a configuração de email do django (console backend em dev)
            try:
                form.save(request=request, use_https=False, from_email=None, email_template_name='registration/password_reset_email.html')
                return Response({'success': True, 'message': 'Instruções de redefinição enviadas se o e-mail existir.'})
            except Exception as e:
                return Response({'success': False, 'message': f'erro ao enviar e-mail: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'success': False, 'message': 'e-mail inválido.'}, status=status.HTTP_400_BAD_REQUEST)


class CheckSessionView(APIView):
    """verifica se a sessão do usuário ainda é válida"""
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({
                'success': True,
                'authenticated': False
            })
        
        # determinar tipo de usuário
        user_type = None
        username = request.user.username
        
        try:
            locador = Locador.objects.filter(user=username).first()
            if locador:
                user_type = 'locador'
                request.session['locador_id'] = locador.id
                request.session['locatario_id'] = None
            else:
                locatario = Locatario.objects.filter(user=username).first()
                if locatario:
                    user_type = 'locatario'
                    request.session['locatario_id'] = locatario.id
                    request.session['locador_id'] = None
        except Exception as e:
            print(f"erro ao determinar tipo de usuário: {e}")
        
        return Response({
            'success': True,
            'authenticated': True,
            'user': UserSerializer(request.user).data,
            'user_type': user_type
        })


class MeuEnderecoView(APIView):
    """retorna o endereço do usuário logado"""
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({
                'success': False,
                'message': 'usuário não autenticado'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        locatario_id = request.session.get('locatario_id')
        locador_id = request.session.get('locador_id')
        
        endereco = None
        
        if locatario_id:
            try:
                locatario = Locatario.objects.get(id=locatario_id)
                endereco = locatario.endereco
            except Locatario.DoesNotExist:
                pass
        elif locador_id:
            try:
                locador = Locador.objects.get(id=locador_id)
                endereco = locador.endereco
            except Locador.DoesNotExist:
                pass
        
        if endereco:
            return Response({
                'success': True,
                'endereco': {
                    'rua': endereco.rua,
                    'numero': endereco.numero,
                    'bairro': endereco.bairro,
                    'cidade': endereco.cidade,
                    'estado': endereco.estado,
                    'cep': endereco.cep,
                    'complemento': endereco.complemento
                }
            })
        
        return Response({
            'success': False,
            'message': 'endereço não encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
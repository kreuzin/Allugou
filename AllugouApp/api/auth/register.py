from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ValidationError

User = get_user_model()

@api_view(['POST'])
def register_view(request):
    print("Register view called")
    print("Request method:", request.method)
    print("Request data:", request.data)
    try:
        data = request.data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password1')

        # validar campos obrigatórios
        if not all([username, email, password]):
            return Response({
                'success': False,
                'message': 'Por favor, preencha todos os campos obrigatórios'
            }, status=status.HTTP_400_BAD_REQUEST)

        # verificar se o nome de usuário já existe
        if User.objects.filter(username=username).exists():
            return Response({
                'success': False,
                'message': 'Nome de usuário já está em uso'
            }, status=status.HTTP_400_BAD_REQUEST)

        # verificar se o e-mail já existe
        if User.objects.filter(email=email).exists():
            return Response({
                'success': False,
                'message': 'E-mail já está cadastrado'
            }, status=status.HTTP_400_BAD_REQUEST)

        # validar senha
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({
                'success': False,
                'message': ' '.join(e.messages)
            }, status=status.HTTP_400_BAD_REQUEST)

        # criar usuário
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return Response({
            'success': True,
            'message': 'Cadastro realizado com sucesso',
            'user': {
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_201_CREATED)

    except ValidationError as e:
        return Response({
            'success': False,
            'message': 'Erro de validação: ' + ' '.join(e.messages)
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # registrar detalhes do erro para depuração
        print(f"Erro no registro: {str(e)}")
        import traceback
        print(traceback.format_exc())
        
        return Response({
            'success': False,
            'message': f'Ocorreu um erro no cadastro: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
from django import forms
from django.contrib.auth.models import User
from .models import Endereco, Locador


class RegisterLocadorForm(forms.Form):
    # campos do usuário
    username = forms.CharField(label='Nome de usuário', max_length=150)
    email = forms.EmailField(label='E-mail')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput)

    # campos do locador
    nome = forms.CharField(label='Nome completo', max_length=100)
    cpf = forms.CharField(label='CPF', max_length=11)
    tel = forms.CharField(label='Telefone', max_length=11)

    # campos de endereço
    cep = forms.CharField(label='CEP', max_length=8)
    rua = forms.CharField(label='Rua', max_length=30)
    numero = forms.CharField(label='Número', max_length=7)
    bairro = forms.CharField(label='Bairro', max_length=40)
    cidade = forms.CharField(label='Cidade', max_length=50)
    estado = forms.CharField(label='Estado (UF)', max_length=2)
    complemento = forms.CharField(label='Complemento', max_length=30, required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Nome de usuário já existe')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('E-mail já cadastrado')
        return email

    def clean(self):
        cleaned = super().clean()
        pw = cleaned.get('password')
        pw2 = cleaned.get('password2')
        if pw and pw2 and pw != pw2:
            raise forms.ValidationError('As senhas não coincidem')
        return cleaned

    def save(self):
        """Create Endereco, User and Locador. Returns Locador instance."""
        data = self.cleaned_data

        endereco = Endereco.objects.create(
            cep=data['cep'],
            rua=data['rua'],
            numero=data['numero'],
            bairro=data['bairro'],
            cidade=data['cidade'],
            estado=data['estado'],
            complemento=data.get('complemento') or None,
        )

        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )

        locador = Locador.objects.create(
            endereco=endereco,
            user=data['username'],
            tel=data['tel'],
            cpf=data['cpf'],
            nome=data['nome'],
            email=data['email'],
            senha=data['password']
        )

        return locador

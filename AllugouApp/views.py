from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.http import FileResponse, Http404, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .forms import RegisterLocadorForm
from .models import Locador
import os
import mimetypes


@csrf_exempt
def serve_media_cors(request, path):
    """
    serve arquivos de mídia com headers CORS para funcionar cross-origin.
    necessário porque o Django static() não adiciona headers CORS.
    """
    # handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Origin, Content-Type, Accept'
        return response
    
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    
    if not os.path.exists(file_path):
        raise Http404("Arquivo não encontrado")
    
    # detecta o content-type baseado na extensão
    content_type, _ = mimetypes.guess_type(file_path)
    if content_type is None:
        content_type = 'application/octet-stream'
    
    # le o arquivo e cria resposta com content-type correto
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type=content_type)
    
    # headers CORS - todos necessarios pra funcionar em Firefox/Chrome
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, HEAD, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Origin, Content-Type, Accept, Range, ngrok-skip-browser-warning'
    response['Cross-Origin-Resource-Policy'] = 'cross-origin'
    response['X-Content-Type-Options'] = 'nosniff'
    
    # header pro ngrok nao mostrar pagina de aviso
    response['ngrok-skip-browser-warning'] = 'true'
    
    # cache pra performance
    response['Cache-Control'] = 'public, max-age=86400'
    response['Vary'] = 'Origin'
    
    return response


def register(request):
	if request.method == 'POST':
		form = RegisterLocadorForm(request.POST)
		if form.is_valid():
			locador = form.save()
			# loga o usuario automaticamente
			try:
				# pega o user do django q a gente criou no form.save
				from django.contrib.auth.models import User
				user = User.objects.get(username=form.cleaned_data['username'])
				auth_login(request, user)
			except Exception:
				pass
			messages.success(request, 'Registro efetuado com sucesso. Bem-vindo!')
			return redirect('/')
	else:
		form = RegisterLocadorForm()
	return render(request, 'register.html', {'form': form})


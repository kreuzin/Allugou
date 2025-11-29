from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from .forms import RegisterLocadorForm
from .models import Locador





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


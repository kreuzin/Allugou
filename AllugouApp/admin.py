from django.contrib import admin
from .models import *


"""
# superuser
# admin - admindjango depois eu vejo o que faço disso aqui
# vito
"""
# para usar o admin/
admin.site.register(Endereco)
admin.site.register(Locatario)
admin.site.register(Locador)
admin.site.register(OfertaLocacao)
admin.site.register(RequisicaoLocacao)
admin.site.register(Mensagem)
admin.site.register(Locacao)


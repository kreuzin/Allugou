from django.contrib import admin
from .models import *


"""
#superuser
# admin - admindjango dps eu vejo oq faço disso aq
#vito
"""
# Register your models here.

admin.site.register(Endereco)
admin.site.register(Locatario)
admin.site.register(Locador)
admin.site.register(OfertaLocacao)
admin.site.register(Chat)
admin.site.register(RequisicaoLocacao)
admin.site.register(Locacao)

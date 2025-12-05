"""
script para limpar o banco de dados para apresentação
mantém apenas o superusuário admin do Django
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Allugou.settings')
django.setup()

from django.contrib.auth.models import User
from AllugouApp.models import (
    Locador, Locatario, OfertaLocacao, ImagemOferta,
    RequisicaoLocacao, Locacao, Mensagem, Endereco
)

def limpar_banco():
    print("=" * 60)
    print("LIMPANDO BANCO DE DADOS")
    print("=" * 60)
    print()
    
    # Contar antes
    print("Estado ANTES da limpeza:")
    print(f"  - Ofertas de locação: {OfertaLocacao.objects.count()}")
    print(f"  - Imagens: {ImagemOferta.objects.count()}")
    print(f"  - Requisições: {RequisicaoLocacao.objects.count()}")
    print(f"  - Locações: {Locacao.objects.count()}")
    print(f"  - Mensagens: {Mensagem.objects.count()}")
    print(f"  - Locadores: {Locador.objects.count()}")
    print(f"  - Locatários: {Locatario.objects.count()}")
    print(f"  - Endereços: {Endereco.objects.count()}")
    print(f"  - Usuários Django (total): {User.objects.count()}")
    print(f"  - Superusuários: {User.objects.filter(is_superuser=True).count()}")
    print()
    
    confirmacao = input("Deseja realmente LIMPAR o banco? (digite 'SIM' para confirmar): ")
    
    if confirmacao.upper() != 'SIM':
        print("Operação cancelada.")
        return
    
    print()
    print("Iniciando limpeza...")
    print()
    
    # deletar na ordem correta (respeitar foreign keys)
    
    print("  Deletando mensagens...")
    Mensagem.objects.all().delete()
    
    print("  Deletando locações...")
    Locacao.objects.all().delete()
    
    print("  Deletando requisições...")
    RequisicaoLocacao.objects.all().delete()
    
    print("  Deletando imagens de ofertas...")
    ImagemOferta.objects.all().delete()
    
    print("  Deletando ofertas de locação...")
    OfertaLocacao.objects.all().delete()
    
    print("  Deletando locadores...")
    Locador.objects.all().delete()
    
    print("  Deletando locatários...")
    Locatario.objects.all().delete()
    
    print("  Deletando endereços...")
    Endereco.objects.all().delete()
    
    print(" Deletando usuários não-admin...")
    User.objects.filter(is_superuser=False).delete()
    
    print()
    print("=" * 60)
    print("LIMPEZA CONCLUÍDA")
    print("=" * 60)
    print()
    

    print("Estado DEPOIS da limpeza:")
    print(f"  - Ofertas de locação: {OfertaLocacao.objects.count()}")
    print(f"  - Imagens: {ImagemOferta.objects.count()}")
    print(f"  - Requisições: {RequisicaoLocacao.objects.count()}")
    print(f"  - Locações: {Locacao.objects.count()}")
    print(f"  - Mensagens: {Mensagem.objects.count()}")
    print(f"  - Locadores: {Locador.objects.count()}")
    print(f"  - Locatários: {Locatario.objects.count()}")
    print(f"  - Endereços: {Endereco.objects.count()}")
    print(f"  - Usuários Django: {User.objects.count()}")
    print()
    
    superusers = User.objects.filter(is_superuser=True)
    if superusers.exists():
        print("Superusuários mantidos:")
        for user in superusers:
            print(f"  - {user.username} ({user.email})")
    print()
    print("Banco pronto pra popular novamente")
    print()

if __name__ == '__main__':
    limpar_banco()

from django.views.decorators.csrf import csrf_exempt
from .views import login_view, logout_view
from .register import register_view

# adicionar isen\u00e7\u00e3o csrf a todas as visualiza\u00e7\u00f5es
login_view = csrf_exempt(login_view)
logout_view = csrf_exempt(logout_view)
register_view = csrf_exempt(register_view)

__all__ = ['login_view', 'logout_view', 'register_view']
from django.views.decorators.csrf import csrf_exempt
from .views import login_view, logout_view
from .register import register_view

# Add CSRF exemption to all views
login_view = csrf_exempt(login_view)
logout_view = csrf_exempt(logout_view)
register_view = csrf_exempt(register_view)

__all__ = ['login_view', 'logout_view', 'register_view']
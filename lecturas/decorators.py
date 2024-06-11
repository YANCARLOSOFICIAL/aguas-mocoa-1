from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.urls import reverse, NoReverseMatch
from django.contrib.auth.decorators import login_required

def group_required(group_names, redirect_to=None):
    """Require user to be in specific group(s)."""
    def in_group(user):
        if user.is_authenticated:
            if isinstance(group_names, list):
                return any(user.groups.filter(name=group).exists() for group in group_names)
            return user.groups.filter(name=group_names).exists()
        return False
    
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if in_group(request.user):
                return view_func(request, *args, **kwargs)
            if redirect_to:
                try:
                    # Try to treat redirect_to as a view name
                    redirect_url = reverse(redirect_to)
                except NoReverseMatch:
                    # If it fails, treat redirect_to as a URL
                    redirect_url = redirect_to
                return redirect(redirect_url)
            return redirect(request.META.get('HTTP_REFERER', '/Lectura/indexlectura'))
        return _wrapped_view

    return decorator

# Define the required decorators
administrador_or_area_comercial_required = group_required(['Admin', 'Area_Comercial'])
administrador_required = group_required('Admin')
area_comercial_required = group_required('Area_Comercial')
tecnico_operativo_required = group_required('Tecnico_Operativo')

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegistroUsuarioForm, LoginForm

def index(request):
    # Mostrar información del usuario si está logueado
    if request.user.is_authenticated:
        return HttpResponse(f"""
            <div style="font-family: Arial, sans-serif; padding: 20px;">
                <h1>¡Hola, Django desde Docker!</h1>
                <p>Bienvenido, <strong>{request.user.first_name} {request.user.last_name}</strong> ({request.user.username})</p>
                <p><a href="/logout/" style="color: #007bff;">Cerrar sesión</a> | 
                   <a href="/usuarios/" style="color: #007bff;">Ver usuarios</a></p>
            </div>
        """)
    else:
        return HttpResponse("""
            <div style="font-family: Arial, sans-serif; padding: 20px;">
                <h1>¡Hola, Django desde Docker!</h1>
                <p><a href="/login/" style="color: #007bff;">Iniciar sesión</a> | 
                   <a href="/registro/" style="color: #007bff;">Registrarse</a></p>
            </div>
        """)

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada exitosamente para {username}!')
            return redirect('index')
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'registration/registro.html', {'form': form})

def login_usuario(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido de nuevo, {user.first_name}!')
                # Redirigir a la página que el usuario quería acceder o al inicio
                next_page = request.GET.get('next', 'index')
                return redirect(next_page)
            else:
                messages.error(request, 'Credenciales inválidas.')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = LoginForm()
    
    return render(request, 'registration/login.html', {'form': form})

@login_required
def listar_usuarios(request):
    usuarios = User.objects.all().order_by('-date_joined')
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})
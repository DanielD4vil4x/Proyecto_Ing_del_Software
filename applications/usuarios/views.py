# Create your views here.
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import RegistroUsuarioForm

import pyotp


'''
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('menu')   # me redirige a la vista de menu
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'usuarios/login.html')
'''
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            request.session['pre_2fa_user_id'] = user.id  # Guarda el ID temporalmente
            return redirect('verificar_otp')  # Redirige a la vista de verificación
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'usuarios/login.html')


def menu_view(request):
    return render(request, 'usuarios/pagina_principal.html')

def logout_view(request):
    logout(request)
    return redirect('login')

'''

def registro_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        rol = request.POST.get('rol', '')  # si tu modelo lo tiene

        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
        else:
            User = get_user_model()
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Ese usuario ya existe.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.rol = rol  # si tu modelo tiene el campo rol
                user.save()
                messages.success(request, 'Usuario registrado exitosamente.')
                return redirect('login')  # Redirige al login si quieres

    return render(request, 'usuarios/registro.html')
'''


def registro_view(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario registrado correctamente.')
            return redirect('mostrar-qr')  # redirige al login
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'usuarios/registro.html', {'form': form})



def verificar_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user_id = request.session.get('pre_2fa_user_id')

        if not user_id:
            messages.error(request, "Sesión no válida.")
            return redirect('login')

        User = get_user_model()
        user = User.objects.get(id=user_id)

        totp = pyotp.TOTP(user.otp_secret)
        if totp.verify(otp):
            login(request, user)
            del request.session['pre_2fa_user_id']  # Limpia sesión temporal
            return redirect('menu')
        else:
            messages.error(request, "Código OTP inválido.")

    return render(request, 'usuarios/verificar_otp.html')

import pyotp
import qrcode
import io
import base64
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def mostrar_qr(request):
    user = request.user

    # Si el usuario ya tiene otp_secret, reutilízalo, si no, crea uno
    if not user.otp_secret:
        user.otp_secret = pyotp.random_base32()
        user.save()

    totp = pyotp.TOTP(user.otp_secret)
    otp_uri = totp.provisioning_uri(name=user.username, issuer_name="MiSitioDobleAuth")

    # Generar el QR
    qr = qrcode.make(otp_uri)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return render(request, 'usuarios/mostrar_qr.html', {'qr_code': img_str})


import pyotp
import qrcode
import base64
from io import BytesIO
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login

@login_required
def activar_2fa(request):
    user = request.user

    # Si no tiene clave OTP, la generamos
    if not user.otp_secret:
        user.otp_secret = pyotp.random_base32()
        user.save()

    # Generamos el QR
    otp_uri = pyotp.totp.TOTP(user.otp_secret).provisioning_uri(
        name=user.username, issuer_name="MiSitio"
    )
    qr = qrcode.make(otp_uri)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    if request.method == 'POST':
        codigo = request.POST.get('codigo_otp')
        totp = pyotp.TOTP(user.otp_secret)
        if totp.verify(codigo):
            request.session['2fa_validado'] = True
            messages.success(request, 'Doble autenticación completada correctamente.')
            return redirect('menu')
        else:
            messages.error(request, 'Código inválido. Intenta nuevamente.')

    return render(request, 'usuarios/activar_2fa.html', {
        'qr_base64': qr_base64
    })



import pyotp
import qrcode
import qrcode.image.svg
from io import BytesIO
import base64
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def verificar_otp_view(request):
    user = request.user

    # Si el usuario aún no tiene clave secreta, se la asignamos
    if not user.otp_secret:
        user.otp_secret = pyotp.random_base32()
        user.save()

    # Generamos el objeto TOTP y la URL para escanear
    totp = pyotp.TOTP(user.otp_secret)
    otp_auth_url = totp.provisioning_uri(name=user.username, issuer_name="MiAppSegura")

    # Generamos la imagen QR como base64
    qr = qrcode.make(otp_auth_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')
        if totp.verify(otp_code):
            request.session['otp_verified'] = True
            return redirect('menu')
        else:
            messages.error(request, "Código incorrecto. Inténtalo de nuevo.")

    return render(request, 'usuarios/verificar_otp.html', {'qr_base64': qr_base64})

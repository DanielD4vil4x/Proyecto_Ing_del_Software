from django.urls import path
from .views import login_view, logout_view, registro_view, menu_view, activar_2fa
from applications.usuarios import views

urlpatterns = [
    
    path('login/', login_view, name='login'),
    path('menu/', views.menu_view, name='menu'),
    path('logout/', logout_view,name='logout'),
    path('registro/', registro_view, name='registro'),
    path('verificar-otp/', views.verificar_otp, name='verificar_otp'),
    path('mostrar-qr/', views.mostrar_qr, name='mostrar_qr'),
    path('activar-2fa/', activar_2fa, name='activar_2fa'),
]






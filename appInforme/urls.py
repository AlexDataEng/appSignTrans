from django.urls import path
from . import views


urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('inicio', views.inicioInforme, name="inicioInforme"),
    path('emitir/', views.emitir, name="emitir"),
    path("actualizar/", views.actualizar_informe, name="actualizar_informe"),
    path("firmar/", views.firmarInforme, name="firmaInforme"),
    path("anular/", views.anularInforme, name="anularInforme"),
    path("buscar/", views.buscarInforme, name="buscarInforme"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('guardar_informacion/', views.guardar_informacion, name='guardar_informacion'),
    path('emitir_pdf/<int:n_informe>/', views.emitir_pdf, name="emitir_pdf")
    
]

from django.contrib import admin
from appInforme import models
# Register your models here.

admin.site.register(models.Usuarios)
admin.site.register(models.UsuariosPermitidoAnular)
admin.site.register(models.Clientes)
admin.site.register(models.Transportes)
admin.site.register(models.Conductores)
admin.site.register(models.Vendedores)
admin.site.register(models.Productos)
admin.site.register(models.Facturas)
admin.site.register(models.Informes)
admin.site.register(models.DetalleDevolucion)
admin.site.register(models.ProductosDev)
admin.site.register(models.FacturasInformes)

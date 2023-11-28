from django.db import models

# Create your models here.


class Usuarios(models.Model):
    id_usuarios = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=255, unique=True)
    tipo_permiso = models.CharField(max_length=100)
    firma = models.TextField()
    contrasena = models.CharField(max_length=255)

class UsuariosPermitidoAnular(models.Model):
    id_usuario_anula = models.AutoField(primary_key=True)
    nombre_usuario_anula = models.CharField(max_length=255, unique=True)

class Clientes(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    rut_cliente = models.CharField(max_length=12, unique=True)
    nombre_cliente = models.CharField(max_length=150)
    ciudad = models.CharField(max_length=100)
    comuna = models.CharField(max_length=150)

class Transportes(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_transporte = models.CharField(max_length=255)

class Conductores(models.Model):
    id_conductor = models.AutoField(primary_key=True)
    nombre_conductor = models.CharField(max_length=255, unique=True)

class Vendedores(models.Model):
    id_vendedor = models.AutoField(primary_key=True)
    nombre_vendedor = models.CharField(max_length=255, unique=True)
    

class Facturas(models.Model):
    factura = models.IntegerField(primary_key=True)
    fecha_factura = models.DateField()
    rut_cliente = models.CharField(max_length=12)


class Informes(models.Model):
    folio_informe = models.AutoField(primary_key=True)
    factura = models.IntegerField()
    nc_requerido = models.CharField(max_length=255, null=True)
    n_nc = models.IntegerField(null=True)
    orden_retiro = models.CharField(max_length=255, null=True)
    hoja_ruta = models.IntegerField(null=True)
    fecha_recepcion = models.DateField(null=True)
    fecha_informe = models.DateField()
    firma_calidad = models.TextField()
    firma_seleccion = models.TextField(null=True)
    firma_despacho = models.TextField(null=True)

class DetalleDevolucion(models.Model):
    folio_informe = models.IntegerField(primary_key=True)
    factura = models.IntegerField()
    tipo_devolucion = models.CharField(max_length=255)
    categoria_devolucion = models.CharField(max_length=255)
    motivo_devolucion = models.CharField(max_length=255, null=True)
    nombre_vendedor = models.CharField(max_length=255, null=True)
    transporte = models.CharField(max_length=255, null=True)
    usuario_anulacion = models.CharField(max_length=255, null=True)
    dev_envase_ic = models.CharField(max_length=255, null=True)
    cliente_recepciona = models.CharField(max_length=255, null=True)
    observacion = models.TextField(null=True)

class ProductosDev(models.Model):
    factura = models.IntegerField()
    folio_informe = models.IntegerField()
    codigo = models.IntegerField(primary_key=True)
    lote = models.IntegerField(null=True)
    nombre_producto = models.CharField(max_length=255, null=True)
    total_facturado = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_devuelto = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    bodega_destino = models.CharField(max_length=255, null=True)
    estado_producto = models.CharField(max_length=255, null=True)
    proceso = models.CharField(max_length=255, null=True)

    class Meta:
        unique_together = ('factura', 'folio_informe')


class Productos(models.Model):
    codigo = models.IntegerField(primary_key=True)
    lote = models.CharField(max_length=50, null=True)
    producto = models.CharField(max_length=255)

class FacturasInformes(models.Model):
    facturas_factura = models.IntegerField()
    informes_factura = models.IntegerField()
    
    class Meta:
        unique_together = ('facturas_factura', 'informes_factura')

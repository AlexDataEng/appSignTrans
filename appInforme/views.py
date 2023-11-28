from django.shortcuts import render, redirect
from appInforme import models
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

 # Modulos de creacion de PDF
from io import BytesIO
from xhtml2pdf import pisa
from jinja2 import Environment, FileSystemLoader

# Create your views here.

# Login
def login(request):
    return render(request, "login.html")

# Registrarse
def signup(request):
    return render(request, "registrarse.html")

# Inicio
def inicio(request):
    return render(request, "inicio.html")

# Inicio de informe
def inicioInforme(request):
    return render(request, "inicio-informe.html")



# Emitir Informe
"""def emitir(request):
    return render(request, "emitir-informe.html")
"""
def emitir(request):
    #Obtención de datos Clientes
    clientes = models.Clientes.objects.all()
    datos_clientes = {cliente.rut_cliente: {'nombre_cliente': cliente.nombre_cliente, 'ciudad': cliente.ciudad, 'comuna': cliente.comuna} for cliente in clientes}

    #Objención de usuarios con permisos de anulación
    usuarios_anulacion = models.UsuariosPermitidoAnular.objects.all()

    #Obtención de datos de los transporte
    transportes = models.Transportes.objects.values_list('nombre_transporte', flat=True)
    datos_transportes = {transporte: {} for transporte in transportes}
    datos_transportes_json = json.dumps(datos_transportes)
    
    #Obtención de datos de los Vendedores
    vendedores = models.Vendedores.objects.values_list('nombre_vendedor', flat=True)
    datosVendedores = list(vendedores)
    datosVendedoresJSON = json.dumps(datosVendedores)
    
    #Obtención de datos de los Conductores
    conductores = models.Conductores.objects.values_list('nombre_conductor', flat=True)
    datosConductores = list(conductores)
    datosConductoresJSON = json.dumps(datosConductores)

    #Obtención del próximo número de informe
        # Obtén el último número de informe desde la base de datos
    ultimo_numero_informe = models.Informes.objects.order_by('-folio_informe').first()

        # Calcula el próximo número de informe
    proximo_numero_informe = ultimo_numero_informe.folio_informe + 1 if ultimo_numero_informe else 1


     # Obtención de datos de productos
    productos = models.Productos.objects.all()
    datos_productos = {str(producto.codigo): {'lote': producto.lote, 'producto': producto.producto} for producto in productos}
    datos_productos_json = json.dumps(datos_productos)

    return render(request, 'emitir-informe.html', {
        'usuarios_anulacion': usuarios_anulacion,
        'datos_clientes_json': json.dumps(datos_clientes),
        'datos_transportes_json': datos_transportes_json,
        'datosVendedoresJSON': datosVendedoresJSON,
        'datosConductoresJSON': datosConductoresJSON,
        'proximo_numero_informe': proximo_numero_informe,
        'datos_productos_json': datos_productos_json
    })


















# Guardar la información
def guardar_informacion(request):
    
    if request.method == 'POST':
        
    # Obtener datos del formulario
        
        # Datos Detalles Devolucion
        fecha_recepcion = request.POST.get('fechaRecepcion')
        input_tipo_devolucion = request.POST.get('tipoDevolucion')
        lista_anulacion = request.POST.get('listaAnulacion')
        input_categoria_devolucion = request.POST.get('categoriaMotivo')
        motivo_devolucion = request.POST.get('motivo_devolucion')
        input_dev_envase_ic = request.POST.get('dev_envase_ic')     
        input_recepcion_cliente = request.POST.get('recepcion_cliente')
        orden_de_retiro = request.POST.get('orden_de_retiro')
        requiere_NC = request.POST.get('requiere_NC')
        input_observacion = request.POST.get('observacion')
        
        devo = {"arg_fecha_recepcion":fecha_recepcion, }

        # Datos Facturacion
        rut_cliente = request.POST.get('rut_cliente')
        nombre_cliente = request.POST.get('nombre_cliente')
        ciudad = request.POST.get('ciudad')
        comuna = request.POST.get('comuna')
        nombre_transporte = request.POST.get('nombre_transporte')
        input_n_ruta = request.POST.get('n_ruta')
        input_nombre_conductor = request.POST.get('nombre_conductor')
        input_nombre_vendedor = request.POST.get('nombre_vendedor')
        n_factura = request.POST.get('n_factura')
        input_fecha_factura = request.POST.get('fecha_factura')
        input_fecha_informe = request.POST.get('fecha_informe')
        n_informe = request.POST.get('n_informe')

        nombre_usuario_calidad = request.user.username
        nombre_usuario_seleccion = 'null'
        nombre_usuario_despacho = 'null'
        

        # Datos Tablas - Fila 1
        codigoProducto_Row1 = request.POST.get('codigoProducto_Row1')
        loteInput_Row1 = request.POST.get('loteInput_Row1')
        productoInput_Row1 = request.POST.get('productoInput_Row1')
        totalFacturado_Row1 = request.POST.get('totalFacturado_Row1')
        totalDevuelto_Row1 = request.POST.get('totalDevuelto_Row1')
        bodegaDestino_Row1 = request.POST.get('bodegaDestino_Row1')
        estadoProducto_Row1 = request.POST.get('estadoProducto_Row1')
        estadoProceso_Row1 = request.POST.get('estadoProceso_Row1')


        # Todos los datos en formato JSON
        import json

    # Recolectar datos

        # Datos de Devolucion
        datos_devolucion = {
            'fecha_recepcion': request.POST.get('fechaRecepcion'),
            'input_tipo_devolucion': request.POST.get('tipoDevolucion'),
            'lista_anulacion': request.POST.get('listaAnulacion'),
            'input_categoria_devolucion': request.POST.get('categoriaMotivo'),
            'motivo_devolucion': request.POST.get('motivo_devolucion'),
            'input_dev_envase_ic': request.POST.get('dev_envase_ic'),
            'input_recepcion_cliente': request.POST.get('recepcion_cliente'),
            'orden_de_retiro': request.POST.get('orden_de_retiro'),
            'requiere_NC': request.POST.get('requiere_NC'),
            'input_observacion': request.POST.get('observacion'),
        }

        # Datos de Facturacion
        datos_facturacion = {
            'rut_cliente': request.POST.get('rut_cliente'),
            'nombre_cliente': request.POST.get('nombre_cliente'),
            'ciudad': request.POST.get('ciudad'),
            'comuna': request.POST.get('comuna'),
            'nombre_transporte': request.POST.get('nombre_transporte'),
            'input_n_ruta': request.POST.get('n_ruta'),
            'input_nombre_conductor': request.POST.get('nombre_conductor'),
            'input_nombre_vendedor': request.POST.get('nombre_vendedor'),
            'n_factura': request.POST.get('n_factura'),
            'input_fecha_factura': request.POST.get('fecha_factura'),
            'input_fecha_informe': request.POST.get('fecha_informe'),
            'n_informe': request.POST.get('n_informe'),
            'nombre_usuario_calidad': request.user.username,
            'nombre_usuario_seleccion': 'null',
            'nombre_usuario_despacho': 'null',
        }

        # Datos de Fila 1
        datos_tabla_fila_1 = {
            'codigoProducto_Row1': request.POST.get('codigoProducto_Row1'),
            'loteInput_Row1': request.POST.get('loteInput_Row1'),
            'productoInput_Row1': request.POST.get('productoInput_Row1'),
            'totalFacturado_Row1': request.POST.get('totalFacturado_Row1'),
            'totalDevuelto_Row1': request.POST.get('totalDevuelto_Row1'),
            'bodegaDestino_Row1': request.POST.get('bodegaDestino_Row1'),
            'estadoProducto_Row1': request.POST.get('estadoProducto_Row1'),
            'estadoProceso_Row1': request.POST.get('estadoProceso_Row1'),
        }

        # Unificar los datos en un solo diccionario
        datos_totales = {
            'datos_devolucion': datos_devolucion,
            'datos_facturacion': datos_facturacion,
            'datos_tabla_fila_1': datos_tabla_fila_1,
        }

        # Convertir a formato JSON
        json_datos_totales = json.dumps(datos_totales, ensure_ascii=False, indent=4)



    # Insertar campos

        # Tabla Informe
        

        if fecha_recepcion is not True:
            
            nuevo_informe = models.Informes(
                folio_informe = n_informe,
                factura = n_factura,
                nc_requerido = requiere_NC,
                orden_retiro = orden_de_retiro,
                hoja_ruta = input_n_ruta,
                fecha_informe = input_fecha_informe,
                firma_calidad = nombre_usuario_calidad,
                firma_seleccion  = nombre_usuario_seleccion,
                firma_despacho = nombre_usuario_despacho)
                
            nuevo_informe.save()

        else:
            nuevo_informe = models.Informes(
                folio_informe = n_informe,
                factura = n_factura,
                nc_requerido = requiere_NC,
                orden_retiro = orden_de_retiro,
                hoja_ruta = input_n_ruta,
                fecha_recepcion = fecha_recepcion,
                fecha_informe = input_fecha_informe,
                firma_calidad = nombre_usuario_calidad,
                firma_seleccion  = nombre_usuario_seleccion,
                firma_despacho = nombre_usuario_despacho)
                
            nuevo_informe.save()

        
        # Tabla Hoja de Ruta (ELIMINADA)

        # Tabla Factuta
        nueva_factura = models.Facturas(
            factura = n_factura,
            fecha_factura = input_fecha_factura,
            rut_cliente = rut_cliente)
        nueva_factura.save()

            

        # Tabla DetalleDevolucion
        detalle_dev = models.DetalleDevolucion(
            folio_informe  = n_informe,
            factura = n_factura,
            tipo_devolucion = input_tipo_devolucion,
            categoria_devolucion = input_categoria_devolucion,
            motivo_devolucion = motivo_devolucion,
            nombre_vendedor = input_nombre_vendedor,
            transporte = nombre_transporte,
            usuario_anulacion = lista_anulacion,
            dev_envase_ic = input_dev_envase_ic,
            cliente_recepciona = input_recepcion_cliente,
            observacion = input_observacion)        
        detalle_dev.save()
        
        #       fila_1 = {"codigo" : codigoProducto_Row1, "lote" : loteInput_Row1} 

        # Tabla ProductosDev -  Fila 1
        if codigoProducto_Row1:
            detalle_dev = models.ProductosDev(
                factura = n_factura,
                folio_informe = n_informe,
                codigo = codigoProducto_Row1,
                lote = loteInput_Row1,
                nombre_producto = productoInput_Row1,
                total_facturado = totalFacturado_Row1,
                total_devuelto =  totalDevuelto_Row1,
                bodega_destino = bodegaDestino_Row1,
                estado_producto = estadoProducto_Row1,
                proceso = estadoProceso_Row1)
            detalle_dev.save()


        # Redirigir a una página de éxito o hacer lo que necesites después de procesar los datos ***************    *************** ************
        #   return redirect('emitir_pdf', n_informe=n_informe, datos_json=json_datos_totales)
    
        from urllib.parse import urlencode
        from django.urls import reverse

        datos_json=json_datos_totales

        # Codificar el JSON
        datos_json_encoded = urlencode({'datos_json': json.dumps(datos_json)})

        # Generar la URL con el parámetro de consulta
        url = f'{reverse("emitir_pdf", kwargs={"n_informe": n_informe})}?{datos_json_encoded}'

        # Redirigir a la página de éxito
        return redirect(url)

    # Renderizar la página si la solicitud no es POST
    return render(request, 'emitir-informe.html')  

    



# Emitir PDF
def emitir_pdf(request, n_informe, datos_json):
    

    #return HttpResponse(f"Pagina de exito Folio 3 : Informe {n_informe} " )
    
    # Convierte el JSON a un diccionario
    datos = json.loads(datos_json)

    # Datos de Devolucion
    fecha_recepcion = datos['datos_devolucion']['fecha_recepcion']
    input_tipo_devolucion = datos['datos_devolucion']['input_tipo_devolucion']
    lista_anulacion = datos['datos_devolucion']['lista_anulacion']
    input_categoria_devolucion = datos['datos_devolucion']['input_categoria_devolucion']
    input_dev_envase_ic = datos['datos_devolucion']['input_dev_envase_ic']
    input_recepcion_cliente = datos['datos_devolucion']['input_recepcion_cliente']
    orden_de_retiro = datos['datos_devolucion']['orden_de_retiro']
    requiere_NC = datos['datos_devolucion']['requiere_NC']
    input_observacion = datos['datos_devolucion']['input_observacion']

    # Datos de Facturacion
    rut_cliente = datos['datos_facturacion']['rut_cliente']
    nombre_cliente = datos['datos_facturacion']['nombre_cliente']
    ciudad = datos['datos_facturacion']['ciudad']
    comuna = datos['datos_facturacion']['comuna']
    nombre_transporte = datos['datos_facturacion']['nombre_transporte']
    input_n_ruta = datos['datos_facturacion']['input_n_ruta']
    input_nombre_conductor = datos['datos_facturacion']['input_nombre_conductor']
    input_nombre_vendedor = datos['datos_facturacion']['input_nombre_vendedor']
    n_factura = datos['datos_facturacion']['n_factura']
    input_fecha_factura = datos['datos_facturacion']['input_fecha_factura']
    input_fecha_informe = datos['datos_facturacion']['input_fecha_informe']
    nombre_usuario_calidad = datos['datos_facturacion']['nombre_usuario_calidad']
    nombre_usuario_seleccion = datos['datos_facturacion']['nombre_usuario_seleccion']
    nombre_usuario_despacho = datos['datos_facturacion']['nombre_usuario_despacho']

    # Datos de Fila1 Productos
    codigoProducto_Row1 = datos['datos_tabla_fila_1']['codigoProducto_Row1']
    loteInput_Row1 = datos['datos_tabla_fila_1']['loteInput_Row1']
    productoInput_Row1 = datos['datos_tabla_fila_1']['productoInput_Row1']
    totalFacturado_Row1 = datos['datos_tabla_fila_1']['totalFacturado_Row1']
    totalDevuelto_Row1 = datos['datos_tabla_fila_1']['totalDevuelto_Row1']
    bodegaDestino_Row1 = datos['datos_tabla_fila_1']['bodegaDestino_Row1']
    estadoProducto_Row1 = datos['datos_tabla_fila_1']['estadoProducto_Row1']
    estadoProceso_Row1 = datos['datos_tabla_fila_1']['estadoProceso_Row1']

    # Puedes pasar estos datos al contexto si estás renderizando una plantilla
    context = {
        'fecha_recepcion': fecha_recepcion,
        'input_tipo_devolucion': input_tipo_devolucion,
        'lista_anulacion': lista_anulacion,
        'input_categoria_devolucion': input_categoria_devolucion,
        'input_dev_envase_ic': input_dev_envase_ic,
        'input_recepcion_cliente': input_recepcion_cliente,
        'orden_de_retiro': orden_de_retiro,
        'requiere_NC': requiere_NC,
        'input_observacion': input_observacion,
        'rut_cliente': rut_cliente,
        'nombre_cliente': nombre_cliente,
        'ciudad': ciudad,
        'comuna': comuna,
        'nombre_transporte': nombre_transporte,
        'input_n_ruta': input_n_ruta,
        'input_nombre_conductor': input_nombre_conductor,
        'input_nombre_vendedor': input_nombre_vendedor,
        'n_factura': n_factura,
        'input_fecha_factura': input_fecha_factura,
        'input_fecha_informe': input_fecha_informe,
        'nombre_usuario_calidad': nombre_usuario_calidad,
        'nombre_usuario_seleccion': nombre_usuario_seleccion,
        'nombre_usuario_despacho': nombre_usuario_despacho,
        'codigoProducto_Row1': codigoProducto_Row1,
        'loteInput_Row1': loteInput_Row1,
        'productoInput_Row1': productoInput_Row1,
        'totalFacturado_Row1': totalFacturado_Row1,
        'totalDevuelto_Row1': totalDevuelto_Row1,
        'bodegaDestino_Row1': bodegaDestino_Row1,
        'estadoProducto_Row1': estadoProducto_Row1,
        'estadoProceso_Row1': estadoProceso_Row1,}



 
    def render_html_template(template_path, data):
            env = Environment(loader=FileSystemLoader('.'))
            template = env.get_template(template_path)
                
            return template.render(data)

    def convert_html_to_pdf(html_content, output_pdf):
            result = BytesIO()
            pisa.CreatePDF(BytesIO(html_content.encode('utf-8')), result)
                    
            with open(output_pdf, 'wb') as f:
                    f.write(result.getvalue())

            return HttpResponse(f"PDF Generado exitosamente {n_informe} " )

    # Ruta de la plantilla
    template_path = "/appInforme/template/formato_informe.html"
        
    datos = {'titulo': 'Ejemplo 8 de PDF con Python',
                'OBSERVACION': 'Este es un ejemplo básico de generación de PDF con Python y plantillas HTML.',
                "folio_informe" : n_informe,
                "fecha_informe": "28-11-2023"}
        
    # Ruta de salida 
    output_pdf_path = 'appInforme/dir_informe/nuevo_pdf.pdf'

    # Renderizamos los datos con el HTML
    html_content = render_html_template(template_path, datos)

    # Convertimos el html a PDF
    convert_html_to_pdf(html_content, output_pdf_path)
                
        

                #print('PDF generado con éxito: output2.pdf')


    return redirect('inicio')








# Actualizar Informe
def actualizar_informe(request):
    return render(request, "actualizar-informe.html")

# Finmar Informe
def firmarInforme(request):
    return render(request, "firmar-informe.html")

# Anular Informe
def anularInforme(request):
    return render(request, "anular-informe.html")

# Buscar Informe
def buscarInforme(request):
    return render(request, "buscar-informe.html")
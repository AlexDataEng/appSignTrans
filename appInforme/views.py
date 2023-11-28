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

    # Insertar campos

        # Tabla Informe
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
        return redirect('emitir_pdf', n_informe=n_informe)

    # Renderizar la página si la solicitud no es POST
    return render(request, 'emitir-informe.html')  

    



# Emitir PDF
def emitir_pdf(request, n_informe):
    
 
    return HttpResponse(f"Pagina de exito Folio 3 : Informe {n_informe} " )

    # 1. Debo capturar los datos asociados a ese informe.
    # 2. Generar informe
    

    
    
    return render(request, "formato_informe.html", {"FOLIO":500100})
    if request.method == 'POST':
        return HttpResponse("Pagina de exito" )
    else:
        return HttpResponse("Esta página solo acepta solicitudes POST para generar PDF.")
    


    """if request.method == 'POST':
        def render_html_template(template_path, data):
            env = Environment(loader=FileSystemLoader('.'))
            template = env.get_template(template_path)
                
            return template.render(data)

        def convert_html_to_pdf(html_content, output_pdf):
                result = BytesIO()
                pisa.CreatePDF(BytesIO(html_content.encode('utf-8')), result)
                    
                with open(output_pdf, 'wb') as f:
                    f.write(result.getvalue())

        
                template_path = "appInforme/template/formato_informe.html"
                datos = {
                        'titulo': 'Ejemplo 8 de PDF con Python',
                        'contenido': 'Este es un ejemplo básico de generación de PDF con Python y plantillas HTML.'
                    }

                output_pdf_path = 'appInforme/dir_informes/nuevo_pdf.pdf'
                html_content = render_html_template(template_path, datos)


                convert_html_to_pdf(html_content, output_pdf_path)
                return redirect('inicioInforme')

                #print('PDF generado con éxito: output2.pdf')


        return redirect('inicioInforme')

        # Maneja solicitudes GET devolviendo una respuesta HttpResponse de algún tipo.
    elif request.method == 'GET':
        #return HttpResponse("Esta página solo acepta solicitudes POST para generar PDF.")
        return render(request, 'inicio-informe.html')
    
    # Si la solicitud no es ni GET ni POST, devolver una respuesta vacía o un error
    return HttpResponse("Método de solicitud no admitido.")"""








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
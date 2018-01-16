from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from . import settings
from Chamas.Clases import usuario
from Chamas.Clases import carga
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json

def index(request):
    
    return render(request, 'Index.html')

#RUTA QUE VALIDA EL LOGIN DE LOS USUARIOS DE LA ADMINISTRACION
def login(request):
    if request.method == 'POST':
        nit = request.POST['nit']
        password = request.POST['password']
        resultado = usuario.logea_usuario(nit, password)
        if resultado:
            request.session['usuario'] = nit
            return redirect('regUserDB')
        else:
            return render(request, 'Index.html',{'invalido':resultado})

#DEVUELVE LA VISTA DE LA CARGA MASIVA DE DATOS
def load(request):
    return render(request, 'load_data.html')

#CARGA LA VISTA DE LOS REPORTES ADMINISTRATIVOS
def reports(request):
    return render(request, 'Reports.html')

#ESTA VISTA DESPLIEGA EL DASHBOARD
def dashboard(request):
    sellers = usuario.vendedores()       
    return render(request, 'Dasboard.html',{'sellers':sellers})

#ESTA RUTA PERMITE SUBIR ARCHIVOS AL SEVIDOR
def uploadFile(request):
    if request.method == 'POST':
        try:
            filename = request.FILES['archivo']
            fs = FileSystemStorage()
            filena = fs.save(filename.name, filename)
            uploadfile = fs.url(filena)
            res = carga.escribeCTL(filename.name, settings.BASE_DIR+"/media/")
            return render(request, 'load_data.html',{'exitoso':res})
            #carga.ejecuta(settings.BASE_DIR+"/media/")
        except Exception as inst:
            print(str(inst))
            return render(request, 'load_data.html',{'exitoso':False})
        return HttpResponse(settings.BASE_DIR+"/media/"+str(filename))

#EJECUTA LOS COMANDOS DESDE LA TERMINAL PARA LA CARGA MASIVA DE LOS DATOS
def cargaData(request):
    carga.ejecuta(settings.BASE_DIR+"/media/")
    return redirect('dashDB')

#SE ENCARGARA DE MOSTRAR LA VISTA PARA EL REGISTRO DE UN USUARIO NUEVO EN LA BASE DE DATOS
def reg_user(request):
    if request.method == 'POST':
        dpi = request.POST['dpi']
        nit = request.POST['nit']
        pnombre = request.POST['pnombre']
        snombre = request.POST['snombre']
        papellido = request.POST['papellido']
        sapellido = request.POST['sapellido']
        ecivil = request.POST['ecivil']
        gen = request.POST['gen']
        tipo = request.POST['tipo']
        tip = 0
        if tipo == 'Administrador':
            tip = 1
        res = usuario.registra_usuario(dpi,pnombre,snombre,papellido,sapellido,nit,ecivil,gen,tip)
        if res == True:
            return render(request, 'registrarUser.html',{'error':res})
        else:
            return render(request, 'registrarUser.html',{'error':res})
    else:
        return render(request, 'registrarUser.html')

def addAdmin(request):
    if request.method == 'POST':
        dpi = request.POST['dpi']
        res = usuario.agrega_admin(dpi)
        print(res)
        if res == True:
            #hizo el update
            return redirect('dashDB')
        else:
            #hubo un fallo
            return render(request,'Dasboard.html',{'res':res})

def dar_debaja(request, dpi):
    res = usuario.quita_admin(dpi)
    if res == True:
        return redirect('dashDB')
    else:
        return redirect('regUserDB')


def reporte1_data(request):
    datos = usuario.reporte1()
    return render(request, 'Reportes/MasDinero.html', {'datos':datos})

def reporte2_data(request):
    datos = usuario.reporte2()
    return render(request, 'Reportes/MasProducto.html', {'datos':datos})

def reporte3_data(request):
    datos = usuario.reporte3()
    return render(request, 'Reportes/VentasSolteros.html', {'datos':datos})

def reporte4_data(request):
    datos = usuario.reporte4()
    return render(request, 'Reportes/FacturasMes.html', {'datos':datos})

def reporte5_data(request):
    datos = usuario.reporte5()
    return render(request, 'Reportes/Porcentaje.html', {'datos':datos})

def reporte6_dir(request):
    return render(request, 'Reportes/FormDpi.html')

def reporte6_data(request):
    if request.method == 'POST':
        dpi = request.POST['dpi']
        datos = usuario.reporte6(dpi)
        return render(request, 'Reportes/FormDpi.html', {'datos':datos})

def detalle_factura(request, factura):
    datos = usuario.detalle_fac(factura)
    return render(request, 'Reportes/detalle.html', {'datos':datos})
    pass

#--------------------ANDROID----------------------------------
@csrf_exempt
def saludo(request):
    if request.method =='POST':
        return HttpResponse("SALUDOS DESDE DJANGO POST")
    else:
        return HttpResponse("METODO GET")    

@csrf_exempt
def ingresar_Android(request):
    if request.method == 'POST':
        nit = request.POST['nit']
        password = request.POST['password']
        resultado = usuario.loguea_usAndroid(nit, password)
        if resultado:
            return HttpResponse("True")
        else:
            return HttpResponse("False")
    else:
        return HttpResponse("INVALIDO")

@csrf_exempt
def devuelve_Usuarion(request):
    if request.method == 'POST':
        nit = request.POST['nit']
        resultado = usuario.devuelveUsuario(nit)
        serializa = ""
        if len(resultado) == 1:
            for r in resultado:
                dpi = r['DPIV']
                pnombre = r['PNOMBRE']
                snombre = r['SNOMBRE']
                papellido = r['PAPELLIDO']
                sapellido = r['SAPELLIDO']
                ecivil = r['ECIVIL']
                us = Usuario(dpi,pnombre,snombre,papellido,sapellido,ecivil)
                serializa = json.dumps(us, cls = UserEncoder, indent=4)
            print(serializa)
            return HttpResponse(str(serializa))
        else:
            return HttpResponse("NADA")
    else:
        return HttpResponse("nada")

@csrf_exempt
def devuelveCategorias(request):
    if request.method == 'GET':
        resultado = usuario.devuelve_categorias()
        serializa = ""
        lista = []
        if len(resultado)>0:
            for r in resultado:
                idcategoria = r['ID_CATEGORIA']
                nombre = r['NOMBRE']
                catego = Categoria(idcategoria,nombre)
                lista.append(catego)
            serializa = json.dumps(lista, cls = UserEncoder, indent=4)
            print(serializa)
            return HttpResponse(str(serializa))
        else:
            return HttpResponse("NADA")

@csrf_exempt
def devuelve_productos(request):
    if request.method == 'POST':
        idcategoria = request.POST['idcatego']
        resultado = usuario.devuelve_productos(idcategoria)
        serializa = ""
        lista = []
        if len(resultado)>0:
            for r in resultado:
                idproducto = r['ID_PRODUCTO']
                nombre = r['NOMBRE']
                producto = Producto(idproducto,nombre)
                lista.append(producto)
            serializa = json.dumps(lista, cls = UserEncoder, indent=4)
            print(serializa)
            return HttpResponse(str(serializa))
        else:
            return HttpResponse("NADA")

@csrf_exempt
def consulta_precio(request):
    if request.method == 'POST':
        idproducto = request.POST['idproducto']
        nombre = request.POST['nombre']
        resultado = usuario.consulta_precio(idproducto,nombre)
        for r in resultado:
            precio = r['PRICE']
            return HttpResponse(str(precio))
        return HttpResponse("NADA")

@csrf_exempt
def consulta_tallas(request):
    if request.method == 'POST':
        idproducto = request.POST['idproducto']
        resultado = usuario.consulta_tallas(idproducto)
        serializa = ""
        lista = []
        if len(resultado)>0:
            for r in resultado:
                talla = r['TALLAS']
                tal = Talla(talla)
                lista.append(tal)
            serializa = json.dumps(lista, cls=UserEncoder, indent=4)
            print(serializa)
            return HttpResponse(str(serializa))
        else:
            return HttpResponse("nada")


@csrf_exempt
def consulta_colores(request):
    if request.method == 'POST':
        idproducto = request.POST['idproducto']
        resultado = usuario.consulta_colores(idproducto)
        serializa = ""
        lista = []
        if len(resultado)>0:
            for r in resultado:
                color = r['COLORES']
                col = Color(color)
                lista.append(col)
            serializa = json.dumps(lista, cls=UserEncoder, indent=4)
            print(serializa)
            return HttpResponse(str(serializa))
        else:
            return HttpResponse("nada")

@csrf_exempt
def consulta_nombre_p(request):
    if request.method == 'POST':
        idproducto = request.POST['idproducto']
        print(idproducto)
        resultado = usuario.consulta_nombre_p(idproducto)
        serializa = ""
        lista = []
        if len(resultado)>0:
            for r in resultado:
                nomb = r['NOMBRE']
                print(nomb)
                return HttpResponse(str(nomb))
            #return HttpResponse("NADA")
        return HttpResponse("NADA")

@csrf_exempt
def sincro(request):
    if request.method == 'POST':
        nit = request.POST['nit']
        datos = request.POST['sincro']
        registros = datos.split('\n')
        print(len(registros))
        res = usuario.inserta_registros(registros,nit)
        if res:
            return HttpResponse("True")
        else:
            return HttpResponse("False")
    else:
        return HttpResponse("ERROR")

@csrf_exempt
def obten_facturas(request):
    if request.method == 'POST':
        nit = request.POST['nit']
        resultado = usuario.obten_facturas(nit)
        serializa = ""
        lista = []
        if len(resultado)>0:
            for r in resultado:
                fa = r['NO_FACTURA']
                fact = Factura(fa)
                lista.append(fact)
            serializa = json.dumps(lista, cls=UserEncoder, indent=4)
            print(serializa)
            return HttpResponse(str(serializa))
        else:
            return HttpResponse("NULL")

@csrf_exempt
def obten_total(request):
    if request.method == 'POST':
        no_factura = request.POST['no_factura']     
        resultado = usuario.dame_total(no_factura)
        if len(resultado)>0:
            for r in resultado:
                fa = r['TOTAL']
                return HttpResponse(fa)
        else:
            return HttpResponse("NULL")
    else:
        return HttpResponse("NADA")
            
@csrf_exempt
def obten_detallep(request):
    if request.method == 'POST':
        no_factura = request.POST['no_factura']
        resultado = usuario.obten_detalleP(no_factura)
        serializa = ""
        lista = []
        if len(resultado)>0:
            for r in resultado:
                nom = r['NOM']
                can = r['CANT']
                prod = Producto(can, nom)
                lista.append(prod)
            serializa = json.dumps(lista, cls=UserEncoder, indent=4)
            print(serializa)
            return HttpResponse(str(serializa))
        else:
            return HttpResponse("ERROR")
    else:
        return HttpResponse("error")

class Usuario:
    
    def __init__(self, dpi, pnombre, snombre, papellido, sapellido, ecivil):
        self.dpi = dpi
        self.pnombre = pnombre
        self.snombre = snombre
        self.papellido = papellido
        self.sapellido = sapellido
        self.ecivil = ecivil

class Factura:
    def __init__(self,no_factura):
        self.no_factura = no_factura
        
class Talla:
    
    def __init__(self, talla):
        self.talla = talla

class Color:
    
    def __init__(self,color):
        self.color = color
        
class Categoria:
    
    def __init__(self, idcategoria, nombre):
        self.idcategoria = idcategoria;
        self.nombre = nombre

class Producto:
    def __init__(self, idproducto, nombre):
        self.idproducto = idproducto
        self.nombre = nombre
        

class UserEncoder(json.JSONEncoder):
    
    def default(self, obj):
        return obj.__dict__
    
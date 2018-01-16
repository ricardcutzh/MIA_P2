"""Chamas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^login/', views.login ,name='loginDB'),
    url(r'^load/', views.load ,name='loadDB'),
    url(r'^Reportes/', views.reports ,name='reportDB'),
    url(r'^Usuario/', views.reg_user ,name='regUserDB'),
    url(r'^AddAdmin/', views.addAdmin ,name='addAdminDB'),
    url(r'^Dashboard/', views.dashboard ,name='dashDB'),
    url(r'^ Upload/', views.uploadFile ,name='uploadDB'),
    url(r'^ LoadData/', views.cargaData ,name='loadDataDB'),
    url(r'^admin/', admin.site.urls),
    url(r'^DeBaja/(?P<dpi>\d+)$', views.dar_debaja, name='bajaDB'),
    #----------------------------------------------------------------
    url(r'^Reporte1/', views.reporte1_data, name="rep1DB"),
    url(r'^Reporte2/', views.reporte2_data, name="rep2DB"),
    url(r'^Reporte3/', views.reporte3_data, name="rep3DB"),
    url(r'^Reporte4/', views.reporte4_data, name="rep4DB"),
    url(r'^Reporte5/', views.reporte5_data, name="rep5DB"),
    url(r'^Reporte6/', views.reporte6_dir, name="rep6dirDB"),
    url(r'^ReporteS6/', views.reporte6_data, name="rep6DB"),
    url(r'^Detalle/(?P<factura>\d+)$', views.detalle_factura, name='detallefacDB'),
    #----------------------------------------------------------------
    url(r'^Prueba/', views.saludo),
    url(r'^Ingresar', views.ingresar_Android),
    url(r'^Datos', views.devuelve_Usuarion),
    url(r'^Categorias', views.devuelveCategorias),
    url(r'^Productos', views.devuelve_productos),
    url(r'^Precio', views.consulta_precio),
    url(r'^Tallas', views.consulta_tallas),
    url(r'^Colores', views.consulta_colores),
    url(r'^ProductoNombre', views.consulta_nombre_p),
    url(r'^sincroniza', views.sincro),
    url(r'^Facturas', views.obten_facturas),
    url(r'^DameTotal', views.obten_total),
    url(r'^FacProductos', views.obten_detallep),
    #----------------------------------------------------------------
    url(r'^$', views.index, name='index'),
    #----------------------------------------------------------------
    
]

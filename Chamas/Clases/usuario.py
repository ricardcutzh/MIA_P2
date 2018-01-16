from django.db import connection, transaction
from collections import namedtuple
from datetime import datetime
import random

class user:
    def __init__(self):
        self.DPI
        self.PNOMBRE
        self.SNOMBRE
        self.PAPELLIDO
        self.SAPELLIDO
        self.TIPO
    def __str__(self):
        return self.PNOMBRE

def logea_usuario(nit, password):
    c = connection.cursor()
    bandera = False
    try:
        c.execute("SELECT * FROM USUARIO WHERE NIT=%s AND PNOMBRE =%s AND TIPO = 1",[nit,password])
        rows = c.fetchall()
        if len(rows) == 1:
            bandera = True
    except Exception as inst:
        print("ERROR "+str(inst))
    return bandera

def loguea_usAndroid(nit, password):
    c = connection.cursor()
    bandera = False
    try:
        c.execute("SELECT * FROM USUARIO WHERE NIT=%s AND PNOMBRE =%s",[nit,password])
        rows = c.fetchall()
        if len(rows) == 1:
            bandera = True
    except Exception as inst:
        print("ERROR "+str(inst))
    return bandera

def vendedores():
    c = connection.cursor()
    try:
        c.execute("SELECT DPIV, PNOMBRE, SNOMBRE, PAPELLIDO, SAPELLIDO, TIPO FROM USUARIO WHERE TIPO = 1")
        resultado = dictfetchall(c)
        return resultado
    except Exception as inst:
        print("ERROR "+str(inst))
        return None

def registra_usuario(dpi, pnombre, snombre, papellido, sapellido, nit, ecivil, gen, tipo):
    c = connection.cursor()
    try:
        c.execute("INSERT INTO USUARIO(DPIV,PNOMBRE,SNOMBRE,PAPELLIDO,SAPELLIDO,NIT,ECIVIL,GEN,TIPO) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",[dpi,pnombre,snombre,papellido,sapellido,nit,ecivil,gen,tipo])
        transaction.commit()
        return True
    except Exception as inst:
        print("Error "+str(inst))
        return False

def agrega_admin(dpi):
    c = connection.cursor()
    try:
        if existe_usuario(dpi):
            c.execute("UPDATE USUARIO SET TIPO = 1 WHERE DPIV = %s;",[dpi])
            #transaction.commit()
            return True
        else:
            return False
    except Exception as inst:
        print("Error: agrega admin "+str(inst))
        return False

def existe_usuario(dpi):
    c = connection.cursor()
    try:
        c.execute("SELECT DPIV FROM USUARIO WHERE DPIV = %s",[dpi])
        rows = c.fetchall()
        print(len(rows))
        if len(rows) > 0:
            return True 
        else:
            return False
    except Exception as inst:
        print("Error: "+str(inst))
        return False

def quita_admin(dpi):
    c = connection.cursor()
    try:
        if existe_usuario(dpi):
            c.execute("UPDATE USUARIO SET TIPO = 0 WHERE DPIV = %s;",[dpi])
            #transaction.commit()
            return True
        else:
            return False
    except Exception as inst:
        print("Error: agrega quita "+str(inst))
        return False

def reporte1():
    c = connection.cursor()
    try:
        c.execute("SELECT DPI, NOMBRE, APELLIDO,TO_CHAR(RES.T0TAL) AS GASTADO FROM( SELECT U.DPIV AS DPI, U.PNOMBRE AS NOMBRE, U.PAPELLIDO AS APELLIDO, SUM((DV.CANTIDAD * DV.PRECIO)) AS T0TAL FROM DETALLE_VENTA DV, FACTURA F, USUARIO U, PRODUCTO P WHERE U.DPIV = F.DPI_USUARIO AND F.NO_FACTURA = DV.NO_FACTURA AND DV.ID_PRODUCTO = P.ID_PRODUCTO  group by U.PNOMBRE, U.PAPELLIDO, U.DPIV ORDER BY SUM((DV.CANTIDAD * DV.PRECIO))  DESC) RES WHERE ROWNUM <=10;")
        resultado = dictfetchall(c)
        return resultado
    except Exception as inst:
        print("Error: REPORTE 1 "+str(inst))
        return None

def reporte2():
    c = connection.cursor()
    try:
        c.execute("SELECT RES.DPI, RES.NOMBRE, RES.APELLIDO, TO_CHAR(RES.NP) AS PROD FROM( SELECT U.DPIV AS DPI, U.PNOMBRE AS NOMBRE, U.PAPELLIDO AS APELLIDO, SUM(DV.CANTIDAD) AS NP FROM DETALLE_VENTA DV, FACTURA F, USUARIO U, PRODUCTO P WHERE  U.DPIV = F.DPI_USUARIO AND F.NO_FACTURA = DV.NO_FACTURA AND DV.ID_PRODUCTO = P.ID_PRODUCTO group by U.DPIV, U.PNOMBRE, U.PAPELLIDO ORDER BY SUM(DV.CANTIDAD) DESC) RES WHERE ROWNUM <=10;")
        resultado = dictfetchall(c)
        return resultado
    except Exception as inst:
        print("Error: REPORTE 2 "+str(inst))
        return None

def reporte3():
    c = connection.cursor()
    try:
        c.execute("SELECT IDP, PRODUCTO, TO_CHAR(RES.TOTALMES) AS NUV FROM (SELECT P.ID_PRODUCTO AS IDP, P.NOMBRE AS PRODUCTO, SUM(DV.CANTIDAD) AS TOTALMES FROM PRODUCTO P, DETALLE_VENTA DV, FACTURA F, USUARIO U WHERE U.ECIVIL = 'Soltero' AND U.DPIV = F.DPI_USUARIO AND F.NO_FACTURA = DV.NO_FACTURA AND DV.ID_PRODUCTO = P.ID_PRODUCTO AND EXTRACT(DAY FROM F.FECHA)=15  group by P.NOMBRE, P.ID_PRODUCTO ORDER BY TOTALMES DESC, P.NOMBRE ASC) RES;")
        resultado = dictfetchall(c)
        return resultado
    except Exception as inst:
        print("Error: REPORTE 3 "+str(inst))
        return None

def reporte4():
    c = connection.cursor()
    try:
        c.execute("SELECT TO_CHAR(RES.MES) AS MESES, TO_CHAR(RES.NO_FACTURAS) AS FACTURAS FROM(SELECT EXTRACT(MONTH FROM F.FECHA) AS MES, COUNT(F.NO_FACTURA) AS NO_FACTURAS FROM FACTURA F GROUP BY EXTRACT(MONTH FROM F.FECHA) ORDER BY MES) RES;")
        resultado = dictfetchall(c)
        return resultado
    except Exception as inst:
        print("Error: REPORTE 4 "+str(inst))
        return None

def reporte5():
    c = connection.cursor()
    try:
        c.execute("SELECT TO_CHAR(MESES) AS MONTHS, TO_CHAR(P_MAS) AS MASCULINO, TO_CHAR(P_FEM) AS FEMENINO FROM( SELECT MAS.MES AS MESES, ROUND((MAS.TOTAL_M/(MAS.TOTAL_M + FEM.TOTAL_F))*100,1) AS P_MAS , ROUND((FEM.TOTAL_F/(MAS.TOTAL_M + FEM.TOTAL_F))*100,1) AS P_FEM FROM(    SELECT EXTRACT(MONTH FROM F.FECHA) AS MES, SUM(DV.CANTIDAD * DV.PRECIO) TOTAL_M    FROM FACTURA F, DETALLE_VENTA DV, USUARIO U    WHERE U.GEN = 'M' AND U.DPIV = F.DPI_USUARIO AND F.NO_FACTURA = DV.NO_FACTURA group by EXTRACT(MONTH FROM F.FECHA) ORDER BY MES ASC) MAS,(    SELECT EXTRACT(MONTH FROM F.FECHA) AS MES, SUM(DV.CANTIDAD * DV.PRECIO) TOTAL_F    FROM FACTURA F, DETALLE_VENTA DV, USUARIO U    WHERE U.GEN = 'F' AND U.DPIV = F.DPI_USUARIO AND F.NO_FACTURA = DV.NO_FACTURA group by EXTRACT(MONTH FROM F.FECHA) ORDER BY MES ASC)FEM WHERE MAS.MES = FEM.MES GROUP BY MAS.MES, ROUND((MAS.TOTAL_M/(MAS.TOTAL_M + FEM.TOTAL_F))*100,1), ROUND((FEM.TOTAL_F/(MAS.TOTAL_M + FEM.TOTAL_F))*100,1) ORDER BY MESES ASC);")
        resultado = dictfetchall(c)
        return resultado
    except Exception as inst:
        print("Error: REPORTE 5 "+str(inst))
        return None

def reporte6(dpi):
    c = connection.cursor()
    try:
        c.execute("SELECT FAC, SER, FECH, TO_CHAR(TOTAL) AS TOT FROM(SELECT F.NO_FACTURA AS FAC, F.SERIE AS SER, F.FECHA AS FECH, SUM((DV.CANTIDAD * DV.PRECIO)) AS TOTAL FROM USUARIO U, FACTURA F, DETALLE_VENTA DV WHERE U.DPIV = %s AND U.DPIV = F.DPI_USUARIO AND F.NO_FACTURA = DV.NO_FACTURA group by F.NO_FACTURA, F.SERIE, F.FECHA ORDER BY TOTAL DESC);",[dpi])
        resultado = dictfetchall(c)
        return resultado
    except Exception as inst:
        print("Error: REPORTE 5 "+str(inst))
        return None

def detalle_fac(factura):
    c = connection.cursor()
    try:
        c.execute("SELECT NOMBRE, TALL, COL, TO_CHAR(QT) AS CANT, TO_CHAR(PR) AS PRICE FROM(SELECT P.NOMBRE AS NOMBRE, DV.TALLA AS TALL, DV.COLOR AS COL, DV.CANTIDAD AS QT, DV.PRECIO AS PR  FROM PRODUCTO P, DETALLE_VENTA DV, FACTURA F WHERE P.ID_PRODUCTO = DV.ID_PRODUCTO AND F.NO_FACTURA = DV.NO_FACTURA AND F.NO_FACTURA = %s);",[factura])
        resultado = dictfetchall(c)
        return resultado
    except Exception as inst:
        print("Error: REPORTE  detalle "+str(inst))
        return None

def devuelveUsuario(nit):
    c = connection.cursor()
    try:
        c.execute("SELECT DPIV, PNOMBRE, SNOMBRE, PAPELLIDO, SAPELLIDO, ECIVIL FROM USUARIO WHERE NIT = %s",[nit])
        resultado = dictfetchall(c)
        return resultado
    except Exception as inst:
        print("ERROR "+str(inst))
        return None

def devuelve_categorias():
    c = connection.cursor()
    try:
        c.execute("SELECT ID_CATEGORIA, NOMBRE FROM CATEGORIA")
        resultado = dictfetchall(c)
        return resultado
    except Exception as inst:
        print("ERROR "+str(inst))
        return None

def devuelve_productos(idcategoria):
    c = connection.cursor()
    try:
        c.execute("SELECT ID_PRODUCTO, NOMBRE FROM PRODUCTO WHERE ID_CATEGORIA=%s", [idcategoria])
        resultado = dictfetchall(c)
        return resultado
    except Exception as inst:
        print("ERROR "+str(inst))
        return None

def consulta_precio(idproducto, nombre):
    c = connection.cursor()
    try:
        c.execute("SELECT TO_CHAR(DV.PRECIO) AS PRICE FROM DETALLE_VENTA DV, PRODUCTO P WHERE DV.ID_PRODUCTO = P.ID_PRODUCTO AND P.ID_PRODUCTO = %s AND P.NOMBRE = %s AND ROWNUM = 1;",[idproducto,nombre])
        resultado = dictfetchall(c)
        return resultado
    except Exception as inst:
        print("ERROR "+str(inst))
        return None

def consulta_tallas(idproducto):
    c = connection.cursor()
    try:
        c.execute("SELECT DISTINCT DV.TALLA AS TALLAS FROM DETALLE_VENTA DV, PRODUCTO P WHERE DV.ID_PRODUCTO = P.ID_PRODUCTO AND P.ID_PRODUCTO =%s;",[idproducto])
        resultado = dictfetchall(c)
        return resultado
    except Exception as inst:
        print("ERROR "+str(inst))
        return None

def consulta_colores(idproducto):
    c = connection.cursor()
    try:
        c.execute("SELECT DISTINCT DV.COLOR AS COLORES FROM DETALLE_VENTA DV, PRODUCTO P WHERE DV.ID_PRODUCTO = P.ID_PRODUCTO AND P.ID_PRODUCTO = %s;",[idproducto])
        resultado = dictfetchall(c)
        return resultado
    except Exception as inst:
        print("ERROR "+str(inst))
        return None

def consulta_nombre_p(idproducto):
    c = connection.cursor()
    try:
        c.execute("SELECT NOMBRE FROM PRODUCTO WHERE ID_PRODUCTO=%s;",[idproducto])
        resultado = dictfetchall(c)
        return resultado
    except Exception as inst:
        print("ERROR "+str(inst))
        return None

#**************SINCRONIZACION DE SERVIDORES*****************************
def get_dpi(nit):
    c = connection.cursor()
    try:
        c.execute("SELECT DPIV FROM USUARIO WHERE NIT=%s;",[nit])
        resultado = dictfetchall(c)
        for r in resultado:
            dpi = r['DPIV']
            return dpi
    except Exception as inst:
        print("ERROR "+str(inst))
        return None

def devuelve_factura():
    no_factura = ""
    for x in range(0,6):
        val = random.randint(0,9)
        no_factura = no_factura + str(val)
    return no_factura

def inserta_factura(no_factura,dpi):
    now = datetime.now()
    anio = now.year
    mes = now.month
    dia = now.day
    fecha = str(dia)+"/"+str(mes)+"/"+str(anio)
    c = connection.cursor()
    try:
        c.execute("INSERT INTO FACTURA(NO_FACTURA,SERIE,FECHA,DPI_USUARIO,ID_SUCURSAL) VALUES(%s,%s,%s,%s,%s);",[no_factura,'A',fecha,dpi,'1'])
        transaction.commit()
        return True
    except Exception as inst:
        print("ERROR "+str(inst))
        return False

def inserta_detalle(no_factura, idproducto,talla,color,cantidad,precio):
    c = connection.cursor()
    try:
        c.execute("INSERT INTO DETALLE_VENTA(NO_FACTURA,ID_PRODUCTO,TALLA,COLOR,CANTIDAD,PRECIO) VALUES(%s,%s,%s,%s,%s,%s);",[no_factura,idproducto,talla,color,cantidad,precio])
        transaction.commit()
        return True
    except Exception as inst:
        print("ERROR "+str(inst))
        return False    

def inserta_registros(registros,nit):
    no_factura = devuelve_factura()
    dpi = get_dpi(nit)
    inserta_factura(no_factura,dpi)
    try:
        for reg in registros:
            linea = reg.split(',')
            if len(linea)>0:
                idproducto = linea[0]
                cantidad = linea[1]
                talla = linea[2]
                color = linea[3]
                precio = linea[4]
                inserta_detalle(no_factura,idproducto,talla,color,cantidad,precio)
        return True
    except Exception as inst:
        return False
    
#***********************FIN SINCRONIZACION******************************

def obten_facturas(nit):
    dpi = get_dpi(nit)
    c = connection.cursor()
    try:
        c.execute("SELECT NO_FACTURA FROM FACTURA WHERE DPI_USUARIO =%s;",[dpi])
        resultado = dictfetchall(c)
        return resultado
    except Exception as inst:
        print("ERROR "+str(inst))
        return None

def dame_total(no_factura):
    c = connection.cursor()
    try:
        c.execute("SELECT TO_CHAR(SUM(DV.CANTIDAD * DV.PRECIO)) AS TOTAL FROM DETALLE_VENTA DV WHERE DV.NO_FACTURA=%s", [no_factura])
        resultado = dictfetchall(c)
        return resultado
    except Exception as inst:
        print("ERROR "+str(inst))
        return None

def obten_detalleP(no_factura):
    c = connection.cursor()
    try:
        c.execute("SELECT P.NOMBRE AS NOM, TO_CHAR(DV.CANTIDAD) AS CANT FROM PRODUCTO P, DETALLE_VENTA DV WHERE P.ID_PRODUCTO = DV.ID_PRODUCTO AND DV.NO_FACTURA = %s;",[no_factura])
        resultado = dictfetchall(c)
        return resultado
    except Exception as inst:
        print("ERROR "+str(inst))
        return None

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
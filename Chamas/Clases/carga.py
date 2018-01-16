
import os
#CARGA DE ARCHIVOS A LA BASE DE DATOS

def escribeCTL(filename, rutaMedia):
    ruta = rutaMedia+filename
    ctl = open(rutaMedia+'carga.ctl', 'w')
    ctl.write("OPTIONS (SKIP=1)\n")
    ctl.write("LOAD DATA\n")
    ctl.write("CHARACTERSET WE8ISO8859P1\n")
    ctl.write("INFILE ")
    ctl.write("\'"+ str(ruta + "\'\n"))
    ctl.write("INTO TABLE MASTERT TRUNCATE\n")
    ctl.write("FIELDS TERMINATED BY \",\"\n")
    ctl.write("OPTIONALLY ENCLOSED BY \"\\\"\"\n")
    ctl.write("TRAILING NULLCOLS(\n")
    ctl.write("  DPIC \"TRIM(:DPIC)\",\n")
    ctl.write("  PNOMBREC \"TRIM(:PNOMBREC)\",\n")
    ctl.write("  SNOMBREC \"TRIM(:SNOMBREC)\",\n")
    ctl.write("  PAPELLIDOC \"TRIM(:PAPELLIDOC)\",\n")
    ctl.write("  SAPELLIDOC \"TRIM(:SAPELLIDOC)\",\n")
    ctl.write("  NITC \"TRIM(:NITC)\",\n")
    ctl.write("  ECIVILC \"TRIM(:ECIVILC)\",\n")
    ctl.write("  GENC \"TRIM(:GENC)\",\n")
    ctl.write("  SUCURSAL INTEGER EXTERNAL,\n")
    ctl.write("  DIRSUCURSAL \"TRIM(:DIRSUCURSAL)\",\n")
    ctl.write("  TELSUCURSAL \"TRIM(:TELSUCURSAL)\",\n")
    ctl.write("  DEPARTAMENTO \"TRIM(:DEPARTAMENTO)\",\n")
    ctl.write("  MUNICIPIO \"TRIM(:MUNICIPIO)\",\n")
    ctl.write("  DPIV \"TRIM(:DPIV)\",\n")
    ctl.write("  PNOMBREV \"TRIM(:PNOMBREV)\",\n")
    ctl.write("  SNOMBREV \"TRIM(:SNOMBREV)\",\n")
    ctl.write("  PAPELLIDOV \"TRIM(:PAPELLIDOV)\",\n")
    ctl.write("  SAPELLIDOV \"TRIM(:SAPELLIDOV)\",\n")
    ctl.write("  NITV \"TRIM(:NITV)\",\n")
    ctl.write("  ECIVILV \"TRIM(:ECIVILV)\",\n")
    ctl.write("  GENV \"TRIM(:GENV)\",\n")
    ctl.write("  FACTURA \"TRIM(:FACTURA)\",\n")
    ctl.write("  SERIE \"TRIM(:SERIE)\",\n")
    ctl.write("  FECHAFAC \"TO_DATE(:FECHAFAC, 'DD/MM/YYYY', 'NLS_DATE_LANGUAGE=ENGLISH')\",\n")
    ctl.write("  CANTIDAD INTEGER EXTERNAL,\n")
    ctl.write("  COLOR \"TRIM(:COLOR)\",\n")
    ctl.write("  TALLA \"TRIM(:TALLA)\",\n")
    ctl.write("  NOMBRE_P \"TRIM(:NOMBRE_P)\",\n")
    ctl.write("  PRECIO_P INTEGER EXTERNAL,\n")
    ctl.write("  CATEGORIA \"TRIM(:CATEGORIA)\"\n")
    ctl.write(")")
    ctl.close()
    return True

def ejecuta(media):
    cmd4 = "sqlldr userid= proyecto2/proyecto2 control="+media+"carga.ctl"
    cmd5 = "sqlplus proyecto2/proyecto2 @"+media+"INSERTAATABLAS.sql read;"
    os.system(cmd4)
    os.system(cmd5)


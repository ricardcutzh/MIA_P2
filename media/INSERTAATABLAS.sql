--INSERTANDO DATOS
INSERT INTO DEPARTAMENTO(NOMBRE)
SELECT DISTINCT DEPARTAMENTO FROM MASTERT;

--INSERTANDO CATEGORIAS
INSERT INTO CATEGORIA(NOMBRE)
SELECT DISTINCT CATEGORIA FROM MASTERT;

--INSERTANDO EN MUNICIPIO
INSERT INTO MUNICIPIO(NOMBRE, ID_DEPTO)
SELECT DISTINCT MA.MUNICIPIO, D.ID_DEPTO FROM MASTERT MA, DEPARTAMENTO D
WHERE MA.DEPARTAMENTO = D.NOMBRE;

--INSERTANDO EN PRODUCTO
INSERT INTO PRODUCTO(NOMBRE, ID_CATEGORIA)
SELECT DISTINCT M.NOMBRE_P,C.ID_CATEGORIA
FROM MASTERT M, CATEGORIA C
WHERE M.CATEGORIA = C.NOMBRE;

--INSERTANDO SUCURSALES
INSERT INTO SUCURSAL(ID_SUCURSAL, DIRECCION, TELEFONO, ID_MUNICIPIO)
SELECT DISTINCT M.SUCURSAL, M.DIRSUCURSAL, M.TELSUCURSAL, MU.ID_MUNICIPIO
FROM MASTERT M, MUNICIPIO MU
WHERE M.MUNICIPIO = MU.NOMBRE;

--INSERTANDO CLIENTES
INSERT INTO USUARIO(DPIV,PNOMBRE,SNOMBRE,PAPELLIDO,SAPELLIDO,NIT,ECIVIL,GEN)
SELECT DISTINCT DPIC, PNOMBREC, SNOMBREC, PAPELLIDOC, SAPELLIDOC, NITC, ECIVILC, GENC
FROM MASTERT;

--INSERTANDO DEMAS
INSERT INTO USUARIO(DPIV,PNOMBRE,SNOMBRE,PAPELLIDO,SAPELLIDO,NIT,ECIVIL,GEN)
SELECT DISTINCT DPIV ,PNOMBREV, SNOMBREV, PAPELLIDOV, SAPELLIDOV, NITV, ECIVILV, GENV
FROM MASTERT;

--INSERTANDO LAS FACTURAS
INSERT INTO FACTURA(NO_FACTURA, SERIE, FECHA, DPI_USUARIO, ID_SUCURSAL)
SELECT  DISTINCT FACTURA, SERIE, FECHAFAC, DPIC, SUCURSAL
FROM MASTERT group by FACTURA, SERIE, FECHAFAC, DPIC, SUCURSAL;

--INSERTANDO EL DETALLE DE FACTURAS
INSERT INTO DETALLE_VENTA(NO_FACTURA, ID_PRODUCTO, TALLA, COLOR, CANTIDAD, PRECIO)
SELECT M.FACTURA, P.ID_PRODUCTO, M.TALLA, M.COLOR, M.CANTIDAD, M.PRECIO_P
FROM MASTERT M, PRODUCTO P
WHERE M.NOMBRE_P = P.NOMBRE;
commit;
exit;
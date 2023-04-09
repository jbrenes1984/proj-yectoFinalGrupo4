from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow
from Interfaz.gestor_bodegas import Ui_MainWindow
from Dominio.IngresoArticulos import IngresoArticulos
from Dominio.EgresoEntreBodegas import Egresos 
import datetime
from Dominio.EgresoEntreBodegas.NuevaBodega import nuevaBodega


now = datetime.datetime.now()
fecha_actual = now.date()
fecha_actual_str = fecha_actual.strftime('%d-%m-%Y')


class FrmInterfaz(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()  # instancia de la interfaz gráfica
        self.ui.setupUi(self)  # inicializa la interfaz gráfica
        self.oingreso = None
        self.ui.pushButton_agregar_reg.clicked.connect(self.btn_agregar_datos_factura)
        self.ui.pushButton_enviar.clicked.connect(self.btn_agregar_egresos)
        self.ui.pushButton_guardar.clicked.connect(self.btn_guardar_lista)
        self.modelolista = QtGui.QStandardItemModel()
        self.ui.listaIngreso.setModel(self.modelolista)
        self.ui.listaEnvio.setModel(self.modelolista)
        self.ui.cod_registro.textChanged.connect(self.buscar_producto)
        self.ui.id_prod_envio.textChanged.connect(self.buscar_producto_egreso)
        self.ui.btnCrearBodega.clicked.connect(lambda :  self.agregar_bodega() and self.cargar_combobox())
        self.ui.btnEnviarBodegas.clicked.connect(self.btn_guardar_lista_egreso)
        self.cargar_combobox()
       



      
       

        self.paginas = {
            self.ui.pushButton_registro: self.ui.page_registro,
            self.ui.pushButton_crear_bodega: self.ui.page_crear_bodega,
            self.ui.pushButton_envio_bodega: self.ui.page_envio_bodega,
            self.ui.pushButton_entrega_articulos: self.ui.page_entrega_articulos,
            self.ui.pushButton_distribuidores: self.ui.page_distribuidores,
            self.ui.pushButton_saldos_inventario: self.ui.page_saldos_inventario,
            self.ui.pushButton_reporte_distrib: self.ui.page_reporte_distribuidor,
            self.ui.pushButton_reporte: self.ui.page_reporte_txt,
        }

        self.ui.pushButton_registro.clicked.connect(self.mostrar_pagina)
        self.ui.pushButton_crear_bodega.clicked.connect(lambda:self.mostrar_pagina()  and self.cargar_combobox())
        self.ui.pushButton_envio_bodega.clicked.connect(lambda: self.mostrar_pagina() and self.cargar_combobox())
        self.ui.pushButton_entrega_articulos.clicked.connect(self.mostrar_pagina)
        self.ui.pushButton_distribuidores.clicked.connect(self.mostrar_pagina)
        self.ui.pushButton_saldos_inventario.clicked.connect(self.mostrar_pagina)
        self.ui.pushButton_reporte_distrib.clicked.connect(self.mostrar_pagina)
        self.ui.pushButton_reporte.clicked.connect(self.mostrar_pagina)

    def mostrar_pagina(self):
        # obtiene el botón que se presionó
        boton = self.sender()

        # obtiene la página correspondiente del diccionario
        pagina = self.paginas.get(boton)

        # muestra la página en el QStackedWidget
        if pagina:
            self.ui.stackedWidget.setCurrentWidget(pagina)

    def btn_agregar_datos_factura(self):
        self.oingreso = IngresoArticulos.IngresoArticulos()
        self.oingreso.codigoArticulo = self.ui.cod_registro.text()
        self.oingreso.nombreArticulo = self.ui.nombre_registro.text()
        self.oingreso.cantidad = float(self.ui.cantidad_registro.text())
        self.oingreso.preciounitario = float(self.ui.precio_un_registro.text())
        self.oingreso.calcularMontoTotal()  # llamada al método calcularMontoTotal()
        self.bodega = "Bodega Principal"

        itemView = (self.oingreso.codigoArticulo+","+self.oingreso.nombreArticulo+","
                     + str(self.oingreso.cantidad) + ","+str(self.oingreso.preciounitario)+","+str(self.oingreso.montoTotal) +
                    "," + self.ui.numeroFacturaIngreso.text() + "," + fecha_actual_str + "," + self.bodega+ "," + "Ingreso Principal")

        item = QtGui.QStandardItem(itemView)
        self.modelolista.appendRow(item)

        self.ui.cod_registro.clear()
        self.ui.nombre_registro.clear()
        self.ui.cantidad_registro.clear()
        self.ui.precio_un_registro.clear()

    

    def btn_guardar_lista(self):
    # Establece el nombre de archivo y la ubicación
        filepath = "C:/Users/jbren/OneDrive/Escritorio/Proyecto Program 2/Dominio/IngresoArticulos/lista_ingresos.txt"

    # Abre el archivo para escribir
        with open(filepath, "a") as f:
        # Escribe cada línea de la lista en el archivo
         for row in range(self.modelolista.rowCount()):
            line = ""
            for col in range(self.modelolista.columnCount()):
                item = self.modelolista.item(row, col)
                if item is not None:
                    line += item.text() + ","
            line = line.rstrip(",") + "\n"
            f.write(line)

    # Elimina todos los elementos de la lista
        self.modelolista.clear()
        self.ui.numeroFacturaIngreso.clear()


 
    

    def buscar_producto(self):
    # Obtiene el ID ingresado por el usuario
        id_producto = self.ui.cod_registro.text()
        with open(r'C:\Users\jbren\OneDrive\Escritorio\Proyecto Program 2\Dominio\IngresoArticulos\lista_productos.txt', 'r') as f:
            self.lines = f.readlines()    
        
    # Busca el producto correspondiente en la lista
        producto = None
        for line in self.lines:
            datos_producto = line.strip().split(',')
            if datos_producto[0] == id_producto:
                producto = datos_producto
                break
            
        # Si encontramos el producto, colocamos su nombre y precio en los QLineEdit correspondientes
        if producto is not None:
            self.ui.nombre_registro.setText(producto[1])
            self.ui.precio_un_registro.setText(producto[2])
        else:
            # Si no encontramos el producto, limpiamos los QLineEdit correspondientes
            self.ui.nombre_registro.clear()
            self.ui.precio_un_registro.clear()


    
    def agregar_bodega(self):
        id = self.ui.lineEdit_3.text()
        nombre = self.ui.lineEdit_10.text().capitalize()
        direccion = self.ui.lineEdit_8.text().capitalize()
        telefono = self.ui.lineEdit_6.text()

        # Agregar los datos al archivo de texto
        archivo = "C:\\Users\\jbren\\OneDrive\\Escritorio\\Proyecto Program 2\\Dominio\\EgresoEntreBodegas\\bodegas.txt"  # dirección del archivo
        nueva_bodega = nuevaBodega(archivo)
        nueva_bodega.agregar_datos(id, nombre, direccion, telefono)
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_10.clear()
        self.ui.lineEdit_6.clear()
        self.ui.lineEdit_8.clear()
        self.cargar_combobox()


    def cargar_combobox(self):
        archivo = "C:\\Users\\jbren\\OneDrive\\Escritorio\\Proyecto Program 2\\Dominio\\EgresoEntreBodegas\\bodegas.txt"
        with open(archivo, 'r') as f:
            lines = f.readlines()

        bodegas = set()  # usar un set para eliminar duplicados
        for line in lines:
            data = line.strip().split(',')           
            bodega_recibe = data[1]        
            bodegas.add(bodega_recibe)

    
        self.ui.comboBox__bod_recibe.clear()

        for bodega in bodegas:           
            self.ui.comboBox__bod_recibe.addItem(bodega)

    
    def buscar_producto_egreso(self):
    # Obtiene el ID ingresado por el usuario
        id_producto = self.ui.id_prod_envio.text()

    # Abre el archivo de texto
        with open('C:/Users/jbren/OneDrive/Escritorio/Proyecto Program 2/Dominio/IngresoArticulos/lista_ingresos.txt', 'r') as archivo:
            # Itera sobre las líneas del archivo
            for line in archivo:
                datos_producto = line.strip().split(',')
                if datos_producto[0] == id_producto:
                    # Si encontramos el producto, colocamos su nombre y precio en los QLineEdit correspondientes
                    self.ui.nombre_producto_envio.setText(datos_producto[1])
                    self.ui.precio_unitario_envio.setText(datos_producto[2])
                    return
            
    # Si no encontramos el producto, limpiamos los QLineEdit correspondientes
        self.ui.nombre_producto_envio.clear()
        self.ui.precio_unitario_envio.clear()
  

    def btn_agregar_egresos(self):
         self.oegreso = Egresos.EgresoArticulos()
         self.oegreso.codigoArticulo = self.ui.id_prod_envio.text()
         self.oegreso.nombreArticulo = self.ui.nombre_producto_envio.text()
         self.oegreso.cantidad = float(self.ui.cantidad_producto_envio.text())
         self.oegreso.preciounitario = float(self.ui.precio_unitario_envio.text())
         self.oegreso.calcularMontoTotal()  # llamada al método calcularMontoTotal()
         self.oegreso.bodegaEnvia = self.ui.comboBox_bod_envia.currentText()
         self.oegreso.bodegaRecibe = self.ui.comboBox__bod_recibe.currentText()
         
         

         itemView = (self.oegreso.codigoArticulo+","+self.oegreso.nombreArticulo +","
                    + str(self.oegreso.cantidad) + ","+str(self.oegreso.preciounitario)+","+str(self.oegreso.montoTotal) +
                    "," + self.ui.label_19.text() + "," + fecha_actual_str + "," + self.oegreso.bodegaRecibe +"," + self.oegreso.bodegaEnvia)

         item = QtGui.QStandardItem(itemView)
         self.modelolista.appendRow(item)

         self.ui.id_prod_envio.clear()
         self.ui.nombre_producto_envio.clear()
         self.ui.cantidad_producto_envio.clear()
         self.ui.precio_unitario_envio.clear()


    def btn_guardar_lista_egreso(self):
    # Establece el nombre de archivo y la ubicación
        filepath = "C:/Users/jbren/OneDrive/Escritorio/Proyecto Program 2/Dominio/IngresoArticulos/lista_ingresos.txt"
        filepath2 = "C:/Users/jbren/OneDrive/Escritorio/Proyecto Program 2/Dominio/EgresoEntreBodegas/egresos_bodegas.txt"

    # Abre el archivo para escribir
        with open(filepath, "a") as f:
            # Escribe cada línea de la lista en el archivo de ingresos
            for row in range(self.modelolista.rowCount()):
                line = ""
                for col in range(self.modelolista.columnCount()):
                    item = self.modelolista.item(row, col)
                    if item is not None:
                        line += item.text() + ","
                line = line.rstrip(",") + "\n"
                f.write(line)

        # Abre el archivo para escribir
        with open(filepath2, "a") as f:
            # Escribe cada línea de la lista en el archivo de egresos
            for row in range(self.modelolista.rowCount()):
                line = ""
                for col in range(self.modelolista.columnCount()):
                    item = self.modelolista.item(row, col)
                    if item is not None:
                        line += item.text() + ","
                line = line.rstrip(",") + "\n"
                f.write(line)

    # Elimina todos los elementos de la lista
        self.modelolista.clear()      
        self.ui.label_19.clear()      
        self.actualizar_saldos()



        
    def actualizar_saldos(self):
        archivo = open('C:/Users/jbren/OneDrive/Escritorio/Proyecto Program 2/Dominio/IngresoArticulos/lista_ingresos.txt', 'r')
        cantidad_por_id_y_bodega = {}

        for linea in archivo:
            valores = linea.strip().split(',')
            id_articulo = valores[0]
            cantidad_recibida = int(round(float(valores[2])))
            bodega = valores[7]
            nombre_articulo = valores[1]
            precio_unitario = float(valores[3])
            clave = (id_articulo, bodega)
            if clave in cantidad_por_id_y_bodega:
                cantidad_por_id_y_bodega[clave]['cantidad'] += cantidad_recibida
            else:
                cantidad_por_id_y_bodega[clave] = {'cantidad': cantidad_recibida, 'nombre': nombre_articulo, 'precio': precio_unitario}

        archivo.close()
        
        for clave, valores in cantidad_por_id_y_bodega.items():
            print("->>> Ingreso <<<---")
            print(f'ID: {clave[0]},Nombre del producto: {valores["nombre"]},Cantidad recibida: {valores["cantidad"]},  Precio unitario: {valores["precio"]} Bodega Ingreso: {clave[1]} ')

        archivo = open('C:/Users/jbren/OneDrive/Escritorio/Proyecto Program 2/Dominio/EgresoEntreBodegas/egresos_bodegas.txt', 'r')
        cantidad_por_id_y_bodega = {}

        for linea in archivo:
            valores = linea.strip().split(',')
            id_articulo = valores[0]
            cantidad_egresada = int(round(float(valores[2])))
            bodega = valores[8]
            nombre_articulo = valores[1]
            precio_unitario = float(valores[3])
            clave = (id_articulo, bodega)
            if clave in cantidad_por_id_y_bodega:
                cantidad_por_id_y_bodega[clave]['cantidad'] += cantidad_egresada
            else:
                cantidad_por_id_y_bodega[clave] = {'cantidad': cantidad_egresada, 'nombre': nombre_articulo, 'precio': precio_unitario}

        archivo.close()

        for clave, valores in cantidad_por_id_y_bodega.items():
            print("->>> Egreso <<<---")
            print(f'ID: {clave[0]},Nombre del producto: {valores["nombre"]},Cantidad Egresada: {valores["cantidad"]},  Precio unitario: {valores["precio"]} Bodega Egreso: {clave[1]} ')
        

    
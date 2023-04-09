from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QMessageBox
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
        self.ui.id_prod_envio_r_distrib.textChanged.connect(self.buscar_saldos_distribuidores)
        self.ui.btnCrearBodega.clicked.connect(lambda :  self.agregar_bodega() and self.cargar_combobox())
        self.ui.btnEnviarBodegas.clicked.connect(self.btn_guardar_lista_egreso)
        self.cargar_combobox()
        self.cargar_combobox_bodega_entrega()
        self.cargar_combobox_distribuidores()
       



      
       

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
        filepath = "C:/Users/jbren/OneDrive/Escritorio/Proyecto Program 2/Dominio/BaseDatos/lista_ingresos.txt"
        mensaje = "Se guardo exitosamente"
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
        self.actualizar_saldos()
        self.mensaje_confirmacion(mensaje)
       
 
    

    def buscar_producto(self):
    # Obtiene el ID ingresado por el usuario
        id_producto = self.ui.cod_registro.text()        
        with open(r'C:\Users\jbren\OneDrive\Escritorio\Proyecto Program 2\Dominio\BaseDatos\lista_productos.txt', 'r') as f:
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
        mensaje = "Bodega Agregada"

        # Agregar los datos al archivo de texto
        archivo = "C:\\Users\\jbren\\OneDrive\\Escritorio\\Proyecto Program 2\\Dominio\\BaseDatos\\bodegas.txt"  # dirección del archivo
        nueva_bodega = nuevaBodega(archivo)
        nueva_bodega.agregar_datos(id, nombre, direccion, telefono)
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_10.clear()
        self.ui.lineEdit_6.clear()
        self.ui.lineEdit_8.clear()
        self.cargar_combobox()
        self.cargar_combobox_bodega_entrega()
        self.cargar_combobox_distribuidores()
        self.mensaje_confirmacion(mensaje)


    def cargar_combobox(self):
        archivo = "C:\\Users\\jbren\\OneDrive\\Escritorio\\Proyecto Program 2\\Dominio\\BaseDatos\\bodegas.txt"
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
        with open('C:/Users/jbren/OneDrive/Escritorio/Proyecto Program 2/Dominio/BaseDatos/Saldos.txt', 'r') as archivo:
            # Itera sobre las líneas del archivo
            for line in archivo:
                datos_producto = line.strip().split(',')
                if datos_producto[0] == id_producto:
                    # Si encontramos el producto, colocamos su nombre y precio en los QLineEdit correspondientes
                    self.ui.nombre_producto_envio.setText(datos_producto[1])
                    self.ui.precio_unitario_envio.setText(datos_producto[3])
                    self.ui.cantidad_disponible.setText(datos_producto[2])
                    return
            
    # Si no encontramos el producto, limpiamos los QLineEdit correspondientes
        self.ui.nombre_producto_envio.clear()
        self.ui.precio_unitario_envio.clear()
        self.ui.cantidad_disponible.clear()
  

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
        filepath = "C:/Users/jbren/OneDrive/Escritorio/Proyecto Program 2/Dominio/BaseDatos/lista_ingresos.txt"
        filepath2 = "C:/Users/jbren/OneDrive/Escritorio/Proyecto Program 2/Dominio/BaseDatos/egresos_bodegas.txt"
        mensaje = "Datos guardados satisfactoriamente"

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
        self.mensaje_confirmacion(mensaje)



        
    def actualizar_saldos(self):
        archivo = open('C:/Users/jbren/OneDrive/Escritorio/Proyecto Program 2/Dominio/BaseDatos/lista_ingresos.txt', 'r')
        cantidad_por_id_y_bodega = {}
        saldo_por_id_y_bodega = {}

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
            saldo_por_id_y_bodega[clave] = cantidad_por_id_y_bodega[clave]

        archivo.close()
        
        #for clave, valores in cantidad_por_id_y_bodega.items():
            #print("->>> Ingreso <<<---")
            #print(f'ID: {clave[0]},Nombre del producto: {valores["nombre"]},Cantidad recibida: {valores["cantidad"]},  Precio unitario: {valores["precio"]} Bodega Ingreso: {clave[1]} ')

        archivo = open('C:/Users/jbren/OneDrive/Escritorio/Proyecto Program 2/Dominio/BaseDatos/egresos_bodegas.txt', 'r')
        #cantidad_por_id_y_bodega = {}

        for linea in archivo:
            valores = linea.strip().split(',')
            id_articulo = valores[0]
            cantidad_egresada = int(round(float(valores[2])))
            bodega = valores[8]
            #nombre_articulo = valores[1]
            #precio_unitario = float(valores[3])
            clave = (id_articulo, bodega)
            saldo_por_id_y_bodega[clave]['cantidad'] -= cantidad_egresada

            #if clave in cantidad_por_id_y_bodega:
                #cantidad_por_id_y_bodega[clave]['cantidad'] += cantidad_egresada
            #else:
                #cantidad_por_id_y_bodega[clave] = {'cantidad': cantidad_egresada, 'nombre': nombre_articulo, 'precio': precio_unitario}

        archivo.close()

        #for clave, saldo in saldo_por_id_y_bodega.items():
            #if saldo['cantidad'] >= 0:
                #print(f'ID: {clave[0]},Nombre del producto: {saldo["nombre"]},Cantidad Saldo: {saldo["cantidad"]},  Precio unitario: {saldo["precio"]} Bodega Egreso: {clave[1]} ')
            #else:
                #print(f'ID: {clave[0]},Nombre del producto: {saldo["nombre"]},Cantidad Egreso: {abs(saldo["cantidad"])},  Precio unitario: {saldo["precio"]} Bodega Egreso: {clave[1]} ')

        # abrir el archivo para escritura
        with open('C:/Users/jbren/OneDrive/Escritorio/Proyecto Program 2/Dominio/BaseDatos/Saldos.txt', 'w') as archivo_salida:
            # recorrer las claves y saldos
            for clave, saldo in saldo_por_id_y_bodega.items():
                if saldo['cantidad'] >= 0:
                    linea = f'{clave[0]}, {saldo["nombre"]}, {saldo["cantidad"]}, {saldo["precio"]} , {clave[1]}\n'
                else:
                    linea = f'{clave[0]}, {saldo["nombre"]}, {abs(saldo["cantidad"])}, {saldo["precio"]} , {clave[1]}\n'
                archivo_salida.write(linea)
        
        

    def mensaje_confirmacion(self,mensaje):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg.setWindowTitle("Confirmación")
        msg.setText(mensaje)
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        msg.exec()
        return
    
    
    def cargar_combobox_bodega_entrega(self):
        archivo = "C:\\Users\\jbren\\OneDrive\\Escritorio\\Proyecto Program 2\\Dominio\\BaseDatos\\bodegas.txt"
        with open(archivo, 'r') as f:
            lines = f.readlines()

        bodegas = set()  # usar un set para eliminar duplicados
        for line in lines:
            data = line.strip().split(',')           
            bodega_recibe = data[1]        
            bodegas.add(bodega_recibe)

    
        self.ui.comboBox_bod_envia_3.clear()

        for bodega in bodegas:           
            self.ui.comboBox_bod_envia_3.addItem(bodega)



    def cargar_combobox_distribuidores(self):
        archivo = "C:\\Users\\jbren\\OneDrive\\Escritorio\\Proyecto Program 2\\Dominio\\BaseDatos\\distribuidores.txt"
        with open(archivo, 'r') as f:
            lines = f.readlines()

        distribuidores = set()  # usar un set para eliminar duplicados
        for line in lines:
            data = line.strip().split(',')           
            distribuidor_recibe = data[0]        
            distribuidores.add(distribuidor_recibe)

    
        self.ui.comboBox_distrib_recibe_3.clear()

        for distribuidor in distribuidores:           
            self.ui.comboBox_distrib_recibe_3.addItem(distribuidor)           
    

    def buscar_saldos_distribuidores(self):
        id_producto = self.ui.id_prod_envio_r_distrib.text()
        bodega = self.ui.comboBox_bod_envia_3.currentText()

        with open('C:/Users/jbren/OneDrive/Escritorio/Proyecto Program 2/Dominio/BaseDatos/Saldos.txt', 'r') as archivo:
            for line in archivo:
                datos_producto = line.strip().split(',')
                if datos_producto[0] == id_producto and datos_producto[4].strip() == bodega:
                    self.ui.nombre_producto_distrib.setText(datos_producto[1])
                    self.ui.precio_unitario_envio_distrib.setText(datos_producto[3])
                    self.ui.cantidad_producto_envio_distrib.setText(datos_producto[2])
                    return

        self.ui.nombre_producto_distrib.clear()
        self.ui.precio_unitario_envio_distrib.clear()
        self.ui.cantidad_producto_envio_distrib.clear()

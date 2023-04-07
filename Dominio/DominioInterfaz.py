from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow
from Interfaz.gestor_bodegas import Ui_MainWindow
from Dominio.IngresoArticulos import IngresoArticulos
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
        self.ui.pushButton_guardar.clicked.connect(self.btn_guardar_lista)
        self.modelolista = QtGui.QStandardItemModel()
        self.ui.listaIngreso.setModel(self.modelolista)
        self.ui.cod_registro.textChanged.connect(self.buscar_producto)
        self.ui.btnCrearBodega.clicked.connect(self.agregar_bodega)
        self.cargar_combobox()
       



        with open(r'C:\Users\jbren\OneDrive\Escritorio\Proyecto Program 2\Dominio\IngresoArticulos\lista_productos.txt', 'r') as f:
            self.lines = f.readlines()     
    
       

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
        self.ui.pushButton_crear_bodega.clicked.connect(self.mostrar_pagina)
        self.ui.pushButton_envio_bodega.clicked.connect(self.mostrar_pagina)
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

        itemView = (self.oingreso.codigoArticulo+"           "+self.oingreso.nombreArticulo+"                                     "
                    + "        " + str(self.oingreso.cantidad) + "            "+str(self.oingreso.preciounitario)+"              "+str(self.oingreso.montoTotal) +
                    "    " + self.ui.numeroFacturaIngreso.text() + "   " + fecha_actual_str)

        item = QtGui.QStandardItem(itemView)
        self.modelolista.appendRow(item)

        self.ui.cod_registro.clear()
        self.ui.nombre_registro.clear()
        self.ui.cantidad_registro.clear()
        self.ui.precio_un_registro.clear()

    

    def btn_guardar_lista(self):
        # Establece el nombre de archivo y la ubicación
        filename = "lista_ingresos.txt"
        filepath = "C:/Users/jbren/OneDrive/Escritorio/Proyecto Program 2/Dominio/IngresoArticulos/lista_ingresos.txt"

        # Abre el archivo para escribir
        with open(filepath, "a") as f:

            # Escribe cada línea de la lista en el archivo
            for row in range(self.modelolista.rowCount()):
                line = ""
                for col in range(self.modelolista.columnCount()):
                    item = self.modelolista.item(row, col)
                    if item is not None:
                        line += item.text() + "\t"
                line = line.rstrip("\t") + "\n"
                f.write(line)

        # Elimina todos los elementos de la lista
        self.modelolista.clear()
        self.ui.numeroFacturaIngreso.clear()

    def buscar_producto(self):
    # Obtiene el ID ingresado por el usuario
        id_producto = self.ui.cod_registro.text()
        
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
        nombre = self.ui.lineEdit_10.text()
        direccion = self.ui.lineEdit_8.text()
        telefono = self.ui.lineEdit_6.text()

        # Agregar los datos al archivo de texto
        archivo = "C:\\Users\\jbren\\OneDrive\\Escritorio\\Proyecto Program 2\\Dominio\\EgresoEntreBodegas\\bodegas.txt"  # dirección del archivo
        nueva_bodega = nuevaBodega(archivo)
        nueva_bodega.agregar_datos(id, nombre, direccion, telefono)
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_10.clear()
        self.ui.lineEdit_6.clear()
        self.ui.lineEdit_8.clear()


    def cargar_combobox(self):
        archivo = "C:\\Users\\jbren\\OneDrive\\Escritorio\\Proyecto Program 2\\Dominio\\EgresoEntreBodegas\\bodegas.txt"
        with open(archivo, 'r') as f:
            lines = f.readlines()

        bodegas = set()  # usar un set para eliminar duplicados
        for line in lines:
            data = line.strip().split(',')
            bodega_envia = data[1]
            bodega_recibe = data[1]
            bodegas.add(bodega_envia)
            bodegas.add(bodega_recibe)

        # Llenar los combobox con los nombres de las bodegas
        self.ui.comboBox_bod_envia.clear()
        self.ui.comboBox__bod_recibe.clear()

        for bodega in bodegas:
            self.ui.comboBox_bod_envia.addItem(bodega)
            self.ui.comboBox__bod_recibe.addItem(bodega)

  
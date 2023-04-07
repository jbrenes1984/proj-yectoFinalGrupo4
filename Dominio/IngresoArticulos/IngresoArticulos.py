

class IngresoArticulos : 
    def __init__(self) -> None:
        self.idfactura = None
        self.codigoArticulo = None
        self.nombreArticulo = None
        self.cantidad = None
        self.preciounitario = None
        self.montoTotal = None
        self.fecha = None

    def calcularMontoTotal(self):
        self.montoTotal = self.cantidad * self.preciounitario
        return self.montoTotal
    

    
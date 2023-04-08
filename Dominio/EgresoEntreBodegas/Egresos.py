
class EgresoArticulos: 
    def __init__(self) -> None:
        self.idfactura = None
        self.codigoArticulo = None
        self.nombreArticulo = None
        self.cantidad = None
        self.preciounitario = None
        self.montoTotal = None
        self.fecha = None
        self.bodegaEnvia = None
        self.bodegaRecibe = None
        self.factura = None
        self.cantidadDisponible = None

    def calcularMontoTotal(self):
        self.montoTotal = self.cantidad * self.preciounitario
        return self.montoTotal
    

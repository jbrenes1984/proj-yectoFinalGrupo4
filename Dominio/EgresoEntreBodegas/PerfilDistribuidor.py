class perfil_distribuidor:
    def __init__(self, archivo )-> None:
        self.archivo = archivo
    
    def agregar_distribuidor(self,nombre,ubicacion,telefono,cedula):
        with open(self.archivo,'a') as archivo:
            archivo.write(f'Dtb {nombre},{ubicacion},{telefono},{cedula}\n')

    
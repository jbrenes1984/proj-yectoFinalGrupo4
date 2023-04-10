class nuevaBodega:
    def __init__(self, archivo) -> None:
        self.archivo = archivo

    def agregar_datos(self, nombre, ubicacion, telefono):
        with open(self.archivo, 'a') as file:
            file.write(f'{nombre},{ubicacion},{telefono}\n')


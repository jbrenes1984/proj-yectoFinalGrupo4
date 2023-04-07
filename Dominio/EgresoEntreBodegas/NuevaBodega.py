class nuevaBodega :
    def __init__(self,archivo) -> None:
        self.archivo = archivo

    def agregar_datos(self, id, nombre, ubicacion,telefono):
        with open(self.archivo, 'a') as file:
            file.write(f'{id},{nombre},{ubicacion},{telefono}\n')
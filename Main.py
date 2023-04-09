import sys
from PyQt6 import QtWidgets
from Dominio.DominioInterfaz import FrmInterfaz


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = FrmInterfaz()
    window.show()
    sys.exit(app.exec())

import sys

from PyQt5.QtWidgets import QApplication

from ui_manager import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    coffee_info = MainWindow()
    coffee_info.show()

    sys.exit(app.exec_())

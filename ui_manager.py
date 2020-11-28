from PyQt5.QtCore import Qt

from coffee_info import CoffeeInfo, CoffeeInfoManager

from UI.ui_main import Ui_MainWindow
from UI.ui_addEditCoffeeForm import Ui_Dialog

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QDialog, QTableWidgetItem, QErrorMessage


class CoffeeInfoDialog(QDialog):
    def __init__(self, id=None, grade=None, roast=None, consistence=None,
                 taste=None, cost=None, volume=None, update=True, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.manager = CoffeeInfoManager()

        self.parent = parent
        self.update = update
        self.current_id = id

        self.dialog = Ui_Dialog()
        self.dialog.setupUi(self)

        if update:
            self.init_ui(id, grade, roast, consistence, taste, cost, volume)
        self.dialog.pushButton.clicked.connect(lambda: self.save())

    def init_ui(self, id, grade, roast, consistence, taste, cost, volume):
        self.dialog.id.setText(id)
        self.dialog.grade.setText(grade)
        self.dialog.roast.setText(roast)
        self.dialog.consistence.setText(consistence)
        self.dialog.taste.setText(taste)
        self.dialog.cost.setText(cost)
        self.dialog.volume.setText(volume)

    def get_values(self):
        return [self.dialog.id.text(), self.dialog.grade.text(),
                self.dialog.roast.text(), self.dialog.consistence.text(),
                self.dialog.taste.text(), self.dialog.cost.text(),
                self.dialog.volume.text()]

    def save(self):
        values = self.get_values()
        if self.update:
            self.manager.update(self.current_id, *self.get_values())
        else:
            error_message = QErrorMessage(self)
            if not values[0]:
                return error_message.showMessage("ID must not be empty")
            try:
                self.manager.insert(*self.get_values())
            except Exception:
                return error_message.showMessage("ID must be unique")

        self.parent.init_ui()
        self.done(0)


class MainWindow(QMainWindow):
    def __init__(self, currency="₽"):
        super().__init__()

        self.manager = CoffeeInfoManager()
        self.currency = currency

        self.main_window = Ui_MainWindow()
        self.main_window.setupUi(self)

        self.init_ui()

        self.main_window.tableWidget.cellDoubleClicked.connect(self.open_card)
        self.main_window.add_coffee_btn.clicked.connect(self.add_coffee)

    def init_ui(self):
        coffees = self.manager.get_coffees_info()

        self.main_window.tableWidget.setRowCount(len(coffees))
        self.main_window.tableWidget.setColumnCount(7)

        for idx, e in enumerate(coffees):
            self.main_window.tableWidget.setItem(idx, 0, QTableWidgetItem(str(e.get_id())))
            self.main_window.tableWidget.setItem(idx, 1, QTableWidgetItem(e.get_grade()))
            self.main_window.tableWidget.setItem(idx, 2, QTableWidgetItem(e.get_roast()))
            self.main_window.tableWidget.setItem(idx, 3, QTableWidgetItem(e.get_consistence()))
            self.main_window.tableWidget.setItem(idx, 4, QTableWidgetItem(e.get_taste()))
            self.main_window.tableWidget.setItem(idx, 5, QTableWidgetItem(str(e.get_cost())))
            self.main_window.tableWidget.setItem(idx, 6, QTableWidgetItem(str(e.get_volume())))

    def open_card(self, row, column):
        data = [self.main_window.tableWidget.item(row, i).text() for i in range(7)]

        dialog = CoffeeInfoDialog(*data, parent=self)
        dialog.show()

    def add_coffee(self):
        dialog = CoffeeInfoDialog(parent=self, update=False)
        dialog.show()
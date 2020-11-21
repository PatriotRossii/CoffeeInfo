from PyQt5.QtCore import Qt

from coffee_info import CoffeeInfo, CoffeeInfoManager

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

        uic.loadUi("addEditCoffeeForm.ui", self)
        if update:
            self.init_ui(id, grade, roast, consistence, taste, cost, volume)
        self.pushButton.clicked.connect(lambda: self.save())

    def init_ui(self, id, grade, roast, consistence, taste, cost, volume):
        self.id.setText(id)
        self.grade.setText(grade)
        self.roast.setText(roast)
        self.consistence.setText(consistence)
        self.taste.setText(taste)
        self.cost.setText(cost)
        self.volume.setText(volume)

    def get_values(self):
        return [self.id.text(), self.grade.text(), self.roast.text(), self.consistence.text(),
                self.taste.text(), self.cost.text(), self.volume.text()]

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

        uic.loadUi('main.ui', self)
        self.init_ui()

        self.tableWidget.cellDoubleClicked.connect(self.open_card)
        self.add_coffee_btn.clicked.connect(self.add_coffee)

    def init_ui(self):
        coffees = self.manager.get_coffees_info()

        self.tableWidget.setRowCount(len(coffees))
        self.tableWidget.setColumnCount(7)

        for idx, e in enumerate(coffees):
            self.tableWidget.setItem(idx, 0, QTableWidgetItem(str(e.get_id())))
            self.tableWidget.setItem(idx, 1, QTableWidgetItem(e.get_grade()))
            self.tableWidget.setItem(idx, 2, QTableWidgetItem(e.get_roast()))
            self.tableWidget.setItem(idx, 3, QTableWidgetItem(e.get_consistence()))
            self.tableWidget.setItem(idx, 4, QTableWidgetItem(e.get_taste()))
            self.tableWidget.setItem(idx, 5, QTableWidgetItem(str(e.get_cost())))
            self.tableWidget.setItem(idx, 6, QTableWidgetItem(str(e.get_volume())))

    def open_card(self, row, column):
        data = [self.tableWidget.item(row, i).text() for i in range(7)]

        dialog = CoffeeInfoDialog(*data, parent=self)
        dialog.show()

    def add_coffee(self):
        dialog = CoffeeInfoDialog(parent=self, update=False)
        dialog.show()
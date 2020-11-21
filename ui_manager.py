from PyQt5.QtCore import Qt

from coffee_info import CoffeeInfo, CoffeeInfoManager

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QDialog, QTableWidgetItem


class CoffeeInfoDialog(QDialog):
    def __init__(self, id, grade, roast, consistence, taste, cost, volume):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.init_ui(id, grade, roast, consistence, taste, cost, volume)
        self.pushButton.clicked.connect(lambda: self.done(0))

    def init_ui(self, id, grade, roast, consistence, taste, cost, volume):
        uic.loadUi("coffee_card.ui", self)

        self.id.setText(id)
        self.grade.setText(grade)
        self.roast.setText(roast)
        self.consistence.setText(consistence)
        self.taste.setText(taste)
        self.cost.setText(cost)
        self.volume.setText(volume)


class MainWindow(QMainWindow):
    def __init__(self, currency="₽"):
        super().__init__()

        self.manager = CoffeeInfoManager()
        self.currency = currency

        uic.loadUi('main.ui', self)
        self.init_ui()

        self.tableWidget.cellDoubleClicked.connect(self.open_card)

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
            self.tableWidget.setItem(idx, 5, QTableWidgetItem(str(e.get_cost()) + " {}".format(self.currency)))
            self.tableWidget.setItem(idx, 6, QTableWidgetItem(str(e.get_volume())))

    def open_card(self, row, column):
        data = [self.tableWidget.item(row, i).text() for i in range(7)]

        dialog = CoffeeInfoDialog(*data)
        dialog.show()

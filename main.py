import sys
import sqlite3

import addEditCoffeeForm
import main_window
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView


class CustomDialog(QMainWindow, addEditCoffeeForm.Ui_MainWindow):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.ex = args[1]
        self.con = args[2]
        self.comboBox.addItems(['Молотый', 'В зернах'])
        if len(args) == 4:
            self.parameters = list(args[-1])
            self.old()
        else:
            self.parameters = []
        self.pushButton.clicked.connect(self.accept)
        self.label_7.setVisible(False)

    def old(self):
        self.comboBox.clear()
        self.lineEdit.setText(self.parameters[1])
        self.spinBox.setValue(int(self.parameters[2]))
        self.comboBox.addItems(sorted(['Молотый', 'В зернах'],
                                      key=lambda x: x != self.parameters[3]))
        self.lineEdit_2.setText(self.parameters[4])
        self.spinBox_2.setValue(int(self.parameters[5]))
        self.doubleSpinBox.setValue(float(str(self.parameters[6]).replace(',', '.')))

    def accept(self):
        if not self.parameters:
            if self.lineEdit.text() != '' and self.lineEdit_2.text() != '':
                self.con.cursor().execute(
                    f"""
                                INSERT INTO Coffee (
                                Name, Fry, Grained, Taste, Price, Volume) Values('{
                    self.lineEdit.text()}', {
                    self.spinBox.value()}, '{
                    self.comboBox.currentText()}', '{
                    self.lineEdit_2.text()}', {
                    self.spinBox_2.value()}, {
                    self.doubleSpinBox.value()})""").fetchall()
                self.con.commit()
                self.label_7.setVisible(False)
            else:
                self.label_7.setText('Неверные данные')
                self.label_7.setVisible(True)
        else:
            if self.lineEdit.text() != '' and self.lineEdit_2.text() != '':
                self.con.cursor().execute(
                    f"""UPDATE Coffee SET Name = '{
                    self.lineEdit.text()}', Fry = {
                    self.spinBox.value()}, Grained = '{
                    self.comboBox.currentText()}', Taste = '{
                    self.lineEdit_2.text()}', Price = {
                    self.spinBox_2.value()}, Volume = {
                    round(self.doubleSpinBox.value(), 2)} WHERE Id = {
                    self.parameters[0]}""").fetchall()
                self.con.commit()
                self.label_7.setVisible(False)
            else:
                self.label_7.setText('Неверные данные')
                self.label_7.setVisible(True)

    def closeEvent(self, event):
        event.accept()
        self.ex.show()
        self.ex.select_data()


class MyWidget(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connection = sqlite3.connect("coffee.db")
        self.query = "SELECT * FROM Coffee"
        self.select_data()
        self.pushButton.clicked.connect(self.ad)
        self.pushButton_2.clicked.connect(self.ch)

    def select_data(self):
        res = self.connection.cursor().execute(self.query).fetchall()
        # Заполним размеры таблицы
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels([
            'ID', 'Название сорта', 'Степень обжарки',
            'Молотый/в зернах', 'Описание вкуса', 'Цена', 'Объем упаковки'])
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def ad(self):
        self.dlg = CustomDialog(self.connection, self, self.connection)
        self.hide()
        self.dlg.show()

    def ch(self):
        was = self.connection.cursor().execute(self.query).fetchall()[self.tableWidget.currentRow()]
        self.dlg = CustomDialog(self.connection, self, self.connection, was)
        self.hide()
        self.dlg.show()

    def closeEvent(self, event):
        self.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())

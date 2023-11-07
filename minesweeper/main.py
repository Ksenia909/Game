from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QApplication
from datetime import date
import sys

from mydesign import Ui_MainWindow
from beginnerdesign import Ui_Beginner
from intermediatedesign import Ui_Intermediate
from expertdesign import Ui_Expert
from game import GamePole
from connection import Data
from windesign import Ui_Win_window


class MyWindow(QMainWindow):
    LEVEL = [(9, 9, 10, 'Beginner'), (16, 16, 40, 'Intermediate'), (16, 30, 99, 'Expert')]

    def __init__(self):
        super(MyWindow, self).__init__()
        self.game_pole = self.flags = self.time = None
        self.ui_m = Ui_MainWindow()
        self.ui_m.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon/40782.png'))
        self.setStyleSheet('.QWidget {background-image: url(background/1.jpg);}')

        self.ui_m.btn_exit.clicked.connect(self.clicked_exit)
        self.ui_m.btn_rules.clicked.connect(self.clicked_rules)
        self.ui_m.btn_beginner.clicked.connect(self.clicked_beginner)
        self.ui_m.btn_interm.clicked.connect(self.clicked_intermediate)
        self.ui_m.btn_expert.clicked.connect(self.clicked_expert)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.show_time)

        self.conn = Data()

    def clicked_exit(self):
        sys.exit((app.exec()))

    def clicked_rules(self):
        rules = QMessageBox()
        rules.setWindowTitle('Rules')
        rules.setWindowIcon(QtGui.QIcon('icon/40782.png'))
        file1 = open('rules.txt')
        rules.setText(file1.read())
        rules.setIcon(QMessageBox.Information)
        file1.close()
        rules.exec_()

    def start_game(self, level):
        self.close()
        self.game_pole = GamePole(*self.LEVEL[level])
        self.flags = set()
        self.timer.stop()
        self.time = 0
        self.ui_m.lcdMines.display(self.LEVEL[level][2])

    def clicked_beginner(self):
        self.game_window = QtWidgets.QWidget()
        self.ui_m = Ui_Beginner()
        self.ui_m.setupUi(self.game_window)
        self.start_game(0)
        self.game_window.show()
        self.game_window.setStyleSheet('.QWidget {background-image: url(background/2.jpg);}')

        self.ui_m.Menu.clicked.connect(self.clicked_menu)
        self.ui_m.restart_game.clicked.connect(self.clicked_beginner)
        self.init_btn(0)

    def clicked_intermediate(self):
        self.game_window = QtWidgets.QWidget()
        self.ui_m = Ui_Intermediate()
        self.ui_m.setupUi(self.game_window)
        self.start_game(1)
        self.game_window.show()
        self.game_window.setStyleSheet('.QWidget {background-image: url(background/3.jpg);}')

        self.ui_m.Menu.clicked.connect(self.clicked_menu)
        self.ui_m.restart_game.clicked.connect(self.clicked_intermediate)
        self.init_btn(1)

    def clicked_expert(self):
        self.game_window = QtWidgets.QWidget()
        self.ui_m = Ui_Expert()
        self.ui_m.setupUi(self.game_window)
        self.start_game(2)
        self.game_window.show()
        self.game_window.setStyleSheet('.QWidget {background-image: url(background/4.jpg);}')

        self.ui_m.Menu.clicked.connect(self.clicked_menu)
        self.ui_m.restart_game.clicked.connect(self.clicked_expert)
        self.init_btn(2)

    def init_btn(self, level):
        n, m = self.LEVEL[level][:2]
        for i in range(n*m):
            self.ui_m.__dict__[f'pushButton_{str(i)}'].clicked.connect(self.handle_button)

    def clicked_menu(self):
        self.game_window.close()
        self.show()

    def handle_button(self):
        modifiers = QApplication.keyboardModifiers()
        num = int(self.sender().objectName().split('_')[1])
        w = self.game_pole.size_m

        if self.game_pole.start:
            self.game_pole.start = False
            self.game_pole.init_pole(num)
            self.timer.start(1000)

        cell = self.game_pole.pole[num // w][num % w]

        if modifiers == Qt.ControlModifier:
            self.clicked_flag(cell, num)
        else:
            self.clicked_btn(num, w, cell)

    def clicked_flag(self, cell, num):
        if cell.is_flag:
            self.ui_m.__dict__[f'pushButton_{str(num)}'].setIcon(QtGui.QIcon())
            self.ui_m.lcdMines.display(self.ui_m.lcdMines.intValue() + 1)
            self.flags.remove(num)
        else:
            self.ui_m.__dict__[f'pushButton_{str(num)}'].setIcon(QtGui.QIcon('icon/5443213.png'))
            self.ui_m.lcdMines.display(self.ui_m.lcdMines.intValue() - 1)
            self.flags.add(num)
            if self.flags == set(self.game_pole.mines):
                self.victory()

        cell.is_flag = not cell.is_flag

    def clicked_btn(self, num, w, cell):
        if not cell.is_open:
            if cell.is_mine:
                self.game_over()
            else:
                if cell.number != 0:
                    self.open_cell(cell, num)
                else:
                    h = self.game_pole.size_n
                    self.open_zero(cell, num, h, w)

    def open_zero(self, cell, num, h, w):
        if not (cell.is_open or cell.is_mine):
            self.open_cell(cell, num)
            for i, j in GamePole.INDX:
                if 0 <= num // w + i < h and 0 <= num % w + j < w:
                    num2 = w * i + j + num
                    cell2 = self.game_pole.pole[num2//w][num2%w]
                    if cell2.number == 0:
                        self.open_zero(cell2, num2, h, w)
                    self.open_cell(cell2, num2)

    def open_cell(self, cell, btn):
        if cell.is_flag:
            self.clicked_flag(cell, btn)
        cell.is_open = True
        self.ui_m.__dict__[f'pushButton_{str(btn)}'].setEnabled(False)
        self.ui_m.__dict__[f'pushButton_{str(btn)}'].setFlat(True)
        self.ui_m.__dict__[f'pushButton_{str(btn)}'].setText(str(cell.number))
        self.ui_m.__dict__[f'pushButton_{str(btn)}'].setFont(QtGui.QFont("Kristen ITC", 12))
        self.ui_m.__dict__[f'pushButton_{str(btn)}'].setStyleSheet("QPushButton { color: white;}");


    def game_over(self):
        self.timer.stop()
        self.ui_m.label_2.setVisible(True)
        self.ui_m.restart_game.setIcon(QtGui.QIcon('icon/2341909.png'))
        for i in self.game_pole.mines:
            self.ui_m.__dict__[f'pushButton_{i}'].setIcon(QtGui.QIcon('icon/4357187.png'))
            self.ui_m.__dict__[f'pushButton_{i}'].setEnabled(False)                       #прозрачность бомбы

    def show_time(self):
        self.time += 1
        self.ui_m.lcdTime.display(self.time)

    def victory(self):
        self.timer.stop()
        time = self.time
        level = self.game_pole.level
        today = str(date.today())

        if self.conn.get_level(level):
            id, best_date, best_time = self.conn.get_level(level)
            if int(best_time) > time:
                self.conn.update_result_query(level, today, time, id)
        else:
            self.conn.add_new_result_query(level, today, time)


        self.ui_m.restart_game.setIcon(QtGui.QIcon('icon/7626785.png'))
        for i in self.game_pole.mines:
            self.ui_m.__dict__[f'pushButton_{i}'].setEnabled(False)

        self.win()

    def win(self):
        self.win_window = QtWidgets.QDialog()
        self.ui_m = Ui_Win_window()
        self.ui_m.setupUi(self.win_window)
        id, best_date, best_time = self.conn.get_level(self.game_pole.level)
        self.ui_m.label_time1.setText(f'{self.time} sec.')
        self.ui_m.label_time1.setFont(QtGui.QFont("Times", 14))
        self.ui_m.label_time2.setText(f'{best_time} sec.')
        self.ui_m.label_time2.setFont(QtGui.QFont("Times", 14))
        self.ui_m.label_date.setText(best_date)
        self.ui_m.label_date.setFont(QtGui.QFont("Times", 14))
        self.win_window.show()





app = QApplication(sys.argv)
application = MyWindow()
application.show()

sys.exit(app.exec())


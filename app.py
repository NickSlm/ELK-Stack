from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from gui import UI_MainWindow

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = UI_MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
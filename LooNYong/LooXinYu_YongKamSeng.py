import sys
from PyQt5.QtWidgets import QDialog, QApplication,QSplashScreen,QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import time
import src.latest300 as las
class SplashScreen(QSplashScreen):
    def __init__(self):
        super(QSplashScreen,self).__init__()

        loadUi("splash.ui",self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        
    def progress(self):
        for i in range(100):
            time.sleep(0.005)
            self.progressBar.setValue(i)


class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()
        app = QApplication(sys.argv)
        ex = las.Ui_MainWindow()
        ex.show()
        sys.exit(app.exec_())

if __name__=='__main__':
    app=QApplication(sys.argv)
    splash=SplashScreen()
    splash.show()
    splash.progress()

    window=MainPage()
    splash.finish(window)
    app.exec_()


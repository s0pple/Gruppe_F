from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import os

class HotelCreationUI(QMainWindow):
    def __init__(self):
        super(HotelCreationUI, self).__init__()
        uic.loadUi(r'C:\Users\s0pple\Documents\GitHub\Gruppe_F\gui\hotel_creation.ui', self)
        self.show()

class HotelSearchUI(QMainWindow):
    def __init__(self):
        super(HotelSearchUI, self).__init__()
        uic.loadUi(r'C:\Users\s0pple\Documents\GitHub\Gruppe_F\gui\hotel_search.ui', self)
        self.show()

print(os.getcwd())

app = QApplication(sys.argv)
window1 = HotelCreationUI()
window2 = HotelSearchUI()
sys.exit(app.exec_())
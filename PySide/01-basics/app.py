#===========================================================
    # file    : app.py
    # brief   : Pysideテスト
    # author  : @akitsuki-35（https://github.com/akitsuki-35）
    # date    : 2026/06/16
    # updated : 2026/06/16
#===========================================================
import sys
from PySide6.QtWidgets import QApplication, QMainWindow

app = QApplication(sys.argv);

window = QMainWindow();
window.show();

app.exec();
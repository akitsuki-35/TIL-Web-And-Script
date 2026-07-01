#===========================================================
    # file    : titleChange.py
    # brief   : ウィンドウタイトル変更
    # author  : @akitsuki-35（https://github.com/akitsuki-35）
    # date    : 2026/06/23
    # updated : 2026/06/23
#===========================================================
import sys
from random import choice
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

# ウィンドウタイトルの候補
windowTitles = [
    "Synchrogazer",
    "Vitalization",
    "Exterminate",
    "TESTAMENT",
    "METANOIA"
]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.clickedTime = 0

        self.setWindowTitle("App")

        # 押したらウィンドウタイトルが変わるボタン
        button = QPushButton("タイトル変更")
        button.clicked.connect(self.isClicked)

        self.setCentralWidget(button)

    # ボタンがクリックされた時の動作
    def isClicked(self):
        print("クリックされました")
        newWindowTitle = choice(windowTitles)
        print("タイトルが %s に変更されました" % newWindowTitle)
        self.setWindowTitle(newWindowTitle)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
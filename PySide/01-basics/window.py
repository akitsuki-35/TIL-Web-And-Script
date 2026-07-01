#===========================================================
    # file    : window.py
    # brief   : メインウィンドウ作成
    # author  : @akitsuki-35（https://github.com/akitsuki-35）
    # date    : 2026/06/16
    # updated : 2026/06/16
#===========================================================
import sys
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

# ウィンドウサイズ定義
WIDTH = 1280
HEIGHT = 720

# メインウィンドウクラス作成
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # ウィンドウタイトル
        self.setWindowTitle("Test")

        # ボタン作成
        button = QPushButton("これはボタンです")

        # アプリ中央に配置する
        self.setCentralWidget(button)

        # ウィンドウを固定サイズズズにする
        self.setFixedSize(WIDTH, HEIGHT)

# アプリケーション インスタンス生成
app = QApplication(sys.argv)

# ウィンドウ表示
window = MainWindow()
window.show()

# イベントループ開始
app.exec()
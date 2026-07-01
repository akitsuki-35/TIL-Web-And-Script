#===========================================================
    # file    : main.py
    # brief   : Pysideテスト
    # author  : @akitsuki-35（https://github.com/akitsuki-35）
    # date    : 2026/06/16
    # updated : 2026/06/16
#===========================================================
import sys
from PySide6.QtWidgets import QApplication, QMainWindow

# メインウィンドウのクラス
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6")
        self.resize(1280, 720)

# アプリケーションを実行する処理
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
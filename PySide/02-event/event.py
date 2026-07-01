#===========================================================
    # file    : event.py
    # brief   : イベント
    # author  : @akitsuki-35（https://github.com/akitsuki-35）
    # date    : 2026/06/23
    # updated : 2026/06/23
#===========================================================
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

# ボタンの動作チェック
class MainWindowA(QMainWindow):
    def __init__(self):
        super().__init__()

        # ボタン状態を初期設定
        self.isButtonEnable = True

        self.setWindowTitle("App")

        # ボタン作成
        button = QPushButton("これはボタンです")
        button.setCheckable(True)

        # クリックした時の動作
        button.clicked.connect(self.buttonClicked)
        button.clicked.connect(self.buttonEnable)
        button.released.connect(self.buttonReleased)

        # アプリ中央に配置する
        self.setCentralWidget(button)

    # ボタンクリック時の関数
    def buttonClicked(self):
        print("クリックされたよ")

    # ボタンの有効・無効を出力
    def buttonEnable(self, checked):
        # ボタン状態取得
        self.isButtonEnable = checked
        print("ボタン状態", checked)

    # ボタンが離された
    def buttonReleased(self):
        print("離されたよ")

# クリックしたら無効になるボタン
class MainWindowB(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("App")

        self.button = QPushButton("これはボタンです")
        self.button.clicked.connect(self.the_button_was_clicked)

        self.setCentralWidget(self.button)

    def the_button_was_clicked(self):
        self.button.setText("You already clicked me.")
        self.button.setEnabled(False)

        # ウィンドウタイトル変更
        self.setWindowTitle("OneShot App")

app = QApplication(sys.argv)

window = MainWindowB()
window.show()

app.exec()
#===========================================================
    # file    : textfilemanager.py
    # brief   : テキスト読み込みと書き出し
    # author  : @akitsuki-35（https://github.com/akitsuki-35）
    # date    : 2026/06/24
    # updated : 2026/06/24
#===========================================================
import maya.cmds as cmds

# --------------------
# 書き出し
# --------------------
def textFileExport():
    textFilePath = r""

    selection = cmds.ls(sl=True)
    with open(textFilePath, "w",encoding="utf-8") as f:
        for obj in selection:

            f.write(obj + "\n")

# --------------------
# 読み込み
# --------------------
def textFileImport():
    textFilePath = r""

    num = 0

    with open(textFilePath, "r",encoding="utf-8") as f:

        textList= f.read().splitlines()

    for text in textList:
        num += 1
        if "Ru" in text:
            print(text)

    print(num)

# --------------------
# 加工して書き出し
# --------------------
def textFileReplace():
    textFilePath = r""

    with open(textFilePath, "r",encoding="utf-8") as f:

        textList= f.read().splitlines()

    for text in textList:
        newText = text.replace(text, "Code_" + text)
        print(newText)

    textFilePath = ""
    with open(textFilePath, "w",encoding="utf-8") as f:
        for text in textList:
            newText = text.replace(text, "Code_" + text)
            f.write(newText + "\n")

textFileImport()
#===========================================================
    # file    : stack.py
    # brief   : エラー解決
    # author  : @akitsuki-35（https://github.com/akitsuki-35）
    # date    : 2026/06/03
    # updated : 2026/06/03
#===========================================================
def funcA():
    funcB()

def funcB():
    funcC()

def funcC():
    print("test")

funcA()

# Mayaのエラー解決
def getSelection():

    selection = cmds.ls(sl=True)

    if selection:
        return selection[0]
    else:
        return False

def deleteObject():

    obj = getSelection()

    if obj:
        cmds.delete(obj)
    else:
        print("選択されているオブジェクトがありません")

deleteObject()
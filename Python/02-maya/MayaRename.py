#===========================================================
    # file    : MayaRename.py
    # brief   : リネームツール
    # author  : @akitsuki-35（https://github.com/akitsuki-35）
    # date    : 2026/06/17
    # updated : 2026/06/24
#===========================================================
import maya.cmds as cmds
if cmds.window("Sample_Window", exists=True):
    cmds.deleteUI("Sample_Window")
window = cmds.window("Sample_Window", title="Rename Tool", widthHeight=(700, 700))

# ====================
# 関数定義
# ====================
# --------------------
# リネーム実行
# --------------------
def Rename():
    # 文字列の置き換え
    replaceOld = cmds.textField("textfieldReplaceOld", query=True, text=True)
    replaceNew = cmds.textField("textfieldReplaceNew", query=True, text=True)
    
    # 先頭に追加する文字列
    prefix = cmds.textField("textfieldPrefix", query=True, text=True)
    
    # 末尾に追加する文字列
    suffix = cmds.textField("textfieldSuffix", query=True, text=True)
    
    # 検索する文字列
    search = cmds.textField("textfieldSearch", query=True, text=True)
    
    # 名前変更
    select = cmds.ls(sl=True)
    for sel in select:
        newName = prefix +  sel.replace(replaceOld, replaceNew)
        cmds.rename(sel, newName + suffix) 
        
    # 文字列検索
        if search:
            print("----------文字列検索結果ーーーーーーーーーー")
            for sel in select:
                if search in sel:
                    print(sel)

# --------------------
# 番号付け
# --------------------
def Number():

    # 選択中オブジェクト取得
    selectList = cmds.ls(sl=True)

    # 最初に選択したオブジェクトの名前を取り出す
    baseName = selectList[0]

    num = 1

    for sel in selectList:
        print(baseName + "_0" + str(num))
        cmds.rename(sel, baseName + "_0" + str(num))
        num += 1

# ====================
# UI部分
# ====================

# --------------------
# 実行ボタン
# --------------------

cmds.columnLayout("columnExecution", adjustableColumn=True)

cmds.text("textRename", label="リネーム ツール", h=50)

cmds.button("buttonExecution", label="リネーム実行", command=lambda *args:Rename(), h=50)

cmds.separator(height=20)

# --------------------
# 書き換え
# --------------------

cmds.text("textReplace", label="書き換え", h=30)

cmds.setParent("..")

cmds.rowLayout("rowReplace", numberOfColumns=3)

cmds.textField("textfieldReplaceOld", text="", w=200)
cmds.textField("textfieldReplaceNew", text="", w=200)

cmds.separator(height=20)
cmds.setParent("..")

# --------------------
# 頭に文字列追加
# --------------------
cmds.columnLayout("columnPrefix", adjustableColumn=True)

cmds.separator(height=20)
cmds.text("textPrefix", label="先頭に文字列追加", h=30)

cmds.textField("textfieldPrefix", text="", w=200)

cmds.separator(height=20)
cmds.setParent("..")

# --------------------
# 末尾に文字列追加
# --------------------
cmds.columnLayout("columnSuffix", adjustableColumn=True)

cmds.separator(height=20)
cmds.text("textSuffix", label="末尾に文字列追加", h=30)

cmds.textField("textfieldSuffix", text="", w=200)

cmds.separator(height=20)
cmds.setParent("..")

# --------------------
# 文字列検索
# --------------------
cmds.columnLayout("columnSearch", adjustableColumn=True)

cmds.separator(height=20)
cmds.text("textSearch", label="文字列検索", h=30)

cmds.textField("textfieldSearch", text="", w=200)

cmds.separator(height=20)
cmds.setParent("..")

# --------------------
# 番号付け
# --------------------
cmds.columnLayout("columnNumber", adjustableColumn=True)

cmds.button("buttonNumber", label="番号付け", command=lambda *args:Number())

cmds.setParent("..")

# --------------------
# 終了
# --------------------

cmds.setParent("..")# レイアウト終了
cmds.showWindow(window)
#===========================================================
    # file    : MayaUI.py
    # brief   : cmdsUI試作
    # author  : @akitsuki-35（https://github.com/akitsuki-35）
    # date    : 2026/06/10
    # updated : 2026/06/10
#===========================================================
import maya.cmds as cmds

# --------------------
# 関数定義
# --------------------
def PrintTextA():
    print("喪失までのカウントダウン")
    print("羽撃きは鋭く、風切る如く")
    print("銃爪にかけた指で夢をなぞる")

def PrintTextB():
    print("溢れはじめる秘めた熱情")
    print("夜を引き裂く曙光のごとく")
    print("純心は突き立つ牙となり")

def Stairs():
    width = 3; # 階段の幅
    height = 30; # 階段の段数
    
    for i in range(width):
        for j in range(height):
            cName = "cube_" + str(i) + "_" + str(j + 1);
            cmds.polyCube(name = cName); # キューブ生成
            cmds.setAttr(cName + ".translateZ", i); # Z軸移動
            cmds.setAttr(cName + ".translateX", j + 1); # X軸移動
            cmds.setAttr(cName + ".translateY", j + 1); # Y軸移動
            print(i, j); # （デバッグ用）numを出力

def Rename():
    input = cmds.textField("UserInput", query=True, text=True)
    select = cmds.ls(sl=True)
    for sel in select:
        cmds.rename(sel, sel + input) 

if cmds.window("Sample_Window", exists=True):
    cmds.deleteUI("Sample_Window")
window = cmds.window("Sample_Window", title="Sample_Window", widthHeight=(400, 700))

"ここにUIコードを入れる"

# --------------------
# 縦並びレイアウト
# --------------------

cmds.columnLayout("myColumn", adjustableColumn=True)

cmds.text("myText", label="サンプルテキスト", h=50) # テキストラベル挿入
cmds.separator(height=20) # セパレータ挿入

cmds.button("Button1", label="A", h=50, w=100, command=lambda *args:PrintTextA())

cmds.separator(height=20) # セパレータ挿入

cmds.button("Button2", label="B", h=50, w=100, command=lambda *args:PrintTextB())

cmds.setParent("..")

# --------------------
# 横並びレイアウト
# --------------------
cmds.rowLayout("myRow", numberOfColumns=5)

cmds.button("Synchrogazer", label="Synchrogazer", h=50, w=100, command=lambda *args:Stairs())
cmds.button("Vitalization", label="Vitalization", h=50, w=100, command=lambda *args:Rename())
cmds.button("Exterminate", label="Exterminate", h=50, w=100)
cmds.button("TESTAMENT", label="TESTAMENT", h=50, w=100)
cmds.button("METANOIA", label="METANOIA", h=50, w=100)

cmds.setParent("..")

# --------------------
# 縦並びレイアウト
# --------------------

cmds.columnLayout("TextInput", adjustableColumn=True)

cmds.separator(height=20) # セパレータ挿入

cmds.textField("UserInput", text="テキスト入力", w=200) # テキストボックス挿入


cmds.setParent("..")

cmds.setParent("..")#レイアウトから外に出る
cmds.showWindow(window)
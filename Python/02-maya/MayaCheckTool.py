#===========================================================
    # file    : getNode.py
    # brief   : mayaのノード取得
    # author  : @akitsuki-35（https://github.com/akitsuki-35）
    # date    : 2026/05/27
    # updated : 2026/05/27
#===========================================================
import maya.cmds as cmds

# --------------------
# 不要オブジェクトチェック
# --------------------

scenePath = cmds.file(q=True, sceneName=True)

sceneName = scenePath.split("/")[-1].split(".")[0]

if cmds.objExists(sceneName) == True:
    print("True")
    childNodes = cmds.listRelatives(sceneName, allDescendents=True, fullPath=True)
    nodeTypes = ["transform", "joint", "mesh", "locator"]
    
    for node in childNodes:
        if cmds.nodeType(node) == "transform":
            continue
        if cmds.nodeType(node) == "joint":
            continue
        if cmds.nodeType(node) == "mesh":
            continue
        if cmds.nodeType(node) == "locator":
            continue       
        print(node.split("|")[-1])
    
elif cmds.objExists(sceneName) == False:
    print("False")

# --------------------
# アニメーションチェック
# --------------------

anim = cmds.ls(type="animCurve")
if anim:
    print("アニメーションカーブが存在");
    for animCurve in anim:
        print(animCurve)

# --------------------
# ネームスペースチェック
# --------------------

allNodes = cmds.ls()

for node in allNodes:
    if ":" in node:
        print(node)

# --------------------
# 関数定義
# --------------------
def result(plusText):
    text = cmds.scrollField("checkToolsResultField",
                    q=True, text=True)
    cmds.scrollField("checkToolsResultField",
                    edit=True, text=text + "\n" + plusText)

def checkAnim():
    anim = cmds.ls(type="animCurve")
    if anim:
        print("アニメーションカーブが存在");
        for animCurve in anim:
            print(animCurve);

if cmds.window("Check Tools", exists=True):
    cmds.deleteUI("Check Tools")
window = cmds.window("Check Tools", title="Check Tools", widthHeight=(400, 700))

"ここにUIコードを入れる"

# --------------------
# 縦並びレイアウト
# --------------------

cmds.columnLayout("checkToolColumn", adjustableColumn=True)

cmds.button("checkToolButton", label="チェック開始", h=50, command=lambda *args:checkAnim())
cmds.scrollField("checkToolsResultField", text="-----結果-----",h=400)

cmds.setParent("..")

# --------------------
# 終了
# --------------------

cmds.showWindow(window)
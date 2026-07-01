#===========================================================
    # file    : stairs.py
    # brief   : Mayaで階段生成
    # author  : @akitsuki-35（https://github.com/akitsuki-35）
    # date    : 2026/05/20
    # updated : 2026/05/20
#===========================================================
import maya.cmds as cmds;

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
#===========================================================
    # file    : getNode.py
    # brief   : mayaのノード取得
    # author  : @akitsuki-35（https://github.com/akitsuki-35）
    # date    : 2026/05/27
    # updated : 2026/05/27
#===========================================================
import maya.cmds as cmds;

# ノードの取得
nodeList = cmds.ls(selection=True);

# アトリビュートの値を取得
nodeList = cmds.ls(selection=True);
for node in nodeList:
    v =  cmds.getAttr(node + ".translate");
    print(v);

v = cmds.getAttr(nodeList[1] + ".translate")[0];
cmds.setAttr(nodeList[0] + ".translate", v[0], v[1], v[2]);

# ファイル名取得
Path = cmds.file(q=True, sceneName=True);
name = Path.split("/")[-1];
print(Path);

# オブジェクトのリネーム
nodeList = cmds.ls(selection=True);
for sel in nodeList:
   cmds.rename(sel , sel.replace("pCube","Cube"));
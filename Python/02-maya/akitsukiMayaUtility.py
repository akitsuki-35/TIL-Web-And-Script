#===========================================================
    # file    : akitsukiMayaUtility.py
    # brief   : 制作効率化用Mayaツール
    # author  : @akitsuki-35（https://github.com/akitsuki-35）
    # date    : 2026/08/14
    # updated : 2026/08/14
#===========================================================
import maya.cmds as cmds

# --------------------
# 移動・回転・縮小をミラー適用
# --------------------
def mirror():
    # 選択オブジェクト取得
    sel = cmds.ls(sl=True)
    
    if not sel:
        addLog("error:オブジェクトが選択されていません")
        return
    elif len(sel) > 1:
        addLog("error:複数のオブジェクトが選択されています 1つのみ選択してください")
    
    curObject = sel[0]
    
    # 対称オブジェクト取得
    mirObject, mirObjPos = getMirrorObject()
    
    if not mirObject:
        addLog("error:対称オブジェクトが存在しません")
        return
    
    # モード取得
    mode = cmds.radioButtonGrp("mirrorType", query=True, select=True)
    
    # 変形適用軸取得
    mirrorAxis = cmds.checkBoxGrp("axis", query=True, valueArray3=True)
    
    if not any(mirrorAxis):
        addLog("error:適用軸が指定されていません")
        return
    
    # 変形量取得
    value = cmds.floatSliderGrp("valueSlider", query=True, value=True)
    
    # 移動
    if mode == 1:
        curObjPos = cmds.getAttr(f"{curObject}.translate")[0]
        newPos = [curObjPos[0], curObjPos[1], curObjPos[2]]
        
        # X軸
        if mirrorAxis[0]:
            newPos[0] += value
        # Y軸
        if mirrorAxis[1]:
            newPos[1] += value
        # Z軸
        if mirrorAxis[2]:
            newPos[2] += value
        
        # 選択オブジェクト移動処理
        cmds.setAttr(f"{curObject}.translate", newPos[0], newPos[1], newPos[2])
        
        # 対称オブジェクト移動処理
        cmds.setAttr(f"{mirObject}.translate", -newPos[0], -newPos[1], -newPos[2])
        
        addLog("success:移動処理が正常に完了しました")
    
    # 回転
    elif mode == 2:
        curObjRot = cmds.getAttr(f"{curObject}.rotate")[0]
        newRot = [curObjRot[0], curObjRot[1], curObjRot[2]]
        
        # X軸
        if mirrorAxis[0]:
            newRot[0] += value
        # Y軸
        if mirrorAxis[1]:
            newRot[1] += value
        # Z軸
        if mirrorAxis[2]:
            newRot[2] += value
        
        # 選択オブジェクト回転処理
        cmds.setAttr(f"{curObject}.rotate", newRot[0], newRot[1], newRot[2])
        
        # 対称オブジェクト移動処理
        cmds.setAttr(f"{mirObject}.rotate", -newRot[0], -newRot[1], -newRot[2])
        
        addLog("success:回転処理が正常に完了しました")
        
    # 拡大縮小
    elif mode == 3:
        curObjScale = cmds.getAttr(f"{curObject}.scale")[0]
        newScale = [curObjScale[0], curObjScale[1], curObjScale[2]]
        
        # X軸
        if mirrorAxis[0]:
            newScale[0] += value
        # Y軸
        if mirrorAxis[1]:
            newScale[1] += value
        # Z軸
        if mirrorAxis[2]:
            newScale[2] += value
        
        # 選択オブジェクト拡大縮小処理
        cmds.setAttr(f"{curObject}.scale", newScale[0], newScale[1], newScale[2])
        
        # 対称オブジェクト拡大縮小処理
        cmds.setAttr(f"{mirObject}.scale", -newScale[0], -newScale[1], -newScale[2])
        
        addLog("success:拡大縮小処理が正常に完了しました")
        
# --------------------
# 対称位置に複製
# --------------------
def objectDuplicate():
     # 選択オブジェクト取得
    sel = cmds.ls(sl=True)
    
    if not sel:
        addLog("error:オブジェクトが選択されていません")
        return
        
    # 変形適用軸取得
    mirrorAxis = cmds.checkBoxGrp("axis", query=True, valueArray3=True)
        
    for s in sel:
        pos = cmds.getAttr(f"{s}.translate")[0]
        newPos = list(pos)

        if not any(pos):
            addLog("warning:オブジェクトの移動値が0です 同じ位置に複製されます")
        elif not any(mirrorAxis):
            addLog("error:適用軸が指定されていません")
            return
        
        # X軸
        if mirrorAxis[0]:
            newPos[0] = -pos[0]
        # Y軸
        if mirrorAxis[1]:
            newPos[1] = -pos[1]
        # Z軸
        if mirrorAxis[2]:
            newPos[2] = -pos[2]
            
        newObj = cmds.duplicate(s, returnRootsOnly=True)
        cmds.setAttr(f"{newObj[0]}.translate", *newPos)
        addLog("success:複製が正常に完了しました")
        
# --------------------
# 対称オブジェクト取得
# --------------------
def getMirrorObject():
    sel = cmds.ls(sl=True)
    if not sel:
        return 0, 0

    curObject = sel[0]

    # 選択オブジェクト取得
    curObjPos = cmds.getAttr(f"{curObject}.translate")[0]

    # 選択オブジェクト対称位置取得
    mirObjPos = [-pos for pos in curObjPos]

    # メッシュを持つトランスフォームの親を格納
    meshObjs = list({cmds.listRelatives(m, parent=True)[0] for m in cmds.ls(type="mesh")})

    # 対称位置のオブジェクトを検索
    mirObject = [obj for obj in meshObjs if obj != sel[0] and cmds.getAttr(f"{obj}.translate")[0] == tuple(mirObjPos)]

    if mirObject:
        return mirObject[0], mirObjPos
    else:
        return 0, 0

# --------------------
# ログ出力
# --------------------
def addLog(newText):
    text = cmds.scrollField("log", query=True, text=True)
    
    if text:
        updatedText = f"{text.rstrip()}\n{newText}\n"
    else:
        updatedText = f"{newText}\n"
    
    cmds.scrollField("log", edit=True, text=updatedText)
    cmds.scrollField("log", edit=True, insertionPosition=len(updatedText))

# --------------------
# ログをクリア
# --------------------
def logClear():
    cmds.scrollField("log", edit=True, text="")

# --------------------
# ウィンドウ定義
# --------------------
if cmds.window("Sample_Window", exists=True):
    cmds.deleteUI("Sample_Window")
window = cmds.window("Sample_Window", title="akitsuki Maya Utility", widthHeight=(400, 700))

# --------------------
# ツールをタブ切り替えに対応
# --------------------
cmds.tabLayout("toolTab", innerMarginWidth=5, innerMarginHeight=5)

# --------------------
# ミラーツール
# --------------------
# カラムレイアウト作成
cmds.columnLayout("mirrorTool", adjustableColumn=True)

# タブにアサイン
cmds.tabLayout("toolTab", edit=True, tabLabel=[("mirrorTool", u"Mirror")])

# ヘッダテキスト
cmds.text("mirrorHeader", label="Mirror Tool", h=20)
cmds.text("mirrorHeader2", label="対称オブジェクトに処理をミラー", h=20)

# セパレータ
cmds.separator(h=5)

# モード指定
cmds.text("modeText", label="　移動・回転・拡縮のモード指定", h=30, align='left')
cmds.radioButtonGrp("mirrorType", numberOfRadioButtons=3, labelArray3=["Move", "Rotation", "Scaling"], select=1)
cmds.separator(h=5)

# 変形適用軸指定
cmds.text("axisText", label="　変形を適用する軸を指定", h=30, align='left')
cmds.checkBoxGrp("axis", numberOfCheckBoxes=3, labelArray3=["X", "Y", "Z"])
cmds.separator(h=5)

# 変形適用量指定
cmds.text("valueText", label="　変形を適用する量を指定", h=30, align='left')
cmds.floatSliderGrp("valueSlider", label="Value", field=True, minValue=-100, maxValue=100, value=0.1)
cmds.separator(h=30)

# 適用
cmds.button("mirrorButton", label="適用", h=50, command=lambda *args:mirror())
cmds.separator(h=10)

# 複製
cmds.button("duplicateButton", label="選択オブジェクトを対称位置に複製", h=50, command=lambda *args:objectDuplicate())
cmds.separator(h=30)

# ログ
cmds.text("logText", label="　ログ", h=30, align='left')
cmds.scrollField("log", text="", h=100, editable=False)
cmds.button("logClearButton", label="ログをクリア", h=25, command=lambda *args:logClear())

# レイアウトから出る
cmds.setParent("..")

# --------------------
# UI表示
# --------------------
cmds.setParent("..")
cmds.showWindow(window)
#===========================================================
    # file    : VRoidAnimation.py
    # brief   : VRoidモデルのアニメーション制作補助
    # author  : @akitsuki-35（https://github.com/akitsuki-35）
    # date    : 2026/10/23
    # updated : 2026/10/23
#===========================================================
import maya.cmds as cmds

# --------------------
# デフォルトジョイント名定義
# --------------------
JOINT_HIPS = "J_Bip_C_Hips"
JOINT_SPINE = "J_Bip_C_Spine"
JOINT_CHEST = "J_Bip_C_Chest"
JOINT_UPPER_CHEST = "J_Bip_C_UpperChest"
JOINT_NECK = "J_Bip_C_Neck"
JOINT_HEAD = "J_Bip_C_Head"

JOINT_L_SHOULDER = "J_Bip_L_Shoulder"
JOINT_R_SHOULDER = "J_Bip_R_Shoulder"
JOINT_L_UPPER_ARM = "J_Bip_L_UpperArm"
JOINT_R_UPPER_ARM = "J_Bip_R_UpperArm"
JOINT_L_LOWER_ARM = "J_Bip_L_LowerArm"
JOINT_R_LOWER_ARM = "J_Bip_R_LowerArm"
JOINT_L_HAND = "J_Bip_L_Hand"
JOINT_R_HAND = "J_Bip_R_Hand"

JOINT_L_UPPER_LEG = "J_Bip_L_UpperLeg"
JOINT_R_UPPER_LEG = "J_Bip_R_UpperLeg"
JOINT_L_LOWER_LEG = "J_Bip_L_LowerLeg"
JOINT_R_LOWER_LEG = "J_Bip_R_LowerLeg"
JOINT_L_FOOT = "J_Bip_L_Foot"
JOINT_R_FOOT = "J_Bip_R_Foot"
JOINT_L_TOES = "J_Bip_L_Toes"
JOINT_R_TOES = "J_Bip_R_Toes"

# --------------------
# ウィンドウ定義
# --------------------
windowID = "V_Window"

if cmds.window(windowID, exists=True):
    cmds.deleteUI(windowID)
window = cmds.window(windowID, title="VRoid Animation", widthHeight=(400, 700))

# --------------------
# ツールをタブ切り替えに対応
# --------------------
cmds.tabLayout("V_ToolTab", innerMarginWidth=5, innerMarginHeight=5)

# --------------------
# コントローラー生成
# --------------------
# カラムレイアウト作成
cmds.columnLayout("V_Controller", adjustableColumn=True)

# タブにアサイン
cmds.tabLayout("V_ToolTab", edit=True, tabLabel=[("V_Controller", u"Controller")])

# ヘッダテキスト
cmds.text("V_Controller_Header_1", label="Create Controller", h=20)
cmds.text("V_Controller_Header_2", label="VRoidモデルのアニメーション用コントローラー作成", h=20)

# セパレータ
cmds.separator(h=5)

# 主要ジョイント取得
cmds.text("V_CollectJoint_Text", label="　VRoidの主要なアニメーションボーンが存在するか取得", h=30, align='left')
cmds.button("V_CollectJoint_Button", label="収集", h=25, command=lambda *args:logClear())
cmds.separator(h=5)

cmds.image(image="confirm.png")
cmds.image(image="warning.png")

# ログ
cmds.text("V_LogText", label="　ログ", h=30, align='left')
cmds.scrollField("V_Log", text="", h=100, editable=False)
cmds.button("V_LogClearButton", label="ログをクリア", h=25, command=lambda *args:logClear())

# レイアウトから出る
cmds.setParent("..")

# --------------------
# UI表示
# --------------------
cmds.setParent("..")
cmds.showWindow(window)

# --------------------
# ログ出力
# --------------------
def addLog(newText):
    text = cmds.scrollField("V_Log", query=True, text=True)
    
    if text:
        updatedText = f"{text.rstrip()}\n{newText}\n"
    else:
        updatedText = f"{newText}\n"
    
    cmds.scrollField("V_Log", edit=True, text=updatedText)
    cmds.scrollField("V_Log", edit=True, insertionPosition=len(updatedText))

# --------------------
# ログをクリア
# --------------------
def logClear():
    cmds.scrollField("V_Log", edit=True, text="")
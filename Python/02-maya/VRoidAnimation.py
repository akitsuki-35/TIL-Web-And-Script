#===========================================================
    # file    : VRoidAnimation.py
    # brief   : VRoidモデルのアニメーション制作補助
    # author  : @akitsuki-35（https://github.com/akitsuki-35）
    # date    : 2026/10/26
    # updated : 2026/10/26
#===========================================================
import maya.cmds as cmds
from enum import Enum
from dataclasses import dataclass

### VRoidモデルのジョイントチェック・コントローラー作成等のアニメーション補助機能を提供します
### ジョイント名はエクスポート時のデフォルト名を前提としています

# --------------------
# VRoidが生成するデフォルトのジョイント名をテーブルに格納
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
JOINT_L_TOES = "J_Bip_L_ToeBase"
JOINT_R_TOES = "J_Bip_R_ToeBase"

# ジョイントテーブル
V_JOINTS = [
    JOINT_HIPS,
    JOINT_SPINE,
    JOINT_CHEST,
    JOINT_UPPER_CHEST,
    JOINT_NECK,
    JOINT_HEAD,
    JOINT_L_SHOULDER,
    JOINT_R_SHOULDER,
    JOINT_L_UPPER_ARM,
    JOINT_R_UPPER_ARM,
    JOINT_L_LOWER_ARM,
    JOINT_R_LOWER_ARM,
    JOINT_L_HAND,
    JOINT_R_HAND,
    JOINT_L_UPPER_LEG,
    JOINT_R_UPPER_LEG,
    JOINT_L_LOWER_LEG,
    JOINT_R_LOWER_LEG,
    JOINT_L_FOOT,
    JOINT_R_FOOT,
    JOINT_L_TOES,
    JOINT_R_TOES
]

# --------------------
# ジョイント部位テーブル
# --------------------
KEY_NAMES = [
    "Hips",
    "Spine",
    "Chest",
    "UpperChest",
    "Neck",
    "Head",
    "L_Shoulder",
    "R_Shoulder",
    "L_UpperArm",
    "R_UpperArm",
    "L_LowerArm",
    "R_LowerArm",
    "L_Hand",
    "R_Hand",
    "L_UpperLeg",
    "R_UpperLeg",
    "L_LowerLeg",
    "R_LowerLeg",
    "L_Foot",
    "R_Foot",
    "L_Toes",
    "R_Toes"
]

# --------------------
# ジョイントステート列挙体
# 存在の有無および未判定状態を格納
# --------------------
class IsJoint(Enum):
    UNDEFINED = -1 # 未判定
    FALSE = 0 # 存在しない
    TRUE = 1 # 存在する

# --------------------
# ジョイント状態のクラス
# --------------------
@dataclass
class Joint:
    enable: IsJoint
    jointKey: str
    name: str

    def __init__(self, enable=IsJoint(-1), jointKey="", name=""):
        self.enable = enable
        self.jointKey = jointKey
        self.name = name

# ジョイント状態を判定するテーブルを作成
# UI上で [アイコン]部位 : ジョイント名 の書式で表示する
g_Joints = [Joint()] * len(V_JOINTS)
for i in range(len(V_JOINTS)):
    g_Joints[i] = Joint(enable=IsJoint(-1), jointKey=KEY_NAMES[i], name="----------")

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
# 主要ジョイントのチェック
# --------------------
# カラムレイアウト作成
cmds.columnLayout("V_JointCheck", adjustableColumn=True)

# タブにアサイン
cmds.tabLayout("V_ToolTab", edit=True, tabLabel=[("V_JointCheck", u"Joint Check")])

# ヘッダテキスト
cmds.text("V_JointCheck_Header_1", label="Joint Check", h=20)
cmds.text("V_JointCheck_Header_2", label="VRoidの主要ジョイントの有無をチェック", h=20)
cmds.separator(h=5)

cmds.text("V_CollectJoint_Text", label="　★ジョイントを取得", h=20, align='left')

# ジョイント情報表示
cmds.rowLayout("JointRow" + str(i), numberOfColumns=2)
cmds.text("V_JointCount_Value", label="　　--" + "/" + str(len(g_Joints)), h=30, align='left')
cmds.text("V_JointCount_Message", label="　Joint Undefined", h=30, align='left')
cmds.setParent("..")
cmds.separator(h=5)

# スクロールレイアウトでジョイント状態を表示
cmds.scrollLayout(childResizable=True)
cmds.columnLayout(adjustableColumn=True, rowSpacing=0)

# [アイコン]部位 : ジョイント名
for i in range(len(g_Joints)):
    cmds.rowLayout("JointRow" + str(i), numberOfColumns=3)
    if g_Joints[i].enable == IsJoint(0):
        cmds.image("IsEnable" + str(i), image="error.png")
    elif g_Joints[i].enable == IsJoint(1):
        cmds.image("IsEnable" + str(i), image="confirm.png")
    else:
        cmds.image("IsEnable" + str(i), image="help.png")

    cmds.text("JointKey" + str(i), label=g_Joints[i].jointKey + " : ", h=16, align='left')
    cmds.text("JointName" + str(i), label=g_Joints[i].name, h=16, align='left')
    cmds.setParent("..")
cmds.setParent("..")
cmds.setParent("..")

# ボタン
cmds.separator(h=5)
cmds.button("V_CollectJoint_Button", label="Joint Check", w=25, h=25, command=lambda *args:collectJoint())

# ログ
cmds.text("V_JointCheck_LogText", label="　★ログ", h=30, align='left')
cmds.scrollField("V_JointCheck_Log", text="", h=60, editable=False)
cmds.button("V_JointCheck_LogClear", label="ログをクリア", h=25, command=lambda *args:logClear())

# レイアウトから出る
cmds.setParent("..")

# --------------------
# UI表示
# --------------------
cmds.setParent("..")
cmds.showWindow(window)

# --------------------
# ジョイントの有無を判定
# --------------------
def collectJoint():
    count = 0

    for i, name in enumerate(V_JOINTS):
        # VRoidデフォルトジョイント名と一致するジョイントを取得
        joint = cmds.ls(name, type="joint")

        # ジョイントが存在する？
        if joint:
            g_Joints[i].enable = IsJoint(1)
            g_Joints[i].name = name
            count += 1
        else:
            g_Joints[i].enable = IsJoint(0)

        # UIアイテムを書き換え
        if g_Joints[i].enable == IsJoint(0):
            cmds.image("IsEnable" + str(i),  edit=True, image="error.png")
        elif g_Joints[i].enable == IsJoint(1):
            cmds.image("IsEnable" + str(i),  edit=True, image="confirm.png")
        else:
            cmds.image("IsEnable" + str(i),  edit=True, image="empty.png")

        cmds.text("JointName" + str(i), edit=True, label=g_Joints[i].name)

    cmds.text("V_JointCount_Value", edit=True, label="　　" + str(count) + "/" + str(len(g_Joints)))
    if count == len(g_Joints):
        cmds.text("V_JointCount_Message", edit=True, label="　全ての主要ジョイントが存在")
        addLog("collectJoint : 全ての主要ジョイントが存在", "V_JointCheck_Log")
    else:
        cmds.text("V_JointCount_Message", edit=True, label="　存在しない主要ジョイントがあります")
        addLog("collectJoint : 存在しない主要ジョイントがあります", "V_JointCheck_Log")

# --------------------
# ログ出力
# --------------------
def addLog(newText, logItem):
    text = cmds.scrollField(logItem, query=True, text=True)

    if text:
        updatedText = f"{text.rstrip()}\n{newText}\n"
    else:
        updatedText = f"{newText}\n"

    cmds.scrollField(logItem, edit=True, text=updatedText)
    cmds.scrollField(logItem, edit=True, insertionPosition=len(updatedText))

# --------------------
# ログをクリア
# --------------------
def logClear(logItem):
    cmds.scrollField(logItem, edit=True, text="")
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
### ジョイント名はVRMエクスポート時のデフォルト名を前提としています

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
# コントローラー・グループの索引クラス
# 階層構造構築に使用
# --------------------
@dataclass
class Controller:
    jointKey: str # 部位名（インデックスとして使用）
    curveName: str # コントローラー名
    grpName: str # グループ名

    def __init__(self, enable=IsJoint(-1), jointKey="", curveName="", grpName=""):
        self.jointKey = jointKey
        self.curveName = curveName
        self.grpName = grpName

# コントローラー・グループの検索用テーブル
# キーとして部位名を渡し、カーブまたはグループを取得
g_ctrlGrp = [Controller()] * len(V_JOINTS)
for i in range(len(V_JOINTS)):
    g_ctrlGrp[i] = Controller(jointKey=KEY_NAMES[i], curveName="", grpName="")

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
cmds.rowLayout("V_JointRow" + str(i), numberOfColumns=2)
cmds.text("V_JointCount_Value", label="　　--" + "/" + str(len(g_Joints)), h=30, align='left')
cmds.text("V_JointCount_Message", label="　Joint Undefined", h=30, align='left')
cmds.setParent("..")
cmds.separator(h=5)

# スクロールレイアウトでジョイント状態を表示
cmds.scrollLayout(childResizable=True)
cmds.columnLayout(adjustableColumn=True, rowSpacing=0)

# [アイコン]部位 : ジョイント名
for i in range(len(g_Joints)):
    cmds.rowLayout("V_JointRow" + str(i), numberOfColumns=3)
    if g_Joints[i].enable == IsJoint(0):
        cmds.image("V_IsEnable" + str(i), image="error.png")
    elif g_Joints[i].enable == IsJoint(1):
        cmds.image("V_IsEnable" + str(i), image="confirm.png")
    else:
        cmds.image("V_IsEnable" + str(i), image="help.png")

    cmds.text("V_JointKey" + str(i), label=g_Joints[i].jointKey + " : ", h=16, align='left')
    cmds.text("V_JointName" + str(i), label=g_Joints[i].name, h=16, align='left')
    cmds.setParent("..")
cmds.setParent("..")
cmds.setParent("..")

# ボタン
cmds.separator(h=5)
cmds.button("V_CollectJoint_Button", label="ジョイントをチェック", w=25, h=25, command=lambda *args:collectJoint())

# ログ
cmds.text("V_JointCheck_LogText", label="　★ログ", h=30, align='left')
cmds.scrollField("V_JointCheck_Log", text="", h=60, editable=False)
cmds.button("V_JointCheck_LogClear", label="ログをクリア", h=25, command=lambda *args:logClear("V_JointCheck_Log"))

# レイアウトから出る
cmds.setParent("..")

# --------------------
# コントローラー作成
# --------------------
# カラムレイアウト作成
cmds.columnLayout("V_Controller", adjustableColumn=True)

# タブにアサイン
cmds.tabLayout("V_ToolTab", edit=True, tabLabel=[("V_Controller", u"Create Controller")])

# ヘッダテキスト
cmds.text("V_Controller_Header_1", label="Create Controller", h=20)
cmds.text("V_Controller_Header_2", label="VRoidジョイントにコントローラーを追加", h=20)
cmds.separator(h=5)

cmds.text("V_CollectJoint_Text", label="　★コントローラー作成", h=20, align='left')

cmds.text("V_V_ControllerPreSuf_Text", label="　　☆オブジェクト先頭・末尾テキスト", h=30, align='left')

# prefix入力
cmds.rowLayout("V_ControllerPrefixRow" + str(i), numberOfColumns=2)
cmds.text("V_Controller_Prefix_Text", label="　　　Prefix : ", h=20, align='left')
cmds.textField("V_Controller_Prefix", text="V_", w=100, h=20)
cmds.setParent("..")

# suffix入力
cmds.rowLayout("V_ControllerSuffixRow" + str(i), numberOfColumns=2)
cmds.text("V_Controller_Suffix_Text", label="　　　Suffix : ", h=20, align='left')
cmds.textField("V_Controller_Suffix", text="_Ctrl", w=100, h=20)
cmds.setParent("..")

# 半径指定
cmds.text("V_ControllerRadius_Text", label="　　☆コントローラー半径", h=30, align='left')
cmds.intSliderGrp("V_Controller_RadiusSlider", label="　　　Radius : ", field=True, minValue=1, maxValue=10, value=1,
                columnWidth3=[80, 100, 100], columnAlign3=["left", "left", "left"] )

# ボタン
cmds.separator(h=5)
cmds.button("V_Controller_Button", label="コントローラーを作成", w=25, h=25, command=lambda *args:createController())

# ログ
cmds.text("V_Controller_LogText", label="　★ログ", h=30, align='left')
cmds.scrollField("V_Controller_Log", text="", h=400, editable=False)
cmds.button("V_Controller_LogClear", label="ログをクリア", h=25, command=lambda *args:logClear("V_Controller_Log"))

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
            cmds.image("V_IsEnable" + str(i),  edit=True, image="error.png")
        elif g_Joints[i].enable == IsJoint(1):
            cmds.image("V_IsEnable" + str(i),  edit=True, image="confirm.png")
        else:
            cmds.image("V_IsEnable" + str(i),  edit=True, image="empty.png")

        cmds.text("V_JointName" + str(i), edit=True, label=g_Joints[i].name)

    cmds.text("V_JointCount_Value", edit=True, label="　　" + str(count) + "/" + str(len(g_Joints)))
    if count == len(g_Joints):
        cmds.text("V_JointCount_Message", edit=True, label="　全ての主要ジョイントが存在")
        addLog("Success : 全ての主要ジョイントが存在", "V_JointCheck_Log")
    else:
        cmds.text("V_JointCount_Message", edit=True, label="　存在しない主要ジョイントがあります")
        addLog("Warning : 存在しない主要ジョイントがあります", "V_JointCheck_Log")

# --------------------
# コントローラー作成
# --------------------
def createController():
    # コントローラーが既に存在するか取得
    nurbs = cmds.ls(type="nurbsCurve")
    if nurbs:
        addLog(f"Error : 既にコントローラーが作成されています", "V_Controller_Log")
        return

    # prefixとsuffixを取得
    prefix = cmds.textField("V_Controller_Prefix", query=True, text=True)
    suffix = cmds.textField("V_Controller_Suffix", query=True, text=True)

    # prefixまたはsuffixにマルチバイト文字が含まれていたら弾く
    if(isMultiByte(prefix) and isMultiByte(suffix)):
        addLog(f"Error : prefixとsuffixに2バイト文字が含まれています", "V_Controller_Log")
        return
    elif(isMultiByte(prefix)):
        addLog(f"Error : prefixに2バイト文字が含まれています", "V_Controller_Log")
        return
    elif(isMultiByte(suffix)):
        addLog(f"Error : suffixに2バイト文字が含まれています", "V_Controller_Log")
        return

    # 半径を取得
    radius = cmds.intSliderGrp("V_Controller_RadiusSlider", query=True, value=True)

    # ジョイントチェックを実行
    collectJoint()

    for i, name in enumerate(V_JOINTS):
        # VRoidデフォルトジョイント名と一致するジョイントを取得
        joint = cmds.ls(name, type="joint")

        # ジョイントが存在する？
        if joint:
            # 操作用のアニメーションカーブを作成
            itemName = prefix + KEY_NAMES[i] + suffix
            ctrl = cmds.circle(name=f"{itemName}", normal=(0, 1, 0), radius=radius, constructionHistory=False)[0]

            # コントローラーをグループ化
            grpName = f"g_{itemName}"
            group = cmds.group(ctrl, name=grpName)

            # 親グループだけをジョイントの位置・向きに合わせる
            cmds.matchTransform(group, joint, position=True, rotation=True, scale=False)

            # ジョイントと回転順序を合わせる
            cmds.setAttr(f"{ctrl}.rotateOrder", cmds.getAttr(f"{name}.rotateOrder"))

            # コントローラーからジョイントへ回転を伝える
            cmds.orientConstraint(ctrl, joint, maintainOffset=False)

            # テーブルに格納
            g_ctrlGrp[i].curveName = itemName
            g_ctrlGrp[i].jointKey = KEY_NAMES[i]
            g_ctrlGrp[i].grpName = grpName

            print(g_ctrlGrp[i])

            # ログ出力
            addLog(f"Success : Create {ctrl}", "V_Controller_Log")
        else:
            addLog(f"Error : Joint None {name}", "V_Controller_Log")

    # --------------------
    # 階層構造作成
    # --------------------
    # 上半身
    createParent("Head", "Neck")
    createParent("L_Hand", "L_LowerArm")
    createParent("L_LowerArm", "L_UpperArm")
    createParent("L_UpperArm", "L_Shoulder")
    createParent("R_Hand", "R_LowerArm")
    createParent("R_LowerArm", "R_UpperArm")
    createParent("R_UpperArm", "R_Shoulder")
    createParent("Neck", "UpperChest")
    createParent("L_Shoulder", "UpperChest")
    createParent("R_Shoulder", "UpperChest")
    createParent("UpperChest", "Chest")
    createParent("Chest", "Spine")

    # 左足
    createParent("L_Toes", "L_Foot")
    createParent("L_Foot", "L_LowerLeg")
    createParent("L_LowerLeg", "L_UpperLeg")

    # 右足
    createParent("R_Toes", "R_Foot")
    createParent("R_Foot", "R_LowerLeg")
    createParent("R_LowerLeg", "R_UpperLeg")

    # 全身
    createParent("Spine", "Hips")
    createParent("L_UpperLeg", "Hips")
    createParent("R_UpperLeg", "Hips")

# --------------------
# 階層構造作成（グループをコントローラーの子にする）
# --------------------
def createParent(grpKey, curveKey):
    cmds.parent(g_ctrlGrp[KEY_NAMES.index(grpKey)].grpName, g_ctrlGrp[KEY_NAMES.index(curveKey)].curveName)

# --------------------
# マルチバイト文字を判定
# --------------------
def isMultiByte(str):
    return len(str.encode('cp932')) != len(str)

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
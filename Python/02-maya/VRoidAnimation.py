#===========================================================
    # file    : VRoidAnimation.py
    # brief   : VRoidモデルのアニメーション制作補助
    # author  : @akitsuki-35（https://github.com/akitsuki-35）
    # date    : 2026/10/29
    # updated : 2026/10/29
#===========================================================
import maya.cmds as cmds
from enum import Enum
from dataclasses import dataclass

### VRoidモデルのジョイントチェック・コントローラー作成等のアニメーション補助機能を提供します
### ジョイント名はVRMエクスポート時のデフォルト名を前提としています

# --------------------
# VRoidが生成するデフォルトのジョイント名を定数に格納
# --------------------
# 体幹
JOINT_ROOT = "Root"
JOINT_HIPS = "J_Bip_C_Hips"
JOINT_SPINE = "J_Bip_C_Spine"
JOINT_CHEST = "J_Bip_C_Chest"
JOINT_UPPER_CHEST = "J_Bip_C_UpperChest"
JOINT_NECK = "J_Bip_C_Neck"
JOINT_HEAD = "J_Bip_C_Head"

# 肩・腕・手首
JOINT_L_SHOULDER = "J_Bip_L_Shoulder"
JOINT_R_SHOULDER = "J_Bip_R_Shoulder"
JOINT_L_UPPER_ARM = "J_Bip_L_UpperArm"
JOINT_R_UPPER_ARM = "J_Bip_R_UpperArm"
JOINT_L_LOWER_ARM = "J_Bip_L_LowerArm"
JOINT_R_LOWER_ARM = "J_Bip_R_LowerArm"
JOINT_L_HAND = "J_Bip_L_Hand"
JOINT_R_HAND = "J_Bip_R_Hand"

# 下半身
JOINT_L_UPPER_LEG = "J_Bip_L_UpperLeg"
JOINT_R_UPPER_LEG = "J_Bip_R_UpperLeg"
JOINT_L_LOWER_LEG = "J_Bip_L_LowerLeg"
JOINT_R_LOWER_LEG = "J_Bip_R_LowerLeg"
JOINT_L_FOOT = "J_Bip_L_Foot"
JOINT_R_FOOT = "J_Bip_R_Foot"
JOINT_L_TOES = "J_Bip_L_ToeBase"
JOINT_R_TOES = "J_Bip_R_ToeBase"

# 親指
JOINT_L_THUMB1 = "J_Bip_L_Thumb1"
JOINT_R_THUMB1 = "J_Bip_R_Thumb1"
JOINT_L_THUMB2 = "J_Bip_L_Thumb2"
JOINT_R_THUMB2 = "J_Bip_R_Thumb2"
JOINT_L_THUMB3 = "J_Bip_L_Thumb3"
JOINT_R_THUMB3 = "J_Bip_R_Thumb3"

# 人差し指
JOINT_L_INDEX1 = "J_Bip_L_Index1"
JOINT_R_INDEX1 = "J_Bip_R_Index1"
JOINT_L_INDEX2 = "J_Bip_L_Index2"
JOINT_R_INDEX2 = "J_Bip_R_Index2"
JOINT_L_INDEX3 = "J_Bip_L_Index3"
JOINT_R_INDEX3 = "J_Bip_R_Index3"

# 中指
JOINT_L_MIDDLE1 = "J_Bip_L_Middle1"
JOINT_R_MIDDLE1 = "J_Bip_R_Middle1"
JOINT_L_MIDDLE2 = "J_Bip_L_Middle2"
JOINT_R_MIDDLE2 = "J_Bip_R_Middle2"
JOINT_L_MIDDLE3 = "J_Bip_L_Middle3"
JOINT_R_MIDDLE3 = "J_Bip_R_Middle3"

# 薬指
JOINT_L_RING1 = "J_Bip_L_Ring1"
JOINT_R_RING1 = "J_Bip_R_Ring1"
JOINT_L_RING2 = "J_Bip_L_Ring2"
JOINT_R_RING2 = "J_Bip_R_Ring2"
JOINT_L_RING3 = "J_Bip_L_Ring3"
JOINT_R_RING3 = "J_Bip_R_Ring3"

# 小指
JOINT_L_LITTLE1 = "J_Bip_L_Little1"
JOINT_R_LITTLE1 = "J_Bip_R_Little1"
JOINT_L_LITTLE2 = "J_Bip_L_Little2"
JOINT_R_LITTLE2 = "J_Bip_R_Little2"
JOINT_L_LITTLE3 = "J_Bip_L_Little3"
JOINT_R_LITTLE3 = "J_Bip_R_Little3"

# ジョイントテーブル
# VRoidジョイント名を格納し代入やインデックスとして使えるようにする
V_JOINTS = [
    # 体幹
    JOINT_ROOT,
    JOINT_HIPS,
    JOINT_SPINE,
    JOINT_CHEST,
    JOINT_UPPER_CHEST,
    JOINT_NECK,
    JOINT_HEAD,

    # 肩・腕・手首
    JOINT_L_SHOULDER,
    JOINT_R_SHOULDER,
    JOINT_L_UPPER_ARM,
    JOINT_R_UPPER_ARM,
    JOINT_L_LOWER_ARM,
    JOINT_R_LOWER_ARM,
    JOINT_L_HAND,
    JOINT_R_HAND,

    # 下半身
    JOINT_L_UPPER_LEG,
    JOINT_R_UPPER_LEG,
    JOINT_L_LOWER_LEG,
    JOINT_R_LOWER_LEG,
    JOINT_L_FOOT,
    JOINT_R_FOOT,
    JOINT_L_TOES,
    JOINT_R_TOES,

    # 親指
    JOINT_L_THUMB1,
    JOINT_R_THUMB1,
    JOINT_L_THUMB2,
    JOINT_R_THUMB2,
    JOINT_L_THUMB3,
    JOINT_R_THUMB3,

    # 人差し指
    JOINT_L_INDEX1,
    JOINT_R_INDEX1,
    JOINT_L_INDEX2,
    JOINT_R_INDEX2,
    JOINT_L_INDEX3,
    JOINT_R_INDEX3,

    # 中指
    JOINT_L_MIDDLE1,
    JOINT_R_MIDDLE1,
    JOINT_L_MIDDLE2,
    JOINT_R_MIDDLE2,
    JOINT_L_MIDDLE3,
    JOINT_R_MIDDLE3,

    # 薬指
    JOINT_L_RING1,
    JOINT_R_RING1,
    JOINT_L_RING2,
    JOINT_R_RING2,
    JOINT_L_RING3,
    JOINT_R_RING3,

    # 小指
    JOINT_L_LITTLE1,
    JOINT_R_LITTLE1,
    JOINT_L_LITTLE2,
    JOINT_R_LITTLE2,
    JOINT_L_LITTLE3,
    JOINT_R_LITTLE3
]

# 指コントローラー作成判定用に指ジョイントのみを格納したテーブル
V_FINGER_JOINS = [
    # 親指
    JOINT_L_THUMB1,
    JOINT_R_THUMB1,
    JOINT_L_THUMB2,
    JOINT_R_THUMB2,
    JOINT_L_THUMB3,
    JOINT_R_THUMB3,

    # 人差し指
    JOINT_L_INDEX1,
    JOINT_R_INDEX1,
    JOINT_L_INDEX2,
    JOINT_R_INDEX2,
    JOINT_L_INDEX3,
    JOINT_R_INDEX3,

    # 中指
    JOINT_L_MIDDLE1,
    JOINT_R_MIDDLE1,
    JOINT_L_MIDDLE2,
    JOINT_R_MIDDLE2,
    JOINT_L_MIDDLE3,
    JOINT_R_MIDDLE3,

    # 薬指
    JOINT_L_RING1,
    JOINT_R_RING1,
    JOINT_L_RING2,
    JOINT_R_RING2,
    JOINT_L_RING3,
    JOINT_R_RING3,

    # 小指
    JOINT_L_LITTLE1,
    JOINT_R_LITTLE1,
    JOINT_L_LITTLE2,
    JOINT_R_LITTLE2,
    JOINT_L_LITTLE3,
    JOINT_R_LITTLE3
]

# --------------------
# ジョイント部位名テーブル
# VRoidのデフォルトジョイント名が冗長なため、正規化名を各種テーブルのキー名として持たせる
# --------------------
KEY_NAMES = [
    # 体幹
    "Root",
    "Hips",
    "Spine",
    "Chest",
    "UpperChest",
    "Neck",
    "Head",

    # 肩・腕・手首
    "L_Shoulder",
    "R_Shoulder",
    "L_UpperArm",
    "R_UpperArm",
    "L_LowerArm",
    "R_LowerArm",
    "L_Hand",
    "R_Hand",

    # 下半身
    "L_UpperLeg",
    "R_UpperLeg",
    "L_LowerLeg",
    "R_LowerLeg",
    "L_Foot",
    "R_Foot",
    "L_Toes",
    "R_Toes",

    # 親指
    "L_Thumb1",
    "R_Thumb1",
    "L_Thumb2",
    "R_Thumb2",
    "L_Thumb3",
    "R_Thumb3",

    # 人差し指
    "L_Index1",
    "R_Index1",
    "L_Index2",
    "R_Index2",
    "L_Index3",
    "R_Index3",

    # 中指
    "L_Middle1",
    "R_Middle1",
    "L_Middle2",
    "R_Middle2",
    "L_Middle3",
    "R_Middle3",

    # 薬指
    "L_Ring1",
    "R_Ring1",
    "L_Ring2",
    "R_Ring2",
    "L_Ring3",
    "R_Ring3",

    # 小指
    "L_Little1",
    "R_Little1",
    "L_Little2",
    "R_Little2",
    "L_Little3",
    "R_Little3"
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
# ジョイントの有無と部位のキー名, 実ジョイント名を格納
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
# コントローラー・グループの検索用クラス
# 部位キー, コントローラーのカーブ名, グループ名を格納
# 階層構造構築時に部位をキーとしてcurveName, grpNameを取得
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
# レイアウトを作成してタブに挿入
cmds.columnLayout("V_JointCheck", adjustableColumn=True)
cmds.tabLayout("V_ToolTab", edit=True, tabLabel=[("V_JointCheck", u"Joint Check")])

# ヘッダテキスト表示
cmds.text("V_JointCheck_Header_1", label="Joint Check", h=20)
cmds.text("V_JointCheck_Header_2", label="VRoidの主要ジョイントの有無をチェック", h=20)
cmds.separator(h=5)

# 見出しテキスト
cmds.text("V_CollectJoint_Text", label="　★ジョイントを取得", h=20, align='left')

# ジョイント数と判定結果を表示する
cmds.rowLayout("V_JointRow" + str(i), numberOfColumns=2)
cmds.text("V_JointCount_Value", label=f"　　--/{str(len(g_Joints))}", h=30, align='left')
cmds.text("V_JointCount_Message", label="　Joint Undefined", h=30, align='left')
cmds.setParent("..")
cmds.separator(h=5)

# スクロールレイアウトでジョイント状態を表示
cmds.scrollLayout(childResizable=True)
cmds.columnLayout(adjustableColumn=True, rowSpacing=0)

# ジョイント有無の判定結果を表示する領域
# [アイコン]部位 : ジョイント名
for i in range(len(g_Joints)):
    cmds.rowLayout(f"V_JointRow{str(i)}", numberOfColumns=3)
    if g_Joints[i].enable == IsJoint(0):
        cmds.image(f"V_IsEnable{str(i)}", image="error.png")
    elif g_Joints[i].enable == IsJoint(1):
        cmds.image(f"V_IsEnable{str(i)}", image="confirm.png")
    else:
        cmds.image(f"V_IsEnable{str(i)}", image="help.png")

    cmds.text(f"V_JointKey{str(i)}", label=f"{g_Joints[i].jointKey} : ", h=16, align='left')
    cmds.text(f"V_JointName{str(i)}", label=g_Joints[i].name, h=16, align='left')
    cmds.setParent("..")
cmds.setParent("..")
cmds.setParent("..")

# ボタン
cmds.separator(h=5)
cmds.button("V_CollectJoint_Button", label="ジョイントをチェック", w=25, h=25, command=lambda *args:collectJoint())

# ログ
cmds.text("V_JointCheck_LogText", label="　★ログ", h=30, align='left')
cmds.scrollField("V_JointCheck_Log", text="", h=60, editable=False)
cmds.button("V_JointCheck_LogClear", label="ログをクリア", h=25, backgroundColor=[0.3, 0.4, 0.5], command=lambda *args:logClear("V_JointCheck_Log"))

# レイアウトから出る
cmds.setParent("..")

# --------------------
# コントローラー作成
# --------------------
# レイアウトを作成してタブに挿入
cmds.columnLayout("V_Controller", adjustableColumn=True)
cmds.tabLayout("V_ToolTab", edit=True, tabLabel=[("V_Controller", u"Create Controller")])

# ヘッダテキスト
cmds.text("V_Controller_Header_1", label="Create Controller", h=20)
cmds.text("V_Controller_Header_2", label="VRoidジョイントにコントローラーを追加", h=20)
cmds.separator(h=5)

# コントローラー名のprefixとsuffixの入力
cmds.text("V_CollectJoint_Text", label="　★コントローラー作成", h=20, align='left')
cmds.text("V_V_ControllerPreSuf_Text", label="　　☆オブジェクト先頭・末尾テキスト", h=30, align='left')

# prefix
cmds.rowLayout(f"V_ControllerPrefixRow{str(i)}", numberOfColumns=2)
cmds.text("V_Controller_Prefix_Text", label="　　　Prefix : ", h=20, align='left')
cmds.textField("V_Controller_Prefix", text="V_", w=100, h=20)
cmds.setParent("..")

# suffix
cmds.rowLayout(f"V_ControllerSuffixRow{str(i)}", numberOfColumns=2)
cmds.text("V_Controller_Suffix_Text", label="　　　Suffix : ", h=20, align='left')
cmds.textField("V_Controller_Suffix", text="_Ctrl", w=100, h=20)
cmds.setParent("..")

# コントローラー半径を指定
cmds.text("V_ControllerRadius_Text", label="　　☆コントローラー半径", h=30, align='left')
cmds.intSliderGrp("V_Controller_RadiusSlider", label="　　　Radius : ", field=True, minValue=1, maxValue=10, value=1,
                columnWidth3=[80, 100, 100], columnAlign3=["left", "left", "left"] )

# コントローラーにRootを含めるか
cmds.text("V_ControllerCheckBox_Text", label="　　☆詳細設定", h=30, align='left')
cmds.rowLayout(f"V_ControllerCheckBoxRootRow{str(i)}", numberOfColumns=2)
cmds.text("V_ControllerIsRoot_Space", label="　　　", align='left')
cmds.checkBox("V_ControllerIsRoot", label="Rootを含める",  align='left')
cmds.setParent("..")

# コントローラーに指ジョイントを含めるか
cmds.rowLayout(f"V_ControllerCheckBoxFingerRow{str(i)}", numberOfColumns=2)
cmds.text("V_ControllerIsFinger_Space", label="　　　", align='left')
cmds.checkBox("V_ControllerIsFinger", label="指ジョイントを含める",  align='left')
cmds.setParent("..")

# ボタン
cmds.separator(h=5)
cmds.button("V_Controller_Button", label="コントローラーを作成", w=25, h=25, command=lambda *args:createController())

# ログ
cmds.text("V_Controller_LogText", label="　★ログ", h=30, align='left')
cmds.scrollField("V_Controller_Log", text="", h=250, editable=False)
cmds.button("V_Controller_LogClear", label="ログをクリア", h=25, command=lambda *args:logClear("V_Controller_Log"))

# レイアウトから出る
cmds.setParent("..")

# --------------------
# コントローラー選択
# --------------------
# レイアウトを作成してタブに挿入
cmds.columnLayout("V_Select", adjustableColumn=True)
cmds.tabLayout("V_ToolTab", edit=True, tabLabel=[("V_Select", u"Select Controller")])

# ヘッダテキスト
cmds.text("V_Select_Header_1", label="Select Controller", h=20)
cmds.text("V_Select_Header_2", label="コントローラーの選択状態を制御", h=20)
cmds.separator(h=5)

cmds.frameLayout("V_SelectFrame", label="上半身", collapsable=True)
cmds.setParent("..")

# ログ
cmds.text("V_Select_LogText", label="　★ログ", h=30, align='left')
cmds.scrollField("V_Select_Log", text="", h=60, editable=False)
cmds.button("V_Select_LogClear", label="ログをクリア", h=25, command=lambda *args:logClear("V_Select_Log"))

# レイアウトから出る
cmds.setParent("..")

# --------------------
# UIを表示する
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

        # ジョイントが存在するなら、g_Joints[i]に格納
        if joint:
            g_Joints[i].enable = IsJoint(1)
            g_Joints[i].name = name
            count += 1

        else:
            # 見つからなかった場合は失敗フラグを入れる
            g_Joints[i].enable = IsJoint(0)

            # ログを冗長にしないため、読み取れなかったジョイントのみログを出力
            addLog(f"False : ジョイント[{name}]が見つかりません", "V_JointCheck_Log")

        # UIアイテムを書き換え
        # アイコンをジョイント存在の有無に応じて変更
        if g_Joints[i].enable == IsJoint(0):
            cmds.image(f"V_IsEnable{str(i)}",  edit=True, image="error.png")
        elif g_Joints[i].enable == IsJoint(1):
            cmds.image(f"V_IsEnable{str(i)}",  edit=True, image="confirm.png")
        else:
            cmds.image(f"V_IsEnable{str(i)}",  edit=True, image="empty.png")

        # 部位 ; 実ジョイント名の表示
        cmds.text(f"V_JointName{str(i)}", edit=True, label=g_Joints[i].name)

    # ジョイントの正常数/総数を更新
    cmds.text("V_JointCount_Value", edit=True, label=f"　　{str(count)}/{str(len(g_Joints))}")

    # 結果に応じてメッセージ表示とログ出力
    if count == len(g_Joints):
        cmds.text("V_JointCount_Message", edit=True, label="　主要ジョイントは全て正常です")
        addLog("Success : 全ての主要ジョイントが存在", "V_JointCheck_Log")
        return True
    else:
        cmds.text("V_JointCount_Message", edit=True, label="　取得できなかった主要ジョイントがあります")
        addLog("Warning : 削除されているか、vrmデフォルト名から変更されているジョイントが存在します\nコントローラーの作成が正常に行われません", "V_JointCheck_Log")

# --------------------
# コントローラー作成
# --------------------
def createController():
    # コントローラーが既に存在するか取得
    nurbs = cmds.ls(type="nurbsCurve")
    if nurbs:
        addLog(f"Error : 既にコントローラーが作成されています\n新規に作成するには既存のコントローラーを削除してください", "V_Controller_Log")
        return

    # ジョイントチェックを実行し、正常な場合のみ処理を続行
    # 親子関係構築時に破綻するため、1つでも取得できなければ止める
    # Rootや指ジョイントを含める設定でこれらが異常な場合でも止める
    if (collectJoint()):
        addLog(f"Success : JointCheck OK!", "V_Controller_Log")
    else:
        addLog(f"Error : ジョイントが正常ではありません\nJoint Checkのタブを確認してください", "V_Controller_Log")
        return

    # コントローラー名のprefixとsuffixを取得
    prefix = cmds.textField("V_Controller_Prefix", query=True, text=True)
    suffix = cmds.textField("V_Controller_Suffix", query=True, text=True)

    # prefixまたはsuffixにマルチバイト文字が含まれていたら弾く
    # Mayaのオブジェクト名にマルチバイト文字を使えずデフォルト名になるため、親子関係構築や取得時に破綻する
    if(isMultiByte(prefix) and isMultiByte(suffix)):
        addLog(f"Error : prefixとsuffixに2バイト文字が含まれています\nコントローラー名として使用できません", "V_Controller_Log")
        return
    elif(isMultiByte(prefix)):
        addLog(f"Error : prefixに2バイト文字が含まれています\nコントローラー名として使用できません", "V_Controller_Log")
        return
    elif(isMultiByte(suffix)):
        addLog(f"Error : suffixに2バイト文字が含まれています\nコントローラー名として使用できません", "V_Controller_Log")
        return

    # コントローラー半径を取得
    radius = cmds.intSliderGrp("V_Controller_RadiusSlider", query=True, value=True)

    # ルートジョイント・指ジョイントを含める設定を取得
    isRoot = cmds.checkBox("V_ControllerIsRoot", query=True, value=True)
    isFinger = cmds.checkBox("V_ControllerIsFinger", query=True, value=True)

    # 全ての主要ジョイントのコントローラーとグループを作成
    for i, name in enumerate(V_JOINTS):
        # ルートジョイントを含めない設定の場合はルートジョイントのコントローラー作成をスキップ
        if(name == JOINT_ROOT):
            if(not isRoot):
                continue

        # 指ジョイントを含めない設定の場合は指ジョイントのコントローラー作成をスキップ
        if(isFingerJoint(name)):
            if(not isFinger):
                continue

        # VRoidデフォルトジョイント名と一致するジョイントを取得
        joint = cmds.ls(name, type="joint")

        # ジョイントが存在する？
        if joint:
            # 操作用のアニメーションカーブを作成
            itemName = f"{prefix}{KEY_NAMES[i]}{suffix}"
            ctrl = cmds.circle(name=f"{itemName}", normal=(0, 1, 0), radius=radius, constructionHistory=False)[0]

            # コントローラーをグループ化
            grpName = f"g_{itemName}"
            group = cmds.group(ctrl, name=grpName)

            # 親グループだけをジョイントの位置・向きに合わせる
            # コントローラー自体の各値を0にし、操作しやすくする
            cmds.matchTransform(group, joint, position=True, rotation=True, scale=False)

            # ジョイントと回転順序を合わせる
            cmds.setAttr(f"{ctrl}.rotateOrder", cmds.getAttr(f"{name}.rotateOrder"))

            # コントローラーからジョイントへ回転を伝える
            cmds.orientConstraint(ctrl, joint, maintainOffset=False)

            # g_ctrlGrpテーブルに格納し、親子関係構築で使用
            g_ctrlGrp[i].curveName = itemName
            g_ctrlGrp[i].jointKey = KEY_NAMES[i]
            g_ctrlGrp[i].grpName = grpName

            # 結果に応じてログ出力
            if(cmds.ls(itemName)):
                addLog(f"Success : Create Success {ctrl}", "V_Controller_Log")
            else:
                addLog(f"Error : Create Failed {ctrl}", "V_Controller_Log")
        else:
            # ジョイントが存在しない場合はエラーログを出して次の処理へ
            # ただし全ジョイントが取得できないとそもそも処理されないので保険
            addLog(f"Error : ジョイント[{name}]が存在しません", "V_Controller_Log")

    # --------------------
    # コントローラー階層構造作成
    # VRoidモデルの実ジョイントと同じ階層構造を構築
    # コントローラーも階層にしないとモデルが正しく動かない
    # --------------------
    # 指ジョイントコントローラーを作成した場合は、先に指コントローラーの階層構造を作成
    if(isFinger):
        # 左手の先→中→付け根
        createParent("L_Thumb3", "L_Thumb2")
        createParent("L_Thumb2", "L_Thumb1")
        createParent("L_Index3", "L_Index2")
        createParent("L_Index2", "L_Index1")
        createParent("L_Middle3", "L_Middle2")
        createParent("L_Middle2", "L_Middle1")
        createParent("L_Ring3", "L_Ring2")
        createParent("L_Ring2", "L_Ring1")
        createParent("L_Little3", "L_Little2")
        createParent("L_Little2", "L_Little1")

        # 右手の先→中→付け根
        createParent("R_Thumb3", "R_Thumb2")
        createParent("R_Thumb2", "R_Thumb1")
        createParent("R_Index3", "R_Index2")
        createParent("R_Index2", "R_Index1")
        createParent("R_Middle3", "R_Middle2")
        createParent("R_Middle2", "R_Middle1")
        createParent("R_Ring3", "R_Ring2")
        createParent("R_Ring2", "R_Ring1")
        createParent("R_Little3", "R_Little2")
        createParent("R_Little2", "R_Little1")

        # それぞれの指コントローラーを左右の手首コントローラーの子にする
        createParent("L_Thumb1", "L_Hand")
        createParent("L_Index1", "L_Hand")
        createParent("L_Middle1", "L_Hand")
        createParent("L_Ring1", "L_Hand")
        createParent("L_Little1", "L_Hand")
        createParent("R_Thumb1", "R_Hand")
        createParent("R_Index1", "R_Hand")
        createParent("R_Middle1", "R_Hand")
        createParent("R_Ring1", "R_Hand")
        createParent("R_Little1", "R_Hand")

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

    # Spineと左右のUpperLegをHipsの子にする
    createParent("Spine", "Hips")
    createParent("L_UpperLeg", "Hips")
    createParent("R_UpperLeg", "Hips")

    # ルートのコントローラーを作成した場合は、Hipsをルートの子にする
    if(isRoot):
        createParent("Hips", "Root")

# --------------------
# 階層構造作成サブ関数（グループをコントローラーの子にする）
# 子オブジェクト, 親オブジェクトの順序で引数を指定
# --------------------
def createParent(grpKey, curveKey):
    cmds.parent(g_ctrlGrp[KEY_NAMES.index(grpKey)].grpName, g_ctrlGrp[KEY_NAMES.index(curveKey)].curveName)

# --------------------
# コントローラーを作ろうとしているジョイントが指ジョイントか判定
# --------------------
def isFingerJoint(str):
    for i in range(len(V_FINGER_JOINS)):
        if(V_FINGER_JOINS[i] == str):
            return True

    return False

# --------------------
# マルチバイト文字を判定
# --------------------
def isMultiByte(str):
    return len(str.encode('cp932')) != len(str)

# --------------------
# ログ出力
# タブごとのログIDが違うため、ログIDも引数として渡す
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
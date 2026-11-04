#===========================================================
    # file    : VRoidAnimation.py
    # brief   : VRoidモデルのアニメーション制作補助
    # author  : @akitsuki-35（https://github.com/akitsuki-35）
    # date    : 2026/11/04
    # updated : 2026/11/04
#===========================================================
import maya.cmds as cmds
import maya.mel as mel
from enum import Enum
from dataclasses import dataclass
import csv
import os

### VRoidモデルのジョイントチェック・コントローラー作成等のアニメーション補助機能を提供します
### ジョイント名はVRMエクスポート時のデフォルト名を前提としています

### VRoid→BlenderでFBX変換したモデルをDirectXに導入し、Mayaでアニメーションを作成して動かすため
### VRoidのデフォルトボーン名で厳格に精査する

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
    jointName : str # 実ジョイント名（定数を使用）
    curveName: str # コントローラー名
    grpName: str # グループ名

    def __init__(self, jointKey="", jointName="",  curveName="", grpName=""):
        self.jointKey = jointKey
        self.jointName = jointName
        self.curveName = curveName
        self.grpName = grpName

# コントローラー・グループの検索用テーブル
# キーとして部位名を渡し、カーブまたはグループを取得
g_ctrlGrp = [Controller()] * len(V_JOINTS)
for i in range(len(V_JOINTS)):
    g_ctrlGrp[i] = Controller(jointKey=KEY_NAMES[i], jointName=V_JOINTS[i], curveName="", grpName="")

# コントローラーがスクリプトに接続済みか（g_ctrlGrpに詰められているか）
# コントローラー作成後にスクリプトを閉じるとg_ctrlGrpが空になるため、再接続が必要
IS_CTRL_CONNECTED = False

# --------------------
# 選択状態監視ジョブの定義
# --------------------
# 初期化
global V_SelectJobID_1
if "V_SelectJobID_1" not in globals():
    V_SelectJobID_1 = None

global V_SelectJobID_2
if "V_SelectJobID_2" not in globals():
    V_SelectJobID_2 = None

# 既にジョブが存在する場合は削除してクリーンにする
if V_SelectJobID_1 and cmds.scriptJob(exists=V_SelectJobID_1):
    cmds.scriptJob(kill=V_SelectJobID_1, force=True)
    V_SelectJobID_1 = None

if V_SelectJobID_2 and cmds.scriptJob(exists=V_SelectJobID_2):
    cmds.scriptJob(kill=V_SelectJobID_2, force=True)
    V_SelectJobID_2 = None

# --------------------
# 補助関数定義
# --------------------
# --------------------
# コントローラー取得
# --------------------
def getController():
    # 全コントローラーを取得し、リストを返す
    ctrls = []
    for i in range(len(g_ctrlGrp)):
        ctrl = g_ctrlGrp[i].curveName
        if not cmds.objExists(ctrl):
            continue
        else:
            ctrls.append(g_ctrlGrp[i].curveName)

    return ctrls

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
        cmds.text(f"V_JointName{str(i)}_Text", edit=True, label=g_Joints[i].name)

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
    global IS_CTRL_CONNECTED

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
        addLog(f"Error : ジョイントが正常ではありません\n[ジョイント取得]タブを確認してください", "V_Controller_Log")
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
    radius = cmds.intSliderGrp("V_Controller_Radius_Slider", query=True, value=True)

    # 全ての主要ジョイントのコントローラーとグループを作成
    for i, name in enumerate(V_JOINTS):
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
                addLog(f"Success : Create Success [{ctrl}]", "V_Controller_Log")
            else:
                addLog(f"Error : Create Failed [{ctrl}]", "V_Controller_Log")
        else:
            # ジョイントが存在しない場合はエラーログを出して次の処理へ
            # ただし全ジョイントが取得できないとそもそも処理されないので保険
            addLog(f"Error : ジョイント[{name}]が存在しません", "V_Controller_Log")

    # 全コントローラーが正常に作成されたら、コントローラー接続フラグをオンに
    IS_CTRL_CONNECTED = True

    # --------------------
    # コントローラー階層構造作成
    # VRoidモデルの実ジョイントと同じ階層構造を構築
    # コントローラーも階層にしないとモデルが正しく動かない
    # --------------------
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

    # Hipsをルートの子にする
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
# チェックボックス状態に応じてソケット作成
# --------------------
def createSocket():
    settings = []
    settings.append(cmds.checkBox("V_Socket_IsLeftHand", query=True, value=True))
    settings.append(cmds.checkBox("V_Socket_IsRightHand", query=True, value=True))
    settings.append(cmds.checkBox("V_Socket_IsChest", query=True, value=True))

    if not any(settings):
        addLog(f"Error : チェックが入っている部位がないため、ソケットが作成されませんでした", "V_Socket_Log")

    # prefixとsuffixを取得
    prefix = cmds.textField("V_Socket_Prefix", query=True, text=True)
    suffix = cmds.textField("V_Socket_Suffix", query=True, text=True)

    # ソケットを作成
    for i in range(len(settings)):
        match i:
            case 0:
                addSocket(f"{prefix}L_Hand{suffix}", JOINT_L_HAND)
            case 1:
                addSocket(f"{prefix}R_Hand{suffix}", JOINT_R_HAND)
            case 2:
                addSocket(f"{prefix}Chest{suffix}", JOINT_CHEST)


# --------------------
# ソケット作成処理
# --------------------
def addSocket(str, parent):
    # 親ジョイントが存在しない場合は弾く
    if not cmds.objExists(parent):
        addLog(f"Error : [{parent}]が存在しません", "V_Socket_Log")
        return

    # 指定ソケットが既に存在する場合は弾く
    if cmds.objExists(str):
        addLog(f"Error : ソケット[{str}]は既に作成されています", "V_Socket_Log")
        return

    # ソケットとなるロケータを作成
    socket = cmds.spaceLocator(name=str)[0]
    cmds.parent(socket, parent, relative=True)

    # 座標と回転を0にする
    cmds.setAttr(f"{socket}.translate", 0, 0, 0, type="double3")
    cmds.setAttr(f"{socket}.rotate", 0, 0, 0, type="double3")
    cmds.setAttr(f"{socket}.scale", 1, 1, 1, type="double3")

    # ソケットを選択状態にする
    cmds.select(socket, replace=True)

    addLog(f"Success : Create Success [{str}]", "V_Socket_Log")

# --------------------
# ソケットをCSV出力
# --------------------
def exportSockets():
    # 選択中のオブジェクトを取得
    sel = cmds.ls(selection=True, type="transform") or []

    if not sel:
        addLog("Error : 選択されているオブジェクトがありません", "V_Socket_Log")
        return

    # ロケータが選択されているか確認
    socket = sel[0]
    locator = cmds.listRelatives(socket, shapes=True, type="locator") or []

    if not locator:
        addLog(f"Error : [{socket}]はLocatorではありません", "V_Socket_Log")
        return

    # 親ジョイントを取得
    parents = cmds.listRelatives(socket, parent=True, type="joint") or []

    if not parents:
        addLog(f"Error : ソケット[{socket}]に親ジョイントがありません", "V_Socket_Log")
        return

    parent = parents[0]

    # 親ジョイント基準のローカル位置・回転を取得
    position = cmds.getAttr(f"{socket}.translate")[0]
    rotation = cmds.getAttr(f"{socket}.rotate")[0]

    # 出力先フォルダ選択
    Paths = cmds.fileDialog2(fileMode=0, dialogStyle=2, fileFilter="CSV Files (*.csv)", caption="ソケット情報をCSV出力")
    if not Paths:
        return

    # ソケット名をファイル名にする
    filePath = Paths[0]

    # .CSVがない場合は追加する
    if not filePath.lower().endswith(".csv"):
        filePath += ".csv"

    # CSV出力
    with open(filePath, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)

        writer.writerow(["Name", socket])
        writer.writerow(["Parent", parent])
        writer.writerow(["Position", position[0], position[1], position[2]])
        writer.writerow(["Rotation", rotation[0], rotation[1], rotation[2]])

    addLog(f"Success : ソケット[{socket}]の出力に成功しました", "V_Socket_Log")

# --------------------
# コントローラー選択ボタンUIの作成
# 引数：UIのID, ボタン数, ループを開始する配列番号
# --------------------
def createSelectButton(num, idOffset, row):
    cmds.rowLayout(f"V_SelectCenterRow{num}", numberOfColumns=row + 1)

    # ボタン開始位置をずらす空白テキスト
    cmds.text(f"V_SelectBlankCenter{num}", label="　　", h=20, align='left')

    for i in range(row):
        i += idOffset

        cmds.button(f"V_Select{KEY_NAMES[i]}Button", label=KEY_NAMES[i], w=80, h=20,
                    command=lambda *args, i=i:selectController(KEY_NAMES[i]))

    cmds.setParent("..")

# --------------------
# コントローラーの選択状態制御
# --------------------
def selectController(str):
    # ctrlキー・Shiftキーが押されているかを取得
    mods = cmds.getModifiers()
    isCtrlShiftPressed = (mods & 1) > 0 or (mods & 4) > 0

    # コントローラーが作成済みか取得
    nurbs = cmds.ls(type="nurbsCurve")
    if not nurbs:
        addLog(f"Error : コントローラーが作成されていません\n[CTRL作成]タブからコントローラーを作成してください", "V_Select_Log")
        return

    # ターゲットのコントローラー名を取得
    ctrl = g_ctrlGrp[KEY_NAMES.index(str)].curveName

    # 存在しない場合は弾く
    curve = cmds.ls(ctrl)
    if(not curve):
        addLog(f"Error : {str} のコントローラーが存在しません", "V_Select_Log")
        return

    # ターゲットのコントローラーが選択されているか取得
    sel = cmds.ls(selection=True)
    isSel = False
    if ctrl in sel:
        isSel = True

    # ctrlキー・Shiftキーが押されている場合は追加選択し、既に選択されているなら選択解除する
    # アウトライナ上と同様の操作感にする
    cmds.select(ctrl, add=isCtrlShiftPressed, deselect=isSel)

    # ログ出力
    if not isSel:
        addLog(f"Success : [{ctrl}]を選択しました", "V_Select_Log")
    else:
        addLog(f"Success : [{ctrl}]の選択を解除しました", "V_Select_Log")

    # 今選択されているオブジェクトを出力
    sel = cmds.ls(selection=True)
    addLog(f"Log : Select {sel}", "V_Select_Log")

# --------------------
# 全ての選択をクリア
# --------------------
def clearSel():
    cmds.select(clear=True)
    addLog("Log : 全ての選択を解除しました", "V_Select_Log")

# --------------------
# コントローラー再接続
# --------------------
def reconnectController(nurbs):
    global IS_CTRL_CONNECTED

    if not IS_CTRL_CONNECTED:
        # カーブの親を取得
        ctrls =  cmds.listRelatives(nurbs, parent=True, fullPath=False) or []
        ctrls = list(set(ctrls))

        # リスト参照時にデータ不整合が起こるため、V_JOINTS等と部位の順序が一致するよう並べ替える
        for i in range(len(V_JOINTS)):
            # 部位のキー名を取得
            target = KEY_NAMES[i]

            # キー名の文字列が含まれているコントローラーおよびグループを取得する
            for ctrl in ctrls:
                if target in ctrl:

                    # Chestと間違えてUpperChestを持ってこないようにする
                    if target == "Chest" and "UpperChest" in ctrl:
                        continue

                    # コントローラーの親となるグループの名前を取得
                    grp = cmds.listRelatives(ctrl, parent=True, fullPath=False)
                    grpName = grp[0]

                    # g_ctrlGrp[i]に詰める
                    g_ctrlGrp[i].curveName = ctrl
                    g_ctrlGrp[i].grpName = grpName
                    break

        # 接続フラグをオンにし、多重に処理されないようにする
        IS_CTRL_CONNECTED = True
        addLog(f"Reconnect : 作成済みコントローラーを再接続しました", "V_Select_Log")

# --------------------
# コントローラー選択状態に応じてボタン色を変更
# --------------------
def updateSelectButton():
    global IS_CTRL_CONNECTED

    # スクリプトを開く前にコントローラーが作成されていた場合はg_ctrlGrpに詰められていないため詰めなおす
    if not IS_CTRL_CONNECTED:
        nurbs = cmds.ls(type="nurbsCurve")
        if nurbs:
            reconnectController(nurbs)

    sel = cmds.ls(sl=True) or []

    ACTIVE_COLOR = [0.3, 0.4, 0.5]
    DEFAULT_COLOR = [0.365, 0.365, 0.365]

    for i in range(len(V_JOINTS)):
        if g_ctrlGrp[i].curveName in sel:
            cmds.button(f"V_Select{KEY_NAMES[i]}Button", edit=True, bgc=ACTIVE_COLOR)
        else:
            cmds.button(f"V_Select{KEY_NAMES[i]}Button", edit=True, bgc=DEFAULT_COLOR)

# --------------------
# キーフレームが打たれているコントローラーを収集
# --------------------
def collectAnimation():
    animCtrls = []

    # キーが打たれているコントローラーをリストに詰める
    for i in range(len(g_ctrlGrp)):
        ctrl = g_ctrlGrp[i].curveName

        # コントローラー自体が存在しない場合は弾く
        if not cmds.objExists(ctrl):
            addLog(f"Error : コントローラーが作成されていません\n[CTRL作成]タブからコントローラーを作成してください", "V_AnimManager_Log")
            return

        # キーフレーム取得
        key = cmds.keyframe(ctrl, query=True, keyframeCount=True) or 0

        # 1以上あるならリストに詰める
        if key > 0:
            animCtrls.append(ctrl)

    # ログ出力
    if len(animCtrls) > 0:
        addLog(f"Result : アニメーションが存在\n{animCtrls}", "V_AnimManager_Log")
        return True
    else:
        addLog(f"Result : アニメーションが存在しません", "V_AnimManager_Log")
        return False

# --------------------
# コントローラーを初期姿勢に戻す
# --------------------
def initPause(log):
    # 全コントローラーを取得
    ctrls = getController()

    for ctrl in ctrls:
        cmds.setAttr(f"{ctrl}.rotateX", 0)
        cmds.setAttr(f"{ctrl}.rotateY", 0)
        cmds.setAttr(f"{ctrl}.rotateZ", 0)

    addLog("Result : コントローラー回転値を初期姿勢にリセットしました", log)

# --------------------
# コントローラーをタイムエディタに登録
# --------------------
def addTimeEditor():
    # コントローラーまたはキーが存在しない場合はそれ以上処理しない
    if not collectAnimation():
        addLog("Error : アニメーションが存在しないため、処理がスキップされました", "V_AnimManager_Log")
        return

    # アニメーション名をコンポジションとトラックの名前にする
    # 入力されていなければ弾く
    animName = cmds.textField("V_AnimationName", query=True, text=True)
    if not animName:
        addLog("Error : アニメーション名が入力されていません", "V_AnimManager_Log")
        return

    # 全コントローラーを取得
    ctrls = getController()

    try:
        # コンポジションが存在しなければ新規作成
        comps = cmds.timeEditorComposition(query=True, allCompositions=True) or []
        if animName in comps:
            cmds.timeEditorComposition(animName, edit=True, active=True)
            addLog(f"Log : コンポジションを[{animName}]に切り替えました", "V_AnimManager_Log")
        else:
            cmds.timeEditorComposition(animName, active=True)
            addLog(f"Log : コンポジション[{animName}]を新規作成しました", "V_AnimManager_Log")

        # コンポジションに同名アニメーションが既に登録されている場合は弾く
        clips = cmds.timeEditor(allClips='') or []
        for clip in clips:
            clipName = cmds.timeEditorClip(clip, query=True, name=True)

            if animName == clipName:
                addLog(f"Error : クリップ[{animName}]は既に作成されています", "V_AnimManager_Log")
                return

        # アニメーショントラックを作成
        cmds.timeEditorTracks(animName, edit=True, addTrack=1, trackName=animName)

        # パスを生成
        trackPath = f"{animName}|{animName}"

        # コントローラーを選択する
        cmds.select(clear=True)
        cmds.select(ctrls)

        # 開始フレームと終了フレームを取得
        start = cmds.playbackOptions(query=True, minTime=True)

        # タイムエディタにアニメーションクリップを登録
        cmds.timeEditorClip(animName, addSelectedObjects=True, track=trackPath, startTime=start)
        addLog(f"Success : クリップ[{animName}]をコンポジションに登録しました", "V_AnimManager_Log")

        # 初期姿勢に戻す
        isInitPause = cmds.checkBox("V_AddTimeEditor_IsInitPause", query=True, value=True)
        if isInitPause:
            initPause()

        # アクティブなコンポジションをログ出力
        activeComp = cmds.timeEditorComposition(query=True, active=True)
        addLog(f"Log : Active Composition [{activeComp}]", "V_AnimManager_Log")

    # エラーメッセージ
    except Exception as e:
        addLog(f"Error : コンポジションへの登録に失敗しました\n{str(e)}", "V_AnimManager_Log")
        return

    finally:
        # コンポジションを戻す設定の場合は現在のコンポジションを初期のComposition1に戻す
        isInitComp = cmds.checkBox("V_AddTimeEditor_IsInitComp", query=True, value=True)
        if isInitComp:
            comps = cmds.timeEditorComposition(query=True, allCompositions=True) or []
            if "Composition1" in comps:
                cmds.timeEditorComposition("Composition1", edit=True, active=True)
            else:
                cmds.timeEditorComposition("Composition1", active=True)

        # 最後に選択を全て解除する
        cmds.select(clear=True)

# --------------------
# ゲームエクスポータを開く
# --------------------
def openGameExporter():
    # ゲームエクスポータのプラグインとスクリプトをロード
    if not cmds.pluginInfo('gameFbxExporter', query=True, loaded=True):
        cmds.loadPlugin('gameFbxExporter')

    # ゲームエクスポータを開く
    mel.eval('gameFbxExporter;')

# --------------------
# ジョイント選択
# --------------------
def selectJoints():
    # 現在の選択を全て解除
    cmds.select(clear=True)

    # VRoidの実ジョイントを取得
    joints = []
    for i in range(len(g_ctrlGrp)):
        joint = g_ctrlGrp[i].jointName
        if not cmds.objExists(joint):
            continue
        else:
            joints.append(g_ctrlGrp[i].jointName)

    # ジョイントを選択
    if len(joints) > 1:
        cmds.select(joints)
        addLog(f"Success : 全ジョイントを選択しました", "V_AnimManager_Log")

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

# --------------------
# 初期化（ウィンドウ表示直後に呼ぶ）
# --------------------
def init():
    global V_SelectJobID_1
    global V_SelectJobID_2

    # イベント登録
    # 選択されたときおよび選択解除時に発火する
    V_SelectJobID_1 = cmds.scriptJob(event=["SelectionChanged", updateSelectButton],  parent=window)
    V_SelectJobID_2 = cmds.scriptJob(conditionFalse=["SomethingSelected", updateSelectButton], parent=window)

    # 初期化処理
    updateSelectButton()

# --------------------
# ウィンドウ定義
# --------------------
windowID = "V_Window"

# ウィンドウが開かれていたら片付ける
if cmds.window(windowID, exists=True):
    cmds.deleteUI(windowID)

# サイズを固定
window = cmds.window(windowID, title="VRoid Animation", sizeable=False)
cmds.window(window, edit=True, widthHeight=(500, 750))

# --------------------
# ツールをタブ切り替えに対応
# --------------------
cmds.tabLayout("V_ToolTab", innerMarginWidth=5, innerMarginHeight=5)

# --------------------
# 主要ジョイントのチェック
# --------------------
# レイアウトを作成してタブに挿入
cmds.columnLayout("V_JointCheck", adjustableColumn=True)
cmds.tabLayout("V_ToolTab", edit=True, tabLabel=[("V_JointCheck", u"ジョイント取得")])

# ヘッダテキスト表示
cmds.text("V_JointCheck_Header_1", label="Joint Check", h=20, font="boldLabelFont")
cmds.text("V_JointCheck_Header_2", label="VRoidの主要ジョイントの有無をチェック", h=20)
cmds.separator(h=5)

# 見出しテキスト
cmds.text("V_CollectJoint_Text", label="　★ジョイントを取得", h=30, align='left')

# ジョイント数と判定結果を表示する
cmds.rowLayout(f"V_JointCheck_Row{str(i)}", numberOfColumns=2)
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
    cmds.rowLayout(f"V_Joint_Row{str(i)}", numberOfColumns=3)
    if g_Joints[i].enable == IsJoint(0):
        cmds.image(f"V_IsEnable{str(i)}", image="error.png")
    elif g_Joints[i].enable == IsJoint(1):
        cmds.image(f"V_IsEnable{str(i)}", image="confirm.png")
    else:
        cmds.image(f"V_IsEnable{str(i)}", image="help.png")

    cmds.text(f"V_JointKey{str(i)}_Text", label=f"{g_Joints[i].jointKey} : ", h=16, align='left')
    cmds.text(f"V_JointName{str(i)}_Text", label=g_Joints[i].name, h=16, align='left')
    cmds.setParent("..")
cmds.setParent("..")
cmds.setParent("..")

# ボタン
cmds.separator(h=5)
cmds.button("V_CollectJoint_Button", label="ジョイントをチェック", w=25, h=25, command=lambda *args:collectJoint())
cmds.separator(h=5)

# ログ
cmds.text("V_JointCheck_LogText", label="　★ログ", h=30, align='left')
cmds.scrollField("V_JointCheck_Log", text="", h=60, editable=False)
cmds.button("V_JointCheck_LogClear", label="ログをクリア", h=25, command=lambda *args:logClear("V_JointCheck_Log"))

# レイアウトから出る
cmds.setParent("..")

# --------------------
# コントローラー作成
# --------------------
# レイアウトを作成してタブに挿入
cmds.columnLayout("V_Controller", adjustableColumn=True)
cmds.tabLayout("V_ToolTab", edit=True, tabLabel=[("V_Controller", u"CTRL作成")])

# ヘッダテキスト
cmds.text("V_Controller_Header_1", label="Create Controller", h=20, font="boldLabelFont")
cmds.text("V_Controller_Header_2", label="VRoidジョイントにコントローラーを追加", h=20)
cmds.separator(h=5)

# コントローラー名のprefixとsuffixの入力
cmds.text("V_CollectJoint_Text", label="　★コントローラー作成", h=30, align='left')
cmds.text("V_ControllerPreSuf_Text", label="　　☆オブジェクト先頭・末尾テキスト", h=30, align='left')

# prefix
cmds.rowLayout("V_Controller_Prefix_Row", numberOfColumns=2)
cmds.text("V_Controller_Prefix_Text", label="　　　Prefix : ", h=20, align='left')
cmds.textField("V_Controller_Prefix", text="V_", w=100, h=20)
cmds.setParent("..")

# suffix
cmds.rowLayout("V_Controller_Suffix_Row", numberOfColumns=2)
cmds.text("V_Controller_Suffix_Text", label="　　　Suffix : ", h=20, align='left')
cmds.textField("V_Controller_Suffix", text="_Ctrl", w=100, h=20)
cmds.setParent("..")

# コントローラー半径を指定
cmds.text("V_ControllerRadius_Text", label="　　☆コントローラー半径", h=30, align='left')
cmds.intSliderGrp("V_Controller_Radius_Slider", label="　　　Radius : ", field=True, minValue=1, maxValue=10, value=1,
                columnWidth3=[80, 100, 100], columnAlign3=["left", "left", "left"] )

# ボタン
cmds.separator(h=5)
cmds.button("V_Controller_Button", label="コントローラーを作成", w=25, h=25, command=lambda *args:createController())
cmds.separator(h=5)

# ログ
cmds.text("V_Controller_LogText", label="　★ログ", h=30, align='left')
cmds.scrollField("V_Controller_Log", text="", h=250, editable=False)
cmds.button("V_Controller_LogClear", label="ログをクリア", h=25, command=lambda *args:logClear("V_Controller_Log"))

# レイアウトから出る
cmds.setParent("..")

# --------------------
# ソケット作成
# --------------------
# レイアウトを作成してタブに挿入
cmds.columnLayout("V_Socket", adjustableColumn=True)
cmds.tabLayout("V_ToolTab", edit=True, tabLabel=[("V_Socket", u"ソケット作成")])

# ヘッダテキスト
cmds.text("V_Socket_Header_1", label="Create Socket", h=20, font="boldLabelFont")
cmds.text("V_Socket_Header_2", label=".アクセサリー用ソケットを追加", h=20)
cmds.separator(h=5)

# ソケット名のprefixとsuffixの入力
cmds.text("V_Socket_Text", label="　★ソケット作成", h=30, align='left')
cmds.text("V_SocketPreSuf_Text", label="　　☆オブジェクト先頭・末尾テキスト", h=30, align='left')

# prefix
cmds.rowLayout("V_Socket_Prefix_Row", numberOfColumns=2)
cmds.text("V_Socket_Prefix_Text", label="　　　Prefix : ", h=20, align='left')
cmds.textField("V_Socket_Prefix", text="V_", w=100, h=20)
cmds.setParent("..")

# suffix
cmds.rowLayout("V_Socket_Suffix_Row", numberOfColumns=2)
cmds.text("V_Socket_Suffix_Text", label="　　　Suffix : ", h=20, align='left')
cmds.textField("V_Socket_Suffix", text="_Socket", w=100, h=20)
cmds.setParent("..")

# ソケット作成部位の設定
cmds.text("V_Socket_Setting_Text", label="　　☆ソケット作成部位指定", h=30, align='left')
cmds.rowLayout("V_Socket_IsHand_Row", numberOfColumns=4)
cmds.text("V_Socket_IsHand_Blank", label="　　　", align='left')
cmds.checkBox("V_Socket_IsLeftHand", label="L_Hand　", align='left', value=True)
cmds.checkBox("V_Socket_IsRightHand", label="R_Hand　", align='left', value=True)
cmds.checkBox("V_Socket_IsChest", label="Chest", align='left', value=True)
cmds.setParent("..")

# 作成
cmds.separator(h=5)
cmds.button("V_Socket_Button", label="ソケットを作成", w=25, h=25, command=lambda *args:createSocket())
cmds.separator(h=5)

# 出力
cmds.text("V_Socket_Export_Text", label="　★CSV出力", h=30, align='left')
cmds.separator(h=5)
cmds.button("V_Socket_Export_Button", label="選択ソケットをCSV出力", w=25, h=25, command=lambda *args:exportSockets())
cmds.separator(h=5)

# ログ
cmds.text("V_Socket_LogText", label="　★ログ", h=30, align='left')
cmds.scrollField("V_Socket_Log", text="", h=60, editable=False)
cmds.button("V_Socket_LogClear", label="ログをクリア", h=25, command=lambda *args:logClear("V_Socket_Log"))

# レイアウトから出る
cmds.setParent("..")

# --------------------
# コントローラーの選択状態を制御
# --------------------
# レイアウトを作成してタブに挿入
cmds.columnLayout("V_Select", adjustableColumn=True)
cmds.tabLayout("V_ToolTab", edit=True, tabLabel=[("V_Select", u"CTRL選択")])

# ヘッダテキスト
cmds.text("V_Select_Header_1", label="Select Controller", h=20, font="boldLabelFont")
cmds.text("V_Select_Header_2", label="コントローラーの選択状態を制御", h=20)
cmds.separator(h=5)

# 選択解除
cmds.button("V_SelectClear_Button", label="全ての選択を解除", h=25, command=lambda *args:clearSel())
cmds.separator(h=5)
cmds.button("V_InitPauseSel_Button", label="初期姿勢に戻す", w=100, h=25, command=lambda *args:initPause("V_Select_Log"))
cmds.separator(h=5)

# createSelectButtonに引数として渡すID,要素数,開始配列番号
# 引数として渡す際に加算するため、明示的に指定する必要があるのはrowのみ
num = 0
row = 0
idOffset = 0

# 縦に長いためスクロールレイアウトを使う
cmds.scrollLayout(h=500, childResizable=True)

# センターラインのコントローラー群
# 折り畳み可能なレイアウトにする
cmds.frameLayout("V_Select_Frame_Center", label="Center", collapsable=True)
# Root, Hips
cmds.text("V_Select_Center_Text1", label="　★体幹", align='left')
createSelectButton(num:= num + 1, idOffset, row:= 2)
# Spine～UpperChest
cmds.text("V_Select_Center_Text2", label="　★胴", align='left')
createSelectButton(num:= num + 1, idOffset:= idOffset + row, row:= 3)
# Neck, Head
cmds.text("V_Select_Center_Text3", label="　★頭部", align='left')
createSelectButton(num:= num + 1, idOffset:= idOffset + row, row:= 2)
cmds.setParent("..")

# 肩～手首のコントローラー群
cmds.frameLayout("V_Select_Frame_UpperLimb", label="Upper Limb", collapsable=True)
# Shoulder
cmds.text("V_Select_UpperLimb_Text1", label="　★肩", align='left')
createSelectButton(num:= num + 1, idOffset:= idOffset + row, row:= 2)
# UpperArm
cmds.text("V_Select_UpperLimb_Text2", label="　★上腕", align='left')
createSelectButton(num:= num + 1, idOffset:= idOffset + row, row:= 2)
# LowerArm
cmds.text("V_Select_UpperLimb_Text3", label="　★下腕", align='left')
createSelectButton(num:= num + 1, idOffset:= idOffset + row, row:= 2)
# Hand
cmds.text("V_Select_UpperLimb_Text4", label="　★手首", align='left')
createSelectButton(num:= num + 1, idOffset:= idOffset + row, row:= 2)
cmds.setParent("..")

# 下半身のコントローラー群
cmds.frameLayout("V_Select_Frame_LowerLimb", label="Lower Limb", collapsable=True)
# UpperLeg
cmds.text("V_Select_LowerLimb_Text1", label="　★大腿", align='left')
createSelectButton(num:= num + 1, idOffset:= idOffset + row, row:= 2)
# LowerLeg
cmds.text("V_Select_LowerLimb_Text2", label="　★下肢", align='left')
createSelectButton(num:= num + 1, idOffset:= idOffset + row, row:= 2)
# Foot
cmds.text("V_Select_LowerLimb_Text3", label="　★足", align='left')
createSelectButton(num:= num + 1, idOffset:= idOffset + row, row:= 2)
# Toes
cmds.text("V_Select_LowerLimb_Text4", label="　★爪先", align='left')
createSelectButton(num:= num + 1, idOffset:= idOffset + row, row:= 2)
cmds.setParent("..")

# 指のコントローラー群
cmds.frameLayout("V_Select_Frame_Finger", label="Finger", collapsable=True)
# Thumb
cmds.text("V_Select_Finger_Text1", label="　★親指", align='left')
createSelectButton(num:= num + 1, idOffset:= idOffset + row, row:= 2)
createSelectButton(num:= num + 1, idOffset:= idOffset + row, row:= 2)
createSelectButton(num:= num + 1, idOffset:= idOffset + row, row:= 2)
# Index
cmds.text("V_Select_Finger_Text2", label="　★人差し指", align='left')
createSelectButton(num:= num + 1, idOffset:= idOffset + row, row:= 2)
createSelectButton(num:= num + 1, idOffset:= idOffset + row, row:= 2)
createSelectButton(num:= num + 1, idOffset:= idOffset + row, row:= 2)
# Middle
cmds.text("V_Select_Finger_Text3", label="　★中指", align='left')
createSelectButton(num:= num + 1, idOffset:= idOffset + row, row:= 2)
createSelectButton(num:= num + 1, idOffset:= idOffset + row, row:= 2)
createSelectButton(num:= num + 1, idOffset:= idOffset + row, row:= 2)
# Ring
cmds.text("V_Select_Finger_Text4", label="　★薬指", align='left')
createSelectButton(num:= num + 1, idOffset:= idOffset + row, row:= 2)
createSelectButton(num:= num + 1, idOffset:= idOffset + row, row:= 2)
createSelectButton(num:= num + 1, idOffset:= idOffset + row, row:= 2)
# Little
cmds.text("V_Select_Finger_Text5", label="　★小指", align='left')
createSelectButton(num:= num + 1, idOffset:= idOffset + row, row:= 2)
createSelectButton(num:= num + 1, idOffset:= idOffset + row, row:= 2)
createSelectButton(num:= num + 1, idOffset:= idOffset + row, row:= 2)
cmds.setParent("..")

cmds.setParent("..")

cmds.separator(h=5)

# ログ
cmds.text("V_Select_LogText", label="　★ログ", h=30, align='left')
cmds.scrollField("V_Select_Log", text="", h=60, editable=False)
cmds.button("V_Select_LogClear", label="ログをクリア", h=25, command=lambda *args:logClear("V_Select_Log"))

# レイアウトから出る
cmds.setParent("..")

# --------------------
# アニメーションの管理
# --------------------
# レイアウトを作成してタブに挿入
cmds.columnLayout("V_AnimManager", adjustableColumn=True)
cmds.tabLayout("V_ToolTab", edit=True, tabLabel=[("V_AnimManager", u"アニメーション")])

# ヘッダテキスト
cmds.text("V_AnimManager_Header_1", label="Animation Manager", h=20, font="boldLabelFont")
cmds.text("V_AnimManager_Header_2", label="アニメーションの管理", h=20)
cmds.separator(h=5)

# タイムエディタを開く
cmds.button("V_TimeEditor_Button", label="タイムエディタを開く", w=25, h=25, command=lambda *args:mel.eval("TimeEditorWindow;"))
cmds.separator(h=5)

# アニメーション名設定
cmds.text("V_AnimationName_Text", label="　★アニメーション名入力", h=30, align='left')
cmds.rowLayout("V_AnimationName_Row", numberOfColumns=2)
cmds.text("V_AnimationName_Blank", label="　　", h=20, align='left')
cmds.textField("V_AnimationName", text="", w=100, h=20)
cmds.setParent("..")

# アニメーションが存在するか取得
cmds.text("V_Module_Text", label="　★補助機能", h=30, align='left')
cmds.rowLayout("V_CollectAnimation_Row", numberOfColumns=2)
cmds.text("V_CollectAnimation_Blank", label="　　", h=20, align='left')
cmds.button("V_CollectAnimation_Button", label="アニメーション取得", w=100, h=25, command=lambda *args:collectAnimation())
cmds.setParent("..")

# 初期姿勢に戻す
cmds.rowLayout("V_InitPause_Row", numberOfColumns=2)
cmds.text("V_InitPause_Blank", label="　　", h=20, align='left')
cmds.button("V_InitPause_Button", label="初期姿勢に戻す", w=100, h=25, command=lambda *args:initPause("V_AnimManager_Log"))
cmds.setParent("..")

# タイムエディタ出力時の設定
# 初期姿勢に戻すか
cmds.text("V_AddTimeEditor_Setting_Text", label="　★タイムエディタ出力後の処理", h=30, align='left')
cmds.rowLayout("V_AddTimeEditor_IsInitPause_Row", numberOfColumns=2)
cmds.text("V_AddTimeEditor_IsInitPause_Blank", label="　　", align='left')
cmds.checkBox("V_AddTimeEditor_IsInitPause", label="初期姿勢に戻す", align='left', value=True)
cmds.setParent("..")

# 初期コンポジションに戻すか
cmds.rowLayout("V_AddTimeEditor_IsInitComp_Row", numberOfColumns=2)
cmds.text("V_AddTimeEditor_IsInitComp_Blank", label="　　", align='left')
cmds.checkBox("V_AddTimeEditor_IsInitComp", label="初期コンポジションをアクティブにする", align='left', value=True)
cmds.setParent("..")

# タイムエディタに登録
cmds.separator(h=5)
cmds.button("V_AddTimeEditor_Button", label="アニメーションをタイムエディタに登録", w=25, h=25, command=lambda *args:addTimeEditor())
cmds.separator(h=5)

# ジョイント全選択
cmds.text("V_AnimExport_Text", label="　★出力", h=30, align='left')
cmds.rowLayout("V_JointSel_Row", numberOfColumns=2)
cmds.text("V_JointSel_Blank", label="　　", h=20, align='left')
cmds.button("V_JointSel_Button", label="ジョイント全選択", w=100, h=25, command=lambda *args:selectJoints())
cmds.setParent("..")
cmds.separator(h=5)

# ゲームエクスポータを開く
cmds.button("V_Exporter_Button", label="ゲームエクスポータを開く", w=25, h=25, command=lambda *args:openGameExporter())
cmds.separator(h=5)

# ログ
cmds.text("V_AnimManager_LogText", label="　★ログ", h=30, align='left')
cmds.scrollField("V_AnimManager_Log", text="", h=60, editable=False)
cmds.button("V_AnimManager_LogClear", label="ログをクリア", h=25, command=lambda *args:logClear("V_AnimManager_Log"))

# レイアウトから出る
cmds.setParent("..")

# --------------------
# UI表示・初期化
# --------------------
cmds.setParent("..")
cmds.showWindow(window)
init()
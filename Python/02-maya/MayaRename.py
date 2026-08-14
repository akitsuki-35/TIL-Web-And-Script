#===========================================================
    # file    : MayaRename.py
    # brief   : リネームツール
    # author  : @akitsuki-35（https://github.com/akitsuki-35）
    # date    : 2026/06/17
    # updated : 2026/06/24
#===========================================================
import maya.cmds as cmds
if cmds.window("Sample_Window", exists=True):
    cmds.deleteUI("Sample_Window")
window = cmds.window("Sample_Window", title="Rename Tool", widthHeight=(700, 700))

# ====================
# �֐���`
# ====================
# --------------------
# ���l�[�����s
# --------------------
def Rename():
    # ������̒u������
    replaceOld = cmds.textField("textfieldReplaceOld", query=True, text=True)
    replaceNew = cmds.textField("textfieldReplaceNew", query=True, text=True)
    
    # �擪�ɒǉ����镶����
    prefix = cmds.textField("textfieldPrefix", query=True, text=True)
    
    # �����ɒǉ����镶����
    suffix = cmds.textField("textfieldSuffix", query=True, text=True)
    
    # �������镶����
    search = cmds.textField("textfieldSearch", query=True, text=True)
    
    # ���O�ύX
    select = cmds.ls(sl=True)
    for sel in select:
        newName = prefix +  sel.replace(replaceOld, replaceNew)
        cmds.rename(sel, newName + suffix) 
        
    # �����񌟍�
        if search:
            print("----------�����񌟍����ʁ[�[�[�[�[�[�[�[�[�[")
            for sel in select:
                if search in sel:
                    print(sel)

# --------------------
# �ԍ��t��
# --------------------
def Number():

    # �I�𒆃I�u�W�F�N�g�擾
    selectList = cmds.ls(sl=True)

    # �ŏ��ɑI�������I�u�W�F�N�g�̖��O�����o��
    baseName = selectList[0]

    num = 1

    for sel in selectList:
        print(baseName + "_0" + str(num))
        cmds.rename(sel, baseName + "_0" + str(num))
        num += 1

# ====================
# UI����
# ====================

# --------------------
# ���s�{�^��
# --------------------

cmds.columnLayout("columnExecution", adjustableColumn=True)

cmds.text("textRename", label="���l�[�� �c�[��", h=50)

cmds.button("buttonExecution", label="���l�[�����s", command=lambda *args:Rename(), h=50)

cmds.separator(height=20)

# --------------------
# ��������
# --------------------

cmds.text("textReplace", label="��������", h=30)

cmds.setParent("..")

cmds.rowLayout("rowReplace", numberOfColumns=3)

cmds.textField("textfieldReplaceOld", text="", w=200)
cmds.textField("textfieldReplaceNew", text="", w=200)

cmds.separator(height=20)
cmds.setParent("..")

# --------------------
# ���ɕ�����ǉ�
# --------------------
cmds.columnLayout("columnPrefix", adjustableColumn=True)

cmds.separator(height=20)
cmds.text("textPrefix", label="�擪�ɕ�����ǉ�", h=30)

cmds.textField("textfieldPrefix", text="", w=200)

cmds.separator(height=20)
cmds.setParent("..")

# --------------------
# �����ɕ�����ǉ�
# --------------------
cmds.columnLayout("columnSuffix", adjustableColumn=True)

cmds.separator(height=20)
cmds.text("textSuffix", label="�����ɕ�����ǉ�", h=30)

cmds.textField("textfieldSuffix", text="", w=200)

cmds.separator(height=20)
cmds.setParent("..")

# --------------------
# �����񌟍�
# --------------------
cmds.columnLayout("columnSearch", adjustableColumn=True)

cmds.separator(height=20)
cmds.text("textSearch", label="�����񌟍�", h=30)

cmds.textField("textfieldSearch", text="", w=200)

cmds.separator(height=20)
cmds.setParent("..")

# --------------------
# �ԍ��t��
# --------------------
cmds.columnLayout("columnNumber", adjustableColumn=True)

cmds.button("buttonNumber", label="�ԍ��t��", command=lambda *args:Number())

cmds.setParent("..")

# --------------------
# �I��
# --------------------

cmds.setParent("..")# ���C�A�E�g�I��
cmds.showWindow(window)
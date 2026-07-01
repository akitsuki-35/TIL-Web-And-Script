#===========================================================
    # file    : function.py
    # brief   : 関数定義
    # author  : @akitsuki-35（https://github.com/akitsuki-35）
    # date    : 2026/05/27
    # updated : 2026/05/27
#===========================================================
#  ミキサーの関数定義
def Mixer(inputA, inputB):
    return (inputA + "と" + inputB + "のミックスジュース");

cup = Mixer("バナナ", "牛乳");
print(cup);
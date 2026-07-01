#===========================================================
    # file    : test.py
    # brief   : Pythonテスト
    # author  : @akitsuki-35（https://github.com/akitsuki-35）
    # date    : 2026/05/13
    # updated : 2026/05/28
#===========================================================
printlist: list[str] = ["test1", "test2", "test3", "test4",
                        "text5", "text6", "text7", "text8"];

# リストから"text"を含む文字列のみを出力する
for i in printlist:
    if "text" in i:
        print(i);

## index = 1;
for j in range(5):
    print(j);
    j += 1;

# Pythonのif文
x = 10;
if x > 10:
    print("xは10より大きい");
elif x == 10:
    print("xは10と等しい");
else:
    print("xは10より小さい");

# Pythonの変数定義
x = "みかん";
y = 3;

print(x, y);

# 分割文字
a = "METANOIA"
print(a.split("I" + "A"));

# 置換
replace = "TESTAMENT"
print( replace.replace(replace, "METANOIA") )
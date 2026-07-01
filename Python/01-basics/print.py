#===========================================================
    # file    : print.py
    # brief   : 文字列操作
    # author  : @akitsuki-35（https://github.com/akitsuki-35）
    # date    : 2026/05/27
    # updated : 2026/05/27
#===========================================================
def PrintNumberList():
    numberList = ["1","2","3","4","5",
                "6","7","8","9","10"];
    for num in numberList:
        printText = "text_" + num;

        printText = printText.replace("text","maya");
        printText = "A" + printText;
        printText = printText.split("_");
        print(printText);

# 実行
for i in range(10):
    PrintNumberList();
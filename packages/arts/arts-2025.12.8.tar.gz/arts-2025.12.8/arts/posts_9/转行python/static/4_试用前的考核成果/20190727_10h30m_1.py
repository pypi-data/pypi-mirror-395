""" 第一个python游戏 Python冒险世界 """
import random
import time
#  游戏介绍
print("\n（ 友 情 提 示：游 戏 过 程 中，请 通 过 按 “Enter” 键 进 入 下 一 步 ）")
next = input (">>>")
print("\n    游戏介绍：Python冒险世界是一款十分有趣的小游戏，游戏中设置了众多锻炼反应力和逻辑能力的关卡，比如打地鼠、五子棋。")
next = input (">>>")
print("\n    欢迎来到 Python冒险世界！")

#  选择服务区
next = input (">>>")
account = "中国"
password1 = "福建"
password2 = "福建省"
print("    选择服务区：\n\n    （根据您的网络位置，推荐您选择 中国-福建省 服务区）")
user_account = input("\n请输入您选择的国家区域：")
user_password = input("请输入您选择的省份区域：")
#  强制选择 中国-福建省 服务区，设置这个小互动，目的模拟出“网络游戏”的氛围，激起玩家的兴趣。
while not (user_account == account and (user_password == password1 or user_password == password2)):
    print("\n    当前网络不稳定，建议您重新选择服务区")
    user_account = input("请输入您选择的国家区域：")
    user_password = input("请输入您选择的省份区域：")
else:
    print("\n    您已成功进入 中国-福建省 服务区！人生苦短，赶快开始您的冒险吧！")

#  创建角色
next = input (">>>")
hero = input("在踏上征程之前，请先留下您的昵称：")
print("\n    你好，"+hero+"！我是你的伙伴小许，接下来我将会带领你在Python世界里冒险。")

#  第一关：打地鼠
next = input (">>>")
print("    《第一关  打地鼠》")
next = input (">>>")
print("    前面有一群地鼠挡住了我们的去路，需要您发挥出超凡的反应力，将这些地鼠全部打跑")
next = input (">>>")
print("    请通过小键盘（1～9）来选择地鼠，按“Enter”键确认击打，共有20只地鼠，展现你超凡的反应力吧！")
next = input (">>>")
print("\n\n              ＜ 已开始计时 ＞")
time1 = time.time()
hamster = ['O'] * 9
number = error = 0
while number < 20:
    x = random.randint(0,8)
    hamster[x] = "X"
    print("\n\n               "+hamster[6]+"      "+hamster[7]+"      "+hamster[8]+
          "\n\n               "+hamster[3]+"      "+hamster[4]+"      "+hamster[5]+
          "\n\n               "+hamster[0]+"      "+hamster[1]+"      "+hamster[2])
    s = input("请输入：")
    while not s == str(x+1):
        error += 1
        print("    很遗憾，打空了，您已累计打中"+str(number)+"只地鼠，累计失误"+str(error)+"次，当前还剩"+str(20-number)+"只地鼠")
        s = input("请输入：")
    else:
        number += 1
        hamster[x] = "O"
        print("    打中啦！您已累计打中"+str(number)+"只地鼠，累计失误"+str(error)+"次，当前还剩"+str(20-number)+"只地鼠")
else:
    print("\n\n    恭喜！您已成功打跑全部地鼠！共计用时 "+str((time.time()-time1)//1)+" S。\n\n")

#  第二关：五子棋
print("\n\n\n    《第二关  五子棋》")
next = input (">>>")
print("    前面那座山好像就是著名的庐山，山上很可能隐藏着神秘宝物，我们上去看看吧")
next = input (">>>")
print("    前面好像有两个人正在下棋，走，过去看看")
next = input (">>>")
print("    原来是两个守山大神欧阳修和苏轼正在下棋，")
next = input (">>>")
print("    苏轼：你们想上山？哈哈，这座山地势千变万化，没有我的地图，任何人都上不去的")
next = input (">>>")
print("    苏轼：只要你能赢了我的五子棋，我就把地图给你。")
next = input (">>>")
print("    我：……")
next = input (">>>")
print("    苏轼：你不用太紧张啦，这样吧，如果我先连成了五颗棋子，咱就当没看见继续下，直到你连成了五颗棋子，便算你赢。")
next = input (">>>")
print("    没办法，跟他下一盘吧……")
next = input (">>>")
print("    游戏规则：根据棋盘上的数字提示，输入落棋坐标，按“Enter”键确认。\n\n\
              玩家棋子以 O 表示，苏轼棋子以 X 表示。\n\n\
              玩家先落子，先在棋盘上连成连续的五颗棋子者为胜。")
next = input (">>>")
print("    按“Enter”键开始游戏")
next = input (">>>")
#  游戏代码
z = range(119,456)
u = list(range(1,553))
x = [1] * 552
a = [1] * 552
b = [1] * 552
c = [1] * 552
d = [1] * 552
k = [1] * 552
s = [20] * 552
count = []
while max(a+b+c+d) < 24300000:
    #  电脑落棋
    for i in z:
        s[i] = ( a[i]+a[i-1]+a[i-2]+a[i-3]+a[i-4] + b[i]+b[i-23]+b[i-46]+b[i-69]+b[i-92] +
                 c[i]+c[i-22]+c[i-44]+c[i-66]+c[i-88] + d[i]+d[i-24]+d[i-48]+d[i-72]+d[i-96] )
    for f in range(0,552):
        k[f] = s[f]
    for h in count:
        k[h] = 0
    x[k.index(max(k))] = 0
    u[k.index(max(k))] = " X "
    count.append(k.index(max(k)))
    #  打印棋盘
    for w in range(5,20):
        for v in range(4,19):
            print(u[23*w+v],end = "  ")
        print("\n")
    #  玩家落棋
    user = int(input("请选择：")) -1
    x[user] = 30
    u[user] = " O "
    count.append(user)
    for j in z:
        a[j] = x[j] * x[j+1] * x[j+2] * x[j+3] * x[j+4]
        b[j] = x[j] * x[j+23] * x[j+46] * x[j+69] * x[j+92]
        c[j] = x[j] * x[j+22] * x[j+44] * x[j+66] * x[j+88]
        d[j] = x[j] * x[j+24] * x[j+48] * x[j+72] * x[j+96]
else:
    #  打印棋盘
    for w in range(5,20):
        for v in range(4,19):
            print(u[23*w+v],end = "  ")
        print("\n")
    print("恭喜，您已取得胜利！您与苏轼共下了"+str(len(count)//2)+"步棋子之后取胜，水平很不错呀！\n\n")
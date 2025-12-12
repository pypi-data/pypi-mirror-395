RESET = "\033[0m"

# red 
def printred(txt):
    print(f"\033[31m{txt}{RESET}")

def printred2(txt):
    print(f"\033[91m{txt}{RESET}")

def printr(txt):
    print(f"\033[31m{txt}{RESET}")

def printr2(txt):
    print(f"\033[91m{txt}{RESET}")

# green
def printgreen(txt):
    print(f"\033[32m{txt}{RESET}")

def printg(txt):
    print(f"\033[32m{txt}{RESET}")

def printgreen2(txt):
    print(f"\033[92m{txt}{RESET}")

def printg2(txt):
    print(f"\033[92m{txt}{RESET}")

# yellow
def printyellow(txt):
    print(f"\033[33m{txt}{RESET}")

def printy(txt):
    print(f"\033[33m{txt}{RESET}")

def printyellow2(txt):
    print(f"\033[93m{txt}{RESET}")

def printy2(txt):
    print(f"\033[93m{txt}{RESET}")

# blue
def printblue(txt):
    print(f"\033[34m{txt}{RESET}")

def printblue2(txt):
    print(f"\033[94m{txt}{RESET}")

def printb(txt):
    print(f"\033[34m{txt}{RESET}")

def printb2(txt):
    print(f"\033[94m{txt}{RESET}")

# purple
def printpurple(txt): 
    print(f"\033[35m{txt}{RESET}")

def printpurple2(txt):
    print(f"\033[95m{txt}{RESET}")

def printp(txt): 
    print(f"\033[35m{txt}{RESET}")

def printp2(txt):
    print(f"\033[95m{txt}{RESET}")

# cyan
def printcyan(txt):
    print(f"\033[36m{txt}{RESET}")

def printcyan2(txt):
    print(f"\033[96m{txt}{RESET}")

def printc(txt):
    print(f"\033[36m{txt}{RESET}")

def printc2(txt):
    print(f"\033[96m{txt}{RESET}")

# grey
def printgrey(txt):
    print(f"\033[37m{txt}{RESET}")

def printgrey2(txt):
    print(f"\033[90m{txt}{RESET}")

def printgrey3(txt):
    print(f"\033[30m{txt}{RESET}")

def printgy(txt):
    print(f"\033[37m{txt}{RESET}")

def printgy2(txt):
    print(f"\033[90m{txt}{RESET}")

def printgy3(txt):
    print(f"\033[30m{txt}{RESET}")

# white
def printwhite(txt):
    print(f"\033[97m{txt}{RESET}")

def printw(txt):
    print(f"\033[97m{txt}{RESET}")


# ===== 测试 =====
if __name__ == "__main__":
    printred("red 红色")
    printred2("red2 红色")
    printr("r 红色")
    printr2("r2 红色")

    printgreen("green 绿色")
    printgreen2("green2 绿色")
    printg("g 绿色")
    printg2("g2 绿色")

    printyellow("yellow 黄色")
    printyellow2("yellow2 黄色")
    printy("y 黄色")
    printy2("y2 黄色")

    printblue("blue 蓝色")
    printblue2("blue2 蓝色")
    printb("b 蓝色")
    printb2("b2 蓝色")

    printpurple("purple 紫色")
    printpurple2("purple2 紫色")
    printp("p 紫色")
    printp2("p2 紫色")

    printcyan("cyan 青色")
    printcyan2("cyan2 青色")
    printc("c 青色")
    printc2("c2 青色")

    printgrey("grey 灰色")
    printgrey2("grey2 灰色")
    printgrey3("grey3 灰色")
    printgy("gy 灰色")
    printgy2("gy2 灰色")
    printgy3("gy3 灰色")

    printwhite("white 白色")
    printw("w 白色")
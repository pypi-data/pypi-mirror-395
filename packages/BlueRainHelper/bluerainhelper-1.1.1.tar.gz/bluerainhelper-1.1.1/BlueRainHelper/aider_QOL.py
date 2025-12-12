import os

def pause(msg = "Press Enter To Continue..."):
    """Pause the terminal until user press 'Enter'."""
    input("\n" + msg)

def makingSure(msg = "Are You Sure? (y/n) : " ):
    """Let user making sure of their choice."""
    confirmation = input("\n" + msg)
    if confirmation.strip().lower() in ["y", "yes"]:
        return True
    else:
        return False
    
def wipeScreen():
    """Clear terminal Screen."""
    if os.name == "nt":
        cmd = "cls"
    else:
        cmd = "clear"
    os.system(cmd)

def successText(msg = "success"):
    """Print text, color = green"""
    print(f"\033[0;32m{msg}\033[0m")

def dangerText(msg = "danger"):
    """Print text, color = red"""
    print(f"\033[0;31m{msg}\033[0m")

def warningText(msg = "warning"):
    """Print text, color = red"""
    print(f"\033[0;33m{msg}\033[0m")

def customText(msg = "custom", fg = 0, bg = 0, italic = 0, underline = 0):
    fgList = [
    "\033[1;37m", "\033[0;30m", "\033[0;31m", "\033[0;32m", 
    "\033[0;33m", "\033[0;34m", "\033[0;35m", "\033[0;36m", 
    "\033[1;30m", "\033[1;31m", "\033[1;33m"]

    bgList = [
    "\033[40m", "\033[47m", "\033[41m", "\033[42m", 
    "\033[43m", "\033[44m", "\033[45m", "\033[46m", 
    "\033[100m", "\033[101m", "\033[102m"
    ]

    try:
        if 0 <= fg <= 10 and 0 <= bg <= 10:
            if italic == 1:
                print("\033[3m", end="")
            if underline == 1:
                print("\033[4m", end="")
            print ( fgList[fg] + bgList[bg] + msg + "\033[0m")
        else :
            print ("fg and bg must be 0 - 10")
    except:
        print("fg and bg must be int between 0 - 10")

    





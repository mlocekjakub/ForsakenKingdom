import sys
import os

def key_pressed():
    try:
        import tty, termios
    except ImportError:
        try:
            # probably Windows
            import msvcrt
        except ImportError:
            # FIXME what to do on other platforms?
            raise ImportError('getch not available')
        else:
            key = msvcrt.getch().decode('utf-8')
            return key
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


def clear_screen():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')

def get_input(label,new_lines=2,filler=4,center=False):
    new_lines = "\n" * new_lines
    if not center:
        user_input = input(f"{new_lines}{filler*' '}{label}: ")
    else:
        print(new_lines)
        label_length = len(label)
        label = f"{label}:".center(119)
        indent = (119 - label_length)//2 + filler
        print(label)
        print()
        user_input = input("".rjust(indent))
    return user_input

def press_any_button(new_lines=0,indent=4,center=False):
    new_lines = "\n" * new_lines
    if os.name == "nt":
        if not center:
            print(f"{new_lines}{indent*' '}Press any key to continue . . .")    
        else:
            print(new_lines)
            print(f"Press any key to continue . . .".center(119))    
        os.system("pause >nul")
    else:
        input(f"{new_lines}Press enter to continue! ")

def get_confirmation(message,new_lines=2):
    new_lines = "\n" * new_lines
    print(new_lines)
    print(f"{message}".center(119))
    print()
    confirmation = input("".rjust(119//2)).lower()
    return confirmation in ["yes", "y"]
        

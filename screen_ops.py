import pyautogui

def move_right():
    pyautogui.moveRel(50, 0)

def move_left():
    pyautogui.moveRel(-50, 0)

def move_up():
    pyautogui.moveRel(0, -50)

def move_down():
    pyautogui.moveRel(0, 50)

def minimize_window():
    pyautogui.hotkey('win', 'down')

def maximize_window():
    pyautogui.hotkey('win', 'up')
import pyautogui as pag
import time
import locate_images

from rich import print
from rich.console import Console

console = Console()

def login(username: str, password: str):
    username_inputbox: pag.Point = pag.locateCenterOnScreen(locate_images.username_input.__str__(), confidence=0.8)
    password_inputbox: pag.Point = pag.locateCenterOnScreen(locate_images.password_input.__str__(), confidence=0.8)
    confirm: pag.Point = pag.locateCenterOnScreen(locate_images.login_confirm_button.__str__())
    
    console.log(f'输入用户名：{username}')
    pag.click(username_inputbox.x, username_inputbox.y)
    pag.typewrite(username)
    
    console.log(f'输入密码：{password[0:3]}...')
    pag.click(password_inputbox.x, password_inputbox.y)
    pag.typewrite(password)
    
    console.log('确认登录')
    pag.click(confirm.x, confirm.y)
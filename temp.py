# import pyautogui as pag

# pag.mouseInfo()

import time
from rich import print
from rich.console import Console
from rich.progress import Progress, track

console = Console()

for i in track(range(10), description='testing'):
    print('hello')
    console.log('fuckyou')
    time.sleep(0.5)
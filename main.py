import pyautogui as pag
import pygetwindow
import pickle
import pathlib
import login
import locate_images
import answer
import time
import config
import adapters
import listening_part

from rich import print
from rich.console import Console
from rich.prompt import Confirm

console = Console()
adapter = adapters.GLMAdapter(api_key=config.zhipuai_apikey)
runtime_dir = pathlib.Path('./runtime').absolute()

def open_window():
    console.log('正在切换ETS到前台')
    
    # 切换窗口到前台
    taskbar: pag.Point = pag.locateCenterOnScreen(locate_images.taskbar_icon.__str__(), confidence=0.8)
    
    pag.click(taskbar.x, taskbar.y)

    console.log('成功切换ETS到前台')

if __name__ == '__main__':
    open_window()
    window = pygetwindow.getActiveWindow()
    
    # # 登录
    if config.autologin:
        login.login(config.username, config.password)
    
    # console.log('登录完成，请切换到你要完成的作业[仅限单词]，按下任意键继续。')
    # console.input('Press Enter to continue...')
    
    # 选择录音设备
    # record_device_index = None
    # if pathlib.Path.joinpath(runtime_dir, 'audio_device.pyobj').exists():
    #     record_device_index, record_device_channels = pickle.load(open(pathlib.Path.joinpath(runtime_dir, 'audio_device.pyobj'), 'rb'))
    #     console.log(f'读取上次的选择：{record_device_index}。[grey50]要重新选择，请删除 runtime/audio_device.pyobj')
    # else:
    #     record_device_index, record_device_channels = listening_part.select_a_audio_device()
    #     pickle.dump((record_device_index, record_device_channels), open(pathlib.Path.joinpath(runtime_dir, 'audio_device.pyobj'), 'wb'))
    
    # # 测试音频录制设备
    # console.log('[red]接下来将开始测试音频录制设备。')
    # if listening_part.test_audio_record(record_device_index, record_device_channels):
    #     console.log('[green]测试通过，可以开始答题。')
    # else:
    #     console.log('[red]测试未通过，请检查音频录制设备是否正常。')
    
    console.log('开始答题')
    
    while True:
        # open_window()
        
        # 听力部分
        is_listening_part = False
        
        try:
            pag.locateCenterOnScreen(locate_images.audio_icon.__str__(), confidence=0.8)
            
            is_listening_part = True
            
            # console.log('[red]出现听力部分，程序退出！')
            # raise ValueError('出现听力部分')
        except pag.ImageNotFoundException:
            pass
        
        if is_listening_part:
            if config.always_A_in_listening_part:
                option = 'A'
            else:
                pass
                # OCR
                # ocr_result = answer.OCR(window)
                
                # 更改 title
        else:
            # OCR
            ocr_result = answer.OCR(window)
            option = adapter(*ocr_result)
            
        answer.answer_it(option, window)
        
        time.sleep(0.5)
        
        # 答错
        wrong = True
        next_question: pag.Point = None
        
        try:
            next_question = pag.locateCenterOnScreen(locate_images.next_question_button.__str__(), confidence=0.8)
        except pag.ImageNotFoundException:
            wrong = False

        if wrong:
            pag.click(next_question.x, next_question.y)

        time.sleep(1.5)
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

import question_type
import question_type.based_question
import question_type.word_to_chinese
import question_type.speaking

from rich import print
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown

from typing import Literal, Union, Dict

console = Console()
runtime_dir = pathlib.Path('./runtime').absolute()

# 支持的题目类型及对应的答题类
quesition_types: Dict[str, question_type.based_question.BasedQuestion] = {
    '单词：中英互译': question_type.word_to_chinese.TranslationQuestion,
    '单词、短语：朗读\n[red b]注意：确保你的麦克风可以收到扬声器的声音': question_type.speaking.WordSpeakingQuestion,
}

# 支持的适配器
adapter_list: Dict[str, adapters.Adapter] = {
    'ChatGLM 适配器': adapters.GLMAdapter(config.zhipuai_apikey)
}

def open_window():
    console.log('正在切换ETS到前台')
    
    # 切换窗口到前台
    taskbar: pag.Point = pag.locateCenterOnScreen(locate_images.taskbar_icon.__str__(), confidence=0.8)
    
    pag.click(taskbar.x, taskbar.y)

    console.log('成功切换ETS到前台')
    
    return pygetwindow.getActiveWindow()

def get_quesition_type() -> int:
    quesition_type_table = Table()
    quesition_type_table.add_column('序号')
    quesition_type_table.add_column('题目类型')
    
    for index, quesition_type in enumerate(quesition_types.keys()):
        quesition_type_table.add_row(str(index), quesition_type)
    
    console.log(quesition_type_table)
    quesition_type_index = int(Prompt.ask('请选择题目类型', choices=[str(index) for index, _ in enumerate(quesition_types.keys())]))
    
    return quesition_type_index

def get_quesition_adapter() -> int:
    quesition_adapter_table = Table()
    quesition_adapter_table.add_column('序号')
    quesition_adapter_table.add_column('适配器')
    
    for index, quesition_adapter in enumerate(adapter_list.keys()):
        quesition_adapter_table.add_row(str(index), quesition_adapter)
    
    console.log(quesition_adapter_table)
    adapter_index = int(Prompt.ask('请选择适配器', choices=[str(index) for index, _ in enumerate(adapter_list.keys())]))
    
    return adapter_index

def answer_question(window: pygetwindow.getActiveWindow(), quesition_type_index: int, adapter_index: int):
    # 判断题目类型
    _question_type: question_type.word_to_chinese.TranslationQuestion = quesition_types[list(quesition_types.keys())[quesition_type_index]]
    adapter = adapter_list[list(adapter_list.keys())[adapter_index]]
    
    # 答题
    _question_type(window, adapter)()

if __name__ == '__main__':
    # # 登录
    if config.autologin:
        login.login(config.username, config.password)
    
    # console.log('登录完成，请切换到你要完成的作业[仅限单词]，按下任意键继续。')
    # console.input('Press Enter to continue...')
    
    # 选择录音设备
    record_device_index = None
    if pathlib.Path.joinpath(runtime_dir, 'audio_device.pyobj').exists():
        record_device_index, record_device_channels = pickle.load(open(pathlib.Path.joinpath(runtime_dir, 'audio_device.pyobj'), 'rb'))
        console.log(f'读取上次的选择：{record_device_index}。[grey50]要重新选择，请删除 runtime/audio_device.pyobj')
    else:
        record_device_index, record_device_channels = listening_part.select_a_audio_device()
        pickle.dump((record_device_index, record_device_channels), open(pathlib.Path.joinpath(runtime_dir, 'audio_device.pyobj'), 'wb'))
    
    # 测试音频录制设备
    console.log('[red]接下来将开始测试音频录制设备。')
    console.log('[red]按下 [green b]Enter[/green b] 键说明测试通过。按下 [red b]Space[/red b] 表示测试失败。')
    if listening_part.test_audio_record(record_device_index, record_device_channels):
        console.log('[green]测试通过，可以开始答题。')
    else:
        console.log('[red]测试未通过，请检查音频录制设备是否正常。')
        exit(0)

    quesition_type_index = get_quesition_type()
    adapter_index = get_quesition_adapter()
    
    # ===== 开始答题 =====
    console.rule('开始答题', characters='=')
    console.log('[red]警告：答题过程中请勿[r]移动鼠标[/r]、[r]按下键盘上的按键[/r]或进行任何可能影响答题的行为！')
    window = open_window()
    while True: 
        answer_question(window, quesition_type_index, adapter_index)
        time.sleep(2)
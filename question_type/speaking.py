import adapters
import config
import pyautogui as pag
import pytesseract
import utils
import locate_images
import time
from pygetwindow._pygetwindow_win import Win32Window
from question_type.based_question import BasedQuestion
from typing import Union

from rich.console import Console

pytesseract.pytesseract.tesseract_cmd = config.tesseract_path
console = Console()

# 单词、短语朗读题
class WordSpeakingQuestion(BasedQuestion):
    def __init__(self, window: Win32Window, _):
        super().__init__(window)
        
        self.title: Union[str, None] = None
        self.az_speech_key = config.az_speech_key
    
    def ocr(self):
        console.log('正在进行光学字符识别。')
        word_position = (
            pag.Point(400 + self.origin[0], 245 + self.origin[1]),
            pag.Point(700 + self.origin[0], 285 + self.origin[1])
        )
        
        screenshot = pag.screenshot()
        word_clip = screenshot.crop(
            (
                word_position[0].x, word_position[0].y,
                word_position[1].x, word_position[1].y
            )
        )
        word = pytesseract.image_to_string(word_clip, lang='chi_sim')
        console.log(f'[grey50]光学字符识别结果：[white]{word}')
        
        self.title = word
    
    def answer(self):
        # 识别字符和按钮位置
        self.ocr()
        start_record_button_position = pag.locateCenterOnScreen(locate_images.speaking_start_record.__str__(), confidence=0.8)
        
        # 播放
        pag.click(start_record_button_position.x, start_record_button_position.y)
        utils.tts(config.az_endpoint, config.az_speech_key, self.title)
        
        # 注：播放和停止按钮都是同一位置
        pag.click(start_record_button_position.x, start_record_button_position.y)
    
    def eval(self) -> bool:
        return True
    
    def next(self) -> None:
        with console.status("[bold green]正在评分", spinner='moon'):
            # 检测是否评分完成
            while True:
                try:
                    pag.locateCenterOnScreen(locate_images.speaking_click_to_record_text.__str__(), confidence=0.9)
                    break
                except:
                    continue
        
        next_button_position = pag.locateCenterOnScreen(locate_images.speaking_next.__str__(), confidence=0.8)
        
        pag.click(next_button_position.x, next_button_position.y)

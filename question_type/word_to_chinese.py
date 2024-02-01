import time
import adapters
import pytesseract
import config
import locate_images
import pyaudio
import utils
import pyautogui as pag
from pygetwindow._pygetwindow_win import Win32Window
from question_type.based_question import BasedQuestion
from concurrent.futures import ThreadPoolExecutor
from typing import Literal, Union, Dict

from rich import print
from rich.console import Console
from rich.table import Table

pytesseract.pytesseract.tesseract_cmd = config.tesseract_path
console = Console()

# 中英互译
class TranslationQuestion(BasedQuestion):
    def __init__(self, window: Win32Window, adapter: adapters.Adapter):
        super().__init__(window)
        
        self.adapter: adapters.Adapter = adapter
        self.title: Union[None, str] = None
        self.options: Dict[Literal['A', 'B', 'C', 'D'], str] = {}
        
        self.next_question_button_position: Union[None, pag.Point] = None
    
    def ocr(self):
        console.log('正在进行光学字符识别。')
    
        origin: pag.Point = pag.Point(self.window.left, self.window.top)
        title_offset_x = 200
        title_offset_y = 40
        
        offset_x = 120
        offset_y = 50
        
        selection = {
            'title': pag.Point(460 + origin.x, 227 + origin.y),
            'A': pag.Point(294 + origin.x, 392 + origin.y),
            'B': pag.Point(626 + origin.x, 392 + origin.y),
            'C': pag.Point(311 + origin.x, 499 + origin.y),
            'D': pag.Point(623 + origin.x, 499 + origin.y)
        }
        
        screenshot = pag.screenshot()
        title_img = screenshot.crop(
            (
                selection['title'].x - title_offset_x,
                selection['title'].y - title_offset_y,
                selection['title'].x + title_offset_x,
                selection['title'].y + title_offset_y,
            )
        )
        
        A_img = screenshot.crop(
            (
                selection['A'].x - offset_x,
                selection['A'].y - offset_y,
                selection['A'].x + offset_x,
                selection['A'].y + offset_y,
            )
        )
        
        B_img = screenshot.crop(
            (
                selection['B'].x - offset_x,
                selection['B'].y - offset_y,
                selection['B'].x + offset_x,
                selection['B'].y + offset_y,
            )
        )

        C_img = screenshot.crop(
            (
                selection['C'].x - offset_x,
                selection['C'].y - offset_y,
                selection['C'].x + offset_x,
                selection['C'].y + offset_y,
            )
        )

        D_img = screenshot.crop(
            (
                selection['D'].x - offset_x,
                selection['D'].y - offset_y,
                selection['D'].x + offset_x,
                selection['D'].y + offset_y,
            )
        )

        pool = ThreadPoolExecutor(max_workers=8)

        title, A, B, C, D = (
            # pytesseract.image_to_string(title_img, 'chi_sim'),
            # pytesseract.image_to_string(A_img, 'chi_sim'),
            # pytesseract.image_to_string(B_img, 'chi_sim'),
            # pytesseract.image_to_string(C_img, 'chi_sim'),
            # pytesseract.image_to_string(D_img, 'chi_sim')
            pool.submit(pytesseract.image_to_string, title_img, 'chi_sim').result(),
            pool.submit(pytesseract.image_to_string, A_img, 'chi_sim').result(),
            pool.submit(pytesseract.image_to_string, B_img, 'chi_sim').result(),
            pool.submit(pytesseract.image_to_string, C_img, 'chi_sim').result(),
            pool.submit(pytesseract.image_to_string, D_img, 'chi_sim').result(),
        )
        
        table = Table(show_header=True, header_style='bold')
        table.add_column("标题")
        table.add_column("A")
        table.add_column("B")
        table.add_column("C")
        table.add_column("D")
        
        table.add_row(title, A, B, C, D)
        
        console.log('光学字符识别完成。')
        console.log(table)
        
        self.title = title
        self.options['A'] = A
        self.options['B'] = B
        self.options['C'] = C
        self.options['D'] = D

    def is_listening_part(self) -> bool:
        try:
            pag.locateCenterOnScreen(locate_images.transition_audio_icon.__str__(), confidence=0.8)
            return True
        except pag.ImageNotFoundException:
            return False
    
    def listen(self) -> str:
        audio_play_button = pag.locateCenterOnScreen(locate_images.transition_audio_icon.__str__(), confidence=0.8)
        # 播放声音
        pag.click(audio_play_button.x, audio_play_button.y)

        return utils.audio2text(2).lower()

    def answer(self) -> None:
        self.ocr()
        
        if self.is_listening_part():
            console.log("在 without_whisper 分支中不支持听力部分")
            raise RuntimeError("在 without_whisper 分支中不支持听力部分")
        
        option = self.adapter(self.title, *self.options.values())
        
        origin: pag.Point = pag.Point(self.window.left, self.window.top)
        selection = {
            'A': pag.Point(294 + origin.x, 392 + origin.y),
            'B': pag.Point(626 + origin.x, 392 + origin.y),
            'C': pag.Point(311 + origin.x, 499 + origin.y),
            'D': pag.Point(623 + origin.x, 499 + origin.y)
        }
        
        pag.click(selection[option].x, selection[option].y)
    
    def wrong(self) -> None:
        pag.click(self.next_question_button_position.x, self.next_question_button_position.y)
    
    def eval(self) -> bool:
        time.sleep(0.5)
        
        try:
            self.next_question_button_position = pag.locateCenterOnScreen(locate_images.transition_next_question_button.__str__(), confidence=0.8)
            return False
        except pag.ImageNotFoundException:
            return True
    
    def finish(self) -> bool:
        try:
            pag.locateCenterOnScreen(locate_images.transition_finish.__str__(), confidence=0.8)
            return True
        except pag.ImageNotFoundException:
            return False
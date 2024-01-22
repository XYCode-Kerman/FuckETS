import pyautogui as pag
import zhipuai
import pytesseract
import pygetwindow
import config
from typing import Literal
from objprint import op

from rich import print
from rich.console import Console
from rich.table import Column, Table

console = Console()

pytesseract.pytesseract.tesseract_cmd = config.tesseract_path

def OCR(window: pygetwindow.Win32Window):
    console.log('正在进行光学字符识别。')
    
    origin: pag.Point = pag.Point(window.left, window.top)
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

    title, A, B, C, D = (
        pytesseract.image_to_string(title_img, 'chi_sim'),
        pytesseract.image_to_string(A_img, 'chi_sim'),
        pytesseract.image_to_string(B_img, 'chi_sim'),
        pytesseract.image_to_string(C_img, 'chi_sim'),
        pytesseract.image_to_string(D_img, 'chi_sim'),
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
    
    return title, A, B, C, D

def answer_it(select: Literal['A', 'B', 'C', 'D'], window: pygetwindow.Win32Window):
    origin: pag.Point = pag.Point(window.left, window.top)
    
    selection = {
        'A': pag.Point(294 + origin.x, 392 + origin.y),
        'B': pag.Point(626 + origin.x, 392 + origin.y),
        'C': pag.Point(311 + origin.x, 499 + origin.y),
        'D': pag.Point(623 + origin.x, 499 + origin.y)
    }
    
    pag.click(selection[select].x, selection[select].y)
import pygetwindow
from rich.console import Console
from abc import ABC

console = Console()

class BasedQuestion(ABC):
    def __init__(self, window: pygetwindow.Win32Window):
        self.window: pygetwindow.Win32Window = window
        self.origin = (self.window.left, self.window.top)
    
    def eval(self) -> bool:
        """答题效果评估"""
        pass
    
    def wrong(self) -> None:
        """答错后的处理"""
        pass
    
    def answer(self) -> None:
        """答题"""
        pass
    
    def next(self) -> None:
        """下一题"""
        pass
    
    def finish(self) -> bool:
        pass

    def __call__(self, *args, **kwds) -> None:
        # 是否做完
        if self.finish():
            console.log('[green b] 作业内容完成，程序将自动退出。')
            exit(0)
        
        # 答题
        self.answer()
        
        # 效果评估
        is_wrong = not self.eval()
        
        if is_wrong:
            console.log('[white on red]答题错误，进入错误处理流程')
            self.wrong()

        self.next()
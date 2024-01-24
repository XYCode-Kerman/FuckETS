# 答题适配器
import re
import zhipuai
import pickle
from zhipuai.model_api import ChatGLM6bParams

from rich import print
from rich.console import Console
from typing import Any, Literal

console = Console()

class Adapter(object):
    def __init__(self) -> None:
        pass
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        console.log('[red b]不要使用Adapter基类！')

class GLMAdapter(Adapter):
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.model = 'glm-3-turbo'
        try:
            self.total_usage = pickle.load(open('./runtime/usage.pyobj', 'rb'))
        except FileNotFoundError:
            self.total_usage = 0
        
        zhipuai.api_key = self.api_key
    
    def __call__(self, title: str, A: str, B: str, C: str, D: str) -> Literal['A', 'B', 'C', 'D']:
        console.log(f'正在询问LLM：[green]{self.model}')
        
        prompt = f"""
        题目：{title}
        A：{A}
        B：{B}
        C：{C}
        D：{D}
        
        答案是：
        """
        
        params = ChatGLM6bParams(
            prompt=[
                {"role": "user", "content": "你擅长英语，请根据用户给出的题目在ABCD四个选项间选择出你认为最正确的答案。请不要在回答中增加任何除ABCD四个选项外的字符。注意：给你的题目来源于OCR的结果，可能存在错误。"},
                # {"role": "assistant", "content": "好的。"},
                {"role": "user", "content": prompt}
            ],
            top_p=0.7,
            temperature=0.9
        )
        
        params.model = self.model
        
        msg = zhipuai.model_api.invoke(**params.asdict())
        usage = msg['data']['usage']['total_tokens']
        msg = msg['data']['choices'][0]['content']
        
        self.total_usage += usage
        
        pickle.dump(self.total_usage, open('./runtime/usage.pyobj', 'wb'))
        console.log(f'LLM回答：[green]{msg}[/green]。本次调用使用了 [green]{usage}[/green] 个 token。总计使用了 [cyan]{self.total_usage}[/cyan] 个 token。')
        console.log(f'预计本程序将使用：{self.total_usage / 1000 * 0.005:.6f}元。')
        console.log('[grey50]删除 runtime/usage.pyobj 即可清零相关数据。')
        
        # 过滤回答
        try:
            option = re.findall('[a-dA-D]', msg.upper())[0]
        except IndexError:
            console.log('[red]LLM回答有误！使用默认选项 [green]A')

            return 'A'
        
        return option
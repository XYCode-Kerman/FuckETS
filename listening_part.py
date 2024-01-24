import pyaudio
import keyboard
import numpy as np
import wave
import audioop
import rich
from rich import print
from rich.prompt import Prompt, Confirm
from rich.table import Table, Column
from rich.console import Console
from rich.progress import Progress

console = Console()

audio = pyaudio.PyAudio()

def select_a_audio_device() -> int:
    """让用户选择一个输出音频的设备供录音。"""

    devices = []
    
    for i in range(audio.get_device_count()):
        devices.append(audio.get_device_info_by_index(i))
    
    # 过滤出输出设备
    devices = [
        device for device in devices if device['maxInputChannels'] > 0
    ]
    
    devices_table = Table(title="Available Audio Devices")
    devices_table.add_column("索引", style="cyan", no_wrap=True)
    devices_table.add_column("名称", style="green")
    devices_table.add_column("声道", style="magenta")
    
    for index, device in enumerate(devices):
        devices_table.add_row(
            str(device["index"]),
            device["name"],
            str(device["maxInputChannels"])
        )
    
    console.log("请选择一个输出音频的设备供录音。")
    print(devices_table)
    
    device_index = Prompt.ask("请输入设备索引", default="0", choices=[str(i["index"]) for i in devices])
    device_index = int(device_index)
    device_channels = list(filter(lambda x: x["index"] == device_index, devices))[0]['maxInputChannels']
    
    return device_index, device_channels

def test_audio_record(device_index: int, device_channels: int) -> bool:
    """测试录制声音。将获取到的声音大小以进度条的方式显示。"""
    stream = audio.open(format=pyaudio.paInt16, channels=device_channels, rate=44100, input=True, frames_per_buffer=64, input_device_index=device_index)
    stream.start_stream()
    
    # 获取音量大小
    with Progress() as progress:
        task = progress.add_task("测试录音...", total=100)
        
        while True:
            data = stream.read(64, exception_on_overflow=False)
            data = np.fromstring(data, dtype=np.int16)

            volume = np.median(np.mean(data)) * 10
            
            progress.update(task, completed=volume)
            
            # 按下Enter键表示通过，Space键表示失败
            if keyboard.is_pressed('enter'):
                stream.stop_stream()
                audio.terminate()
                return True
            elif keyboard.is_pressed('space'):
                stream.stop_stream()
                audio.terminate()
                return False
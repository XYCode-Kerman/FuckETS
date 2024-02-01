import pyaudio
import os
import wave
import uuid
import pickle
import pathlib
import requests
import azure.cognitiveservices.speech as speechsdk

from rich.console import Console

console = Console()

def record(time: int) -> pathlib.Path:
    audio = pyaudio.PyAudio()
    device_index, channel = pickle.load(open('./runtime/audio_device.pyobj', 'rb'))
    
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=channel,
        rate=44100,
        input=True,
        input_device_index=device_index,
        frames_per_buffer=1024
    )
    frames = []
    output_file = pathlib.Path.joinpath(pathlib.Path('./runtime'), pathlib.Path(f"{uuid.uuid4()}.wav"))

    console.log('[green]开始录音。')
    stream.start_stream()
    for i in range(0, int(44100 * time / 1024)):
        data = stream.read(1024)    
        frames.append(data)
    
    stream.stop_stream()
    stream.close()
    console.log('停止录音')
    
    wavefile = wave.open(output_file.__str__(), 'wb')
    wavefile.setnchannels(channel)
    wavefile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wavefile.setframerate(44100)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()
    audio.terminate()
    
    return output_file

def tts(az_speech_endpoint: str, az_speech_key: str, text: str, speaker: str = 'en-US-RyanMultilingualNeural') -> None:
    console.log('语音合成中')
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=az_speech_key, region=az_speech_endpoint.replace('https://', '').split('.')[0])
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_config.speech_synthesis_voice_name = speaker
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    console.log('语音合成完毕，即将播放。')
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
    
    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        console.log("Speech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        console.log("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                console.log("Error details: {}".format(cancellation_details.error_details))
            console.log("Did you set the speech resource key and region values?")
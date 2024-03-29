import dotenv
import os
dotenv.load_dotenv()

# Login
az_speech_key = os.environ.get('AZURE_SPEECH_SUB_KEY')
az_endpoint = os.environ.get('AZURE_ENDPOINT')
zhipuai_apikey = os.environ.get('ZHIPUAI_APIKEY')
username = os.environ.get('username')
password = os.environ.get('password')
autologin = False

# OCR
tesseract_path = r'D:\Program Files\Tesseract-OCR\tesseract.exe'

# Listening Part
always_A_in_listening_part = True
# FuckETS | 去你🐎的E听说作业

## 这是什么 | What's this?

FuckETS是一个基于[PyAutoGUI](https://github.com/asweigart/pyautogui)的自动完成E听说作业的程序。

## 为什么开发本软件 | Why start the project?

由于作者的班级近期换了一个新的英语老师，天天布置一大堆E听说作业，所以开发了本软件。

## 如何使用 | How to use?

首先，使用`git clone https://github.com/XYCode-Kerman/FuckETS.git`命令将本仓库克隆到本地。

然后，确保你安装了`python3.9`和`poetry`，使用`poetry install`安装依赖。

为了可以正常使用OCR（光学字符识别），你需要安装[Tesseract-OCR](https://github.com/tesseract-ocr/tesseract)及其中文预训练模型，并在`config.py`中进行如下配置

```python
# config.py
tesseract_path = r'此处填入你的tesseract.exe的路径'
```

并重命名`example.env`为`.env`，在其中填入你的E听说用户名和密码。

> `.env`文件会被 git 忽略。
>
> 您可以通过注释`main.py`中的`login.login(config.username, config.password)`语句来关闭自动登录。

最后，使用`poetry run python main.py`命令运行`main.py`即可。

## 配置文件 | config.py and .env

`.env`是用于存储机密信息的，任何情况下都不要将你的`.env`上传到公开环境！其中的配置项及其作用如下：

|    项    |       作用        |   示例值    |
| :------: | :---------------: | :---------: |
| USERNAME | 登录E听说的用户名 | 11451419198 |
| PASSWORD |  登录E听说的密码  |   1919810   |

`config.py`是用于存储一般配置信息的，其中的配置项及其作用如下：

|             项             |                         作用                          |                    示例值                    |
| :------------------------: | :---------------------------------------------------: | :------------------------------------------: |
|          username          |              自动从环境变量中读取用户名               |               DO NOT UPDATE IT               |
|          password          |               自动从环境变量中读取密码                |               DO NOT UPDATE IT               |
|       tesseract_path       |        用于提供OCR功能的`tesseract.exe`的位置         | D:\Program Files\Tesseract-OCR\tesseract.exe |
| always_A_in_listening_part | 在听力部分始终选择A<br />注意：该选项将会在近期被移除 |                     True                     |

## 法律声明 | Legal Disclaimer

本程序使用的是由微软公司（Microsoft）提供的模拟用户输入的**公开的**应用程序编程接口（Application Program Interface, API），**未采用任何方式修改**E听说程序的指令序列、内存环境、配置文件，不违反**《中华人民共和国计算机软件保护条例》第二十三条第五款**及**《中华人民共和国著作权法》**等法律法规，亦不违反美国联邦**《联邦计算机系统保护法》**、**《计算机安全法》**等有关法律法规，不侵犯E听说程序著作权人、微软公司、PyAutoGUI著作权人的各项权利。

根据本程序所使用的**GNU 通用公共许可证**及**MIT 许可证**中的条款，本软件所有者、贡献者、著作权人不承担用户使用本程序造成的任何法律后果。

本声明及许可证的唯一有效版本是托管在Github平台上的master分支中的最新提交中的README.md和LICENSE文件，如该程序因不可抗力等原因无法在Github等平台上托管，则以本程序所有者**XYCode Kerman**的计算机上存储的版本为准。

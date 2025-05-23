something about the project: [Learn2Control](https://ustc3dv.github.io/Learn2Control/)

## 项目功能

该仓库提供了一个使用 ElevenLabs API 进行文本转语音 (TTS) 的工具套件。

核心功能包括：

1.  **文本处理与 TTS 生成**:
    *   提供一个 Python 脚本 (`process_text.py`)，可以将输入的文本文件按句子分割。
    *   为每个句子调用 ElevenLabs API 生成对应的语音文件 (`.wav`)。
    *   将原始文本句子和生成的音频文件保存在指定的输出目录中，并以数字序列命名（例如 `001.txt`, `001.wav`）。

2.  **网页端音频播放与管理**:
    *   包含一个简单的网页应用 (`index.html`, `style.css`, `script.js`)。
    *   该网页能够动态加载并显示 `audio/` 目录下由 Python 脚本生成的文本内容和对应的音频播放器。
    *   用户可以在网页上播放这些音频。
    *   提供 "打包下载全部" 功能，允许用户将 `audio/` 目录下的所有文本和音频文件打包成一个 `.zip` 文件下载。

**简而言之，用户可以使用此仓库将文本批量转换为语音，并通过一个简单的网页界面来收听和管理这些生成的音频文件。**



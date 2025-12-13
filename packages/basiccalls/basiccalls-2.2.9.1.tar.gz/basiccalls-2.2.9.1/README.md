# BasicCalls [![PyPI](https://img.shields.io/pypi/v/basiccalls.svg?logo=python&logoColor=%23959DA5&label=pypi&labelColor=%23282f37)](https://pypi.org/project/basiccalls/)

## 🚀 Enhanced Fork of py-tgcalls

**BasicCalls** is an enhanced fork of the original [py-tgcalls](https://github.com/pytgcalls/pytgcalls) library with additional features and improvements:

### ✨ Key Enhancements
- **Kurigram Compatibility**: Full support for Kurigram (Pyrogram fork) with UpdateGroupCall compatibility patches
- **Improved Stability**: Enhanced error handling and connection management  
- **Extended Features**: Additional functionality for modern Telegram voice/video calls
- **Better Integration**: Optimized for BasicMusic and similar projects

### 🔧 What's New
- UpdateGroupCall peer/chat_id fallback system for Kurigram compatibility
- Enhanced MTProto client detection and initialization
- Improved MediaStream handling with better error management
- Comprehensive test system for validation

<p align="center">
    <b>A simple and elegant client that allows you to make group voice calls quickly and easily.</b>
    <br>
    <a href="https://github.com/y4kupkaya/basiccalls/tree/main/example">
        Examples
    </a>
    •
    <a href="https://github.com/y4kupkaya/basiccalls">
        Repository
    </a>
    •
    <a href="https://yakupkaya.me">
        Developer
    </a>
    •
    <a href="https://pypi.org/project/basiccalls/">
        PyPI
    </a>
</p>

This project allows making Telegram calls using MTProto and WebRTC, based on the power of [NTgCalls] library and [@evgeny-nadymov], with enhancements by Yakup Kaya.

#### Example Usage
```python
from pytgcalls import PyTgCalls
from pytgcalls import idle
...
chat_id = -1001185324811
app = PyTgCalls(client)
app.start()
app.play(
    chat_id,
    'http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4',
)
idle()
```

#### Kurigram Usage Example
```python
# Enhanced compatibility with Kurigram
from kurigram import Client
from pytgcalls import PyTgCalls

app = Client("my_app", api_id=API_ID, api_hash=API_HASH)
calls = PyTgCalls(app)

# Automatic UpdateGroupCall compatibility handling
@calls.on_update()
async def on_update(client, update):
    # Works seamlessly with both peer and chat_id formats
    pass
```

## Features
- Prebuilt wheels for macOS, Linux and Windows.
- Supporting all type of MTProto libraries: Pyrogram, Telethon, Hydrogram and **Kurigram**.
- **Enhanced Kurigram compatibility** with UpdateGroupCall patches.
- Work with voice chats in channels and chats.
- Join as channels or chats.
- Mute/unmute, pause/resume, stop/play, volume control and more...
- **Improved error handling** and connection stability.
- **Comprehensive testing system** for validation.

## Installation

```bash
pip install basiccalls
```

## Original Credits

This project is a fork of [py-tgcalls](https://github.com/pytgcalls/pytgcalls) by Laky-64.
Enhanced and maintained by [Yakup Kaya](https://yakupkaya.me) for improved compatibility and features.

## Contact & Support

- **Developer**: [Yakup Kaya](https://yakupkaya.me)
- **Email**: [y4kupkaya@gmail.com](mailto:y4kupkaya@gmail.com)
- **GitHub**: [@y4kupkaya](https://github.com/y4kupkaya)
- **Telegram**: [@yakupkaya](https://t.me/yakupkaya)
- **LinkedIn**: [yakupkaya](https://www.linkedin.com/in/yakupkaya/)
- **Twitter**: [@y4kupkaya](https://x.com/y4kupkaya)

## Requirements
- Python 3.9 or higher.
- An MTProto Client
- A [Telegram API key](https://docs.pyrogram.org/intro/setup#api-keys).

## How to install?
Here's how to install the PyTgCalls lib, the commands are given below:

``` bash
# With Git
pip install git+https://github.com/pytgcalls/pytgcalls -U

# With PyPi (Recommended)
pip install py-tgcalls -U
```

## Key Contributors
* <b><a href="https://github.com/Laky-64">@Laky-64</a> (DevOps Engineer, Software Architect):</b>
    * Played a crucial role in developing PyTgCalls being an ex developer of pyservercall and of tgcallsjs.
    * Automation with GitHub Actions
* <b><a href="https://github.com/kuogi">@kuogi</a> (Senior UI/UX designer, Documenter):</b>
    * As a Senior UI/UX Designer, Kuogi has significantly improved the user interface of our documentation,
      making it more visually appealing and user-friendly.
    * Played a key role in writing and structuring our documentation, ensuring that it is clear,
      informative, and accessible to all users.
* <b><a href="https://github.com/vrumger">@vrumger</a> (Senior Node.js Developer, Software Architect):</b>
    * Has made important fixes and enhancements to the WebRTC component of the library,
      improving its stability and performance.
    * Main developer of TgCallsJS
* <b><a href="https://github.com/alemidev">@alemidev</a> (Senior Python Developer):</b>
    * Has made important fixes and enhancements to the async part of the library

## Junior Developers
* <b><a href="https://github.com/TuriOG">@TuriOG</a> (Junior Python Developer):</b>
    * Currently working on integrating NTgCalls into <a href="//github.com/pytgcalls/pytgcalls">PyTgCalls</a>, an important step
      in expanding the functionality and usability of the library.

## Special Thanks
* <b><a href="https://github.com/evgeny-nadymov">@evgeny-nadymov</a>:</b>
  A heartfelt thank you to Evgeny Nadymov for graciously allowing us to use their code from telegram-react.
  His contribution has been pivotal to the success of this project.

[NTgCalls]: https://github.com/pytgcalls/ntgcalls
[@evgeny-nadymov]: https://github.com/evgeny-nadymov/

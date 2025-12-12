# 🌐 Pixelith – A Lightweight Multi-Tool Utility Library for Python

Pixelith is a growing Python utility library that provides clean, simple and powerful tools for everyday development needs.  
Currently includes an advanced translation utility powered by Google's unofficial API, and will expand with more tools.

---

## ✨ Features

- 🚀 Modular multi-tool design  
- ⚡ Fast translator engine  
- 🧠 Automatic language detection  
- 🔧 Simple API  
- 🔌 Easily extendable  

---

## 📦 Installation

```bash
pip install pixelith
```

---

## 🚀 Quick Start

### Basic Translation

```python
import pixelith

result = pixelith.translate("tr", "en", "selam dünya")
print(result)
```

---

## 🧠 Advanced Usage (Translator Class)

```python
from pixelith import Translator

t = Translator()

translated, detected = t.translate("auto", "en", "Merhaba, nasılsın?")
print("Translated:", translated)
print("Detected:", detected)
```

---

## © License

MIT License — free to use, modify, and distribute.
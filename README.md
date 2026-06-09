```markdown
# Photo Enhancer Telegram Bot

A professional Telegram bot that enhances photo quality and restores faces using GFPGAN AI.

[![Telegram](https://img.shields.io/badge/Join-Telegram%20Channel-blue)](https://t.me/Hezar_code)
[![GitHub](https://img.shields.io/badge/GitHub-Repo-black)](https://github.com/mmd-aminmoradi/photo-enhancer-telegram-bot)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## About

This Telegram bot uses the powerful **GFPGAN** model (developed by TencentARC) to enhance low-quality photos and restore faces.

If you have an old, blurry, or low-resolution photo, this bot will convert it into a high-quality image.

---

## Features

| Feature | Description |
|---------|-------------|
| Upscale | Resize images 2x, 3x, or 4x |
| Face Enhancement | 6 levels (Low to Max) |
| Sharpening | Soft, Normal, Strong, or Off |
| Interactive Buttons | Easy settings adjustment |
| Document Support | Send as file to preserve quality |

---

## Technologies

- Python 3.10+
- Aiogram 3.x (Telegram Bot Framework)
- GFPGAN (Face Enhancement AI)
- PyTorch & OpenCV
- Pillow & NumPy

---

## Repository Structure

```

photo-enhancer-telegram-bot/
├── bot.py                 # Main bot code
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── .gitignore             # Git ignore rules
└── LICENSE                # MIT License

```

---

## Installation on Local Computer

### Requirements

- Python 3.10 or higher
- 8GB+ RAM (16GB recommended)
- 4GB free disk space
- GPU with CUDA (optional but recommended)

### Step-by-Step

**1. Clone the repository**

```bash
git clone https://github.com/mmd-aminmoradi/photo-enhancer-telegram-bot.git
cd photo-enhancer-telegram-bot
```

2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Download the GFPGAN AI model

```bash
wget https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth
```

5. Add your bot token

Open bot.py and replace YOUR_TOKEN_HERE with your real token from BotFather.

6. Run the bot

```bash
python bot.py
```

7. Test on Telegram

· Send /start to your bot
· Send a photo as Document (File)
· Adjust settings and enjoy

---

Installation on Google Colab (Free GPU)

Best for users without a powerful computer.

Step-by-Step

1. Open Google Colab

Go to colab.research.google.com and sign in with your Google account.

2. Create a new notebook

Click New Notebook.

3. Cell 1 - Install dependencies

```python
!pip install aiogram torch torchvision opencv-python-headless pillow numpy gfpgan nest-asyncio
!wget https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth
```

4. Cell 2 - Paste your bot code

Copy the entire content of bot.py and paste it into a new cell. Make sure to add your bot token.

5. Cell 3 - Run the bot

```python
import asyncio
import nest_asyncio
nest_asyncio.apply()

async def run():
    from bot import main
    await main()

asyncio.run(run())
```

Note: Colab stops after 1 hour of inactivity. Use UptimeRobot to keep it alive.

---

Version History

Version Date Changes
v1.0.0 2026-06-09 Initial release with GFPGAN integration
v1.1.0 Planned Add more AI models
v1.2.0 Planned Batch processing

---

How to Use the Bot on Telegram

Step 1: Start the bot

Send /start to your bot.

Step 2: Send a photo

⚠️ IMPORTANT: Always send as Document (File) for best quality.

How to send as document:

· Tap the 📎 (attachment) button
· Select File or Document
· Choose your photo

Step 3: Adjust settings

Use the inline buttons:

· Upscale : Change size (2x, 3x, 4x)
· Face : Change enhancement level
· Sharpen : Change sharpening strength

Step 4: Process

Click Start Processing and wait about 10 seconds.

Step 5: Get result

The enhanced photo will be sent back with settings information.

---

Troubleshooting

Problem Solution
Module not found Run pip install -r requirements.txt
Out of memory Use Google Colab instead of local PC
Bot doesn't respond Check your token is correct
Low quality output Send photo as Document, not as Photo
Colab stops Use UptimeRobot to ping your Colab URL
Model download fails Download manually from GFPGAN GitHub

---

FAQ

Q: Why send as Document?
A: Telegram compresses photos sent as "Photo". Sending as "Document" preserves original quality.

Q: How long does processing take?
A: About 10 seconds per image on GPU, 30-60 seconds on CPU.

Q: Is there a daily limit?
A: No, if you host it yourself. On Colab, you have limits based on Colab's free tier.

Q: Can I use this commercially?
A: Yes, under the MIT License.

---

Credits

· GFPGAN by TencentARC - GitHub
· Aiogram - Telegram Bot Framework
· PyTorch - Deep learning framework

---

Contact

· Telegram Channel: @Hezar_code
· Author: Amin (Mohammad amin moradi)
· GitHub: mmd-aminmoradi

---

License

This project is licensed under the MIT License - see the LICENSE file for details.

You are free to:

· Use this code commercially
· Modify and distribute it
· Use it in your own projects

---

Star This Project

If you found this project helpful, please give it a star ⭐ on GitHub and join our Telegram channel!

https://img.shields.io/badge/Join-Telegram%20Channel-blue

```
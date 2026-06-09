# Photo Enhancer Telegram Bot

A professional Telegram bot that enhances photo quality and restores faces using GFPGAN AI

Telegram Channel: https://t.me/Hezar_code

---

Features

- Upscale images 2x, 3x, or 4x
- Face enhancement with 6 levels (Low to Max)
- Sharpening options (Soft, Normal, Strong, Off)
- Interactive button interface
- High quality by sending as Document

---

Technologies

- Python 3.10+
- Aiogram (Telegram Bot Framework)
- GFPGAN (Face Enhancement AI)
- PyTorch & OpenCV
- Pillow & NumPy

---

Installation on Local Computer

Requirements:
- Python 3.10 or higher
- 8GB+ RAM
- 4GB free disk space

Steps:

1. Clone the repository

git clone https://github.com/mmd-aminmoradi/photo-enhancer-telegram-bot.git
cd photo-enhancer-telegram-bot

2. Install dependencies

pip install -r requirements.txt

3. Download the AI model

wget https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth

4. Add your bot token

Open bot.py and replace YOUR_TOKEN_HERE with your real token from BotFather.

5. Run the bot

python bot.py

---

Installation on Google Colab (Free GPU)

Best for users without a powerful computer.

1. Go to colab.research.google.com
2. Create a new notebook
3. In the first cell, run:

!pip install aiogram torch torchvision opencv-python-headless pillow numpy gfpgan nest-asyncio
!wget https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth

4. In the second cell, paste your entire bot.py code (add your token)
5. In the third cell, run:

import asyncio
import nest_asyncio
nest_asyncio.apply()

async def run():
    from bot import main
    await main()

asyncio.run(run())

Note: Colab stops after 1 hour of inactivity.

---

How to Use the Bot

1. Send /start to your bot on Telegram
2. Send a photo as Document (File) (not as a compressed photo)
3. Adjust settings using the buttons
4. Click Start Processing
5. Get your enhanced photo

---

Troubleshooting

Problem: Module not found
Solution: Run pip install -r requirements.txt

Problem: Out of memory
Solution: Use Google Colab instead

Problem: Bot doesn't respond
Solution: Check your token is correct

Problem: Low quality output
Solution: Send photo as Document, not as Photo

---

Author: Amin

Telegram Channel: https://t.me/Hezar_code

License: MIT
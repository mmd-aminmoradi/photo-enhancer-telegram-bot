# -*- coding: utf-8 -*-
import logging
import asyncio
import cv2
import numpy as np
from PIL import Image
import io
import torch
import sys
import types
import time
import hashlib
import os

# ========== fix torchvision ==========
try:
    from torchvision.transforms.functional_tensor import rgb_to_grayscale
except ImportError:
    from torchvision.transforms.functional import rgb_to_grayscale
    functional_tensor = types.ModuleType("torchvision.transforms.functional_tensor")
    functional_tensor.rgb_to_grayscale = rgb_to_grayscale
    sys.modules["torchvision.transforms.functional_tensor"] = functional_tensor

# ========== imports ==========
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.default import DefaultBotProperties
from gfpgan import GFPGANer
import nest_asyncio

TOKEN = "توکن_ربات_خود_را_اینجا_وارد_کنید"

class ProEnhancer:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Device: {self.device}")
        self.load_model()
        
    def load_model(self):
        self.face_enhancer = GFPGANer(
            model_path='/content/GFPGANv1.4.pth',
            upscale=4,
            arch='clean',
            channel_multiplier=2,
            bg_upsampler=None,
            device=self.device
        )
        print("GFPGAN model loaded")
    
    async def enhance(self, img_pil, upscale=3, face_weight=0.8):
        img_np = np.array(img_pil)
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        
        _, _, output = self.face_enhancer.enhance(
            img_bgr, 
            has_aligned=False, 
            only_center_face=False,
            paste_back=True, 
            weight=face_weight
        )
        
        if upscale != 4:
            h, w = output.shape[:2]
            new_h, new_w = int(h * upscale/4), int(w * upscale/4)
            output = cv2.resize(output, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
        
        kernel = np.array([[-0.5,-0.5,-0.5], [-0.5,5,-0.5], [-0.5,-0.5,-0.5]]) / 1.5
        output = cv2.filter2D(output, -1, kernel)
        
        output_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        return Image.fromarray(output_rgb)

def get_settings_keyboard(upscale, face_weight, sharpen):
    upscale_names = {2: '2x 🟢', 3: '3x 🔵', 4: '4x 🔴'}
    face_weight_names = {
        0.5: 'Low 🟢', 
        0.6: 'Med-Low 🟡',
        0.7: 'Medium 🟡', 
        0.8: 'High 🟠',
        0.9: 'Very High 🔴', 
        1.0: 'Max 💥'
    }
    sharpen_names = {
        'soft': 'Soft ✨', 
        'normal': 'Normal ⚡', 
        'strong': 'Strong 💪',
        'off': 'Off 🔘'
    }
    
    upscale_text = upscale_names.get(upscale, f"{upscale}x")
    face_text = face_weight_names.get(face_weight, f"{int(face_weight*100)}%")
    sharpen_text = sharpen_names.get(sharpen, sharpen)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"📏 {upscale_text}", callback_data="menu_upscale"),
        ],
        [
            InlineKeyboardButton(text=f"😊 {face_text}", callback_data="menu_weight"),
        ],
        [
            InlineKeyboardButton(text=f"🔪 {sharpen_text}", callback_data="menu_sharpen"),
        ],
        [
            InlineKeyboardButton(text="✅ Start Processing", callback_data="process"),
            InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")
        ]
    ])
    return keyboard

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()
enhancer = None
user_data = {}

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🎯 **Photo Enhancer Bot**\n\n"
        "✨ Features:\n"
        "• Upscale 2x, 3x, 4x\n"
        "• Face enhancement with 6 levels\n"
        "• Fast & stable\n\n"
        "📎 **Send photo as Document**\n\n"
        "🚀 Ready! Send a photo..."
    )

@dp.message(F.document)
async def process_document(message: types.Message):
    doc = message.document
    if not doc.mime_type or not doc.mime_type.startswith('image/'):
        await message.answer("❌ Please send an image file.")
        return
    
    user_data[message.from_user.id] = {
        'file_id': doc.file_id,
        'upscale': 3,
        'face_weight': 0.8,
        'sharpen': 'normal',
        'file_bytes': None
    }
    
    msg = await message.answer("📥 Downloading...")
    try:
        file = await bot.get_file(doc.file_id)
        file_bytes = await bot.download_file(file.file_path)
        user_data[message.from_user.id]['file_bytes'] = file_bytes.read()
        await msg.delete()
        
        settings = user_data[message.from_user.id]
        await message.answer(
            "⚙️ **Settings:**\n\n"
            f"📏 Upscale: {settings['upscale']}x\n"
            f"😊 Face enhancement: {int(settings['face_weight']*100)}%\n"
            f"🔪 Sharpen: {settings['sharpen']}\n\n"
            "👇 Adjust and click Start",
            reply_markup=get_settings_keyboard(
                settings['upscale'], 
                settings['face_weight'], 
                settings['sharpen']
            )
        )
    except Exception as e:
        await msg.edit_text(f"⚠️ Error: {str(e)[:100]}")
        await msg.delete()

@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    
    if user_id not in user_data:
        await callback.answer("❌ Send a photo first", show_alert=True)
        return
    
    data = callback.data
    settings = user_data[user_id]
    
    if data == "menu_upscale":
        current = settings['upscale']
        if current == 2:
            settings['upscale'] = 3
        elif current == 3:
            settings['upscale'] = 4
        else:
            settings['upscale'] = 2
        await callback.answer(f"Upscale: {settings['upscale']}x")
        
    elif data == "menu_weight":
        current = settings['face_weight']
        weights = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        idx = weights.index(current) if current in weights else 3
        next_idx = (idx + 1) % len(weights)
        settings['face_weight'] = weights[next_idx]
        
        names = {0.5:'Low', 0.6:'Med-Low', 0.7:'Medium', 0.8:'High', 0.9:'Very High', 1.0:'Max'}
        await callback.answer(f"Face: {names[settings['face_weight']]}")
        
    elif data == "menu_sharpen":
        current = settings['sharpen']
        sharpens = ['off', 'soft', 'normal', 'strong']
        idx = sharpens.index(current) if current in sharpens else 2
        next_idx = (idx + 1) % len(sharpens)
        settings['sharpen'] = sharpens[next_idx]
        
        names = {'off':'Off', 'soft':'Soft', 'normal':'Normal', 'strong':'Strong'}
        await callback.answer(f"Sharpen: {names[settings['sharpen']]}")
        
    elif data == "process":
        await callback.message.edit_text("🎨 **Processing...** (about 10 seconds)")
        
        try:
            global enhancer
            if enhancer is None:
                await callback.message.edit_text("📦 Loading AI model...")
                enhancer = ProEnhancer()
            
            img = Image.open(io.BytesIO(settings['file_bytes']))
            
            await callback.message.edit_text("🔧 Applying enhancements...")
            result = await enhancer.enhance(
                img,
                upscale=settings['upscale'],
                face_weight=settings['face_weight']
            )
            
            output = io.BytesIO()
            result.save(output, format='JPEG', quality=95)
            output.seek(0)
            
            weight_names = {0.5:'Low', 0.6:'Med-Low', 0.7:'Medium', 0.8:'High', 0.9:'Very High', 1.0:'Max'}
            
            await bot.send_document(
                chat_id=user_id,
                document=BufferedInputFile(output.getvalue(), filename="enhanced.jpg"),
                caption=f"✅ **Image Enhanced!**\n\n"
                       f"📏 Upscale: {settings['upscale']}x\n"
                       f"😊 Face: {weight_names.get(settings['face_weight'], str(settings['face_weight']))}\n"
                       f"🔪 Sharpen: {settings['sharpen']}"
            )
            
            await callback.message.delete()
            
        except Exception as e:
            await callback.message.edit_text(f"⚠️ Error: {str(e)[:150]}")
    
    elif data == "cancel":
        await callback.message.delete()
        await bot.send_message(user_id, "❌ Cancelled.")
        return
    
    if data != "process" and data != "cancel":
        await callback.message.edit_reply_markup(
            reply_markup=get_settings_keyboard(
                settings['upscale'], 
                settings['face_weight'], 
                settings['sharpen']
            )
        )
    
    await callback.answer()

@dp.message(F.photo)
async def process_photo(message: types.Message):
    await message.answer(
        "⚠️ **Important:**\n\n"
        "For best quality, send photo as **Document (File)**.\n\n"
        "📱 How?\n"
        "• Tap 📎 button\n"
        "• Select «File» or «Document»\n"
        "• Choose your photo"
    )

async def main():
    logging.basicConfig(level=logging.INFO)
    print("Bot is ready!")
    print("Features:")
    print("   - Upscale 2x, 3x, 4x")
    print("   - Face enhancement 6 levels")
    print("   - Button interface")
    await dp.start_polling(bot)

if __name__ == '__main__':
    nest_asyncio.apply()
    asyncio.run(main())
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.methods import DeleteWebhook
from aiogram.types import Message
import requests


TOKEN = '' # ПОМЕНЯЙТЕ ТОКЕН БОТА НА ВАШ
AI_TOKEN = '' # ⁡⁢⁣⁣ПОМЕНЯЙТЕ ТОКЕН ИИ НА ВАШ⁡

url = "https://api.intelligence.io.solutions/api/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {AI_TOKEN}",
}


logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN)
dp = Dispatcher()


# ⁡⁢⁣⁡⁢⁣⁣ОБРАБОТЧИК КОМАНДЫ СТАРТ⁡⁡
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer('Привет! Я бот с подключенной нейросетью, отправь свой запрос', parse_mode = 'HTML')


# ⁡⁢⁣⁣ОБРАБОТЧИК ЛЮБОГО ТЕКСТОВОГО СООБЩЕНИЯ⁡
@dp.message(lambda message: message.text)
async def filter_messages(message: Message):
    data = {
        "model": "deepseek-ai/DeepSeek-R1",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant"
            },
            {
                "role": "user",
                "content": message.text
            }
        ],
    }

    response = requests.post(url, headers=headers, json=data)
    data = response.json()

    text = data['choices'][0]['message']['content']
    bot_text = text.split('</think>\n\n')[1]

    await message.answer(bot_text, parse_mode = "Markdown")


# ⁡⁢⁣⁣ОБРАБОТЧИК ЛЮБОГО ИЗОБРАЖЕНИЯ⁡
@dp.message(lambda message: message.photo)
async def handle_image(message: types.Message):
    file_id = message.photo[-1].file_id # ⁡⁢⁣⁣Берем фото лучшего качества⁡
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}" # ⁡⁢⁣⁣Получим ссылку на изображение⁡

    # ⁡⁢⁣⁣Делаем запрос в ИИ⁡
    data = {
        # "model": "Qwen/Qwen2-VL-7B-Instruct",
        "model": "meta-llama/Llama-3.2-90B-Vision-Instruct",
        "messages": [
            {"role": "system", "content": "You're an AI assistant"},
            {"role": "user", "content": [
                {"type": "text", "text": "What is in this image?"},
                {"type": "image_url", "image_url": {"url": file_url}}
            ]}
        ],
    }

    response = requests.post(url, headers=headers, json=data)
    data = response.json()
    text = data['choices'][0]['message']['content'] # ⁡⁢⁣⁣Получаем нужный текст из ⁡⁢⁣⁣JSON файла⁡

    await message.answer(text, parse_mode = "Markdown") # ⁡⁢⁣⁣Отправляем ответ с помощью бота⁡


async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

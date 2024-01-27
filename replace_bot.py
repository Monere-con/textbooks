import asyncio
import os
import aiofiles.os

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from replace_text import replace_text
from bs4 import BeautifulSoup

token = ''

dp = Dispatcher()
bot = Bot(token, parse_mode=ParseMode.HTML)

@dp.message()
async def echo_handler(message: types.File) -> None:

    if message.document.file_size > 20971520:
        message.answer('Больше 20 МБ - никак')
        return
    if message.document.file_name[-4:] != '.fb2':
        message.answer('Только файлы с расширением fb2')
        return
    
    file_name = message.document.file_name
    file_id = message.document.file_id
    file_info = await bot.get_file(file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    read_text = downloaded_file.read().decode('utf-8')
    soup = BeautifulSoup(read_text, 'xml')
    p_text = soup.find_all('p')
    for line in p_text:
        line.string = replace_text(line.text)

    with open(message.document.file_name, 'w', encoding='utf-8') as new_file:
        new_file.write(str(soup))
    
    book = FSInputFile(new_file.name)
    await message.answer_document(book)
    await aiofiles.os.remove(file_name)

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

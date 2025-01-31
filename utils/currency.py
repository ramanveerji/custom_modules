#  Moon-Userbot - telegram userbot
#  Copyright (C) 2020-present Moon Userbot Organization
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import requests
from pyrogram import Client, filters, enums
from pyrogram.types import Message

from utils.scripts import format_exc, import_library
from utils.misc import modules_help, prefix

bs4 = import_library("bs4", "beautifulsoup4")
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}


@Client.on_message(filters.command(["currency", "cc"], prefix) & filters.me)
async def convert(_, message: Message):
    if len(message.command) == 1:
        await message.edit("<b>Enter currency name</b>")
        return

    name = message.command[1]
    await message.edit("<b>Data retrieval...</b>")

    try:
        if name == "btc":
            name = "1₿"
            link = "https://ru.investing.com/crypto/bitcoin"
        else:
            link = f"https://ru.investing.com/currencies/{name}-usd"

        full_page = requests.get(link, headers=headers, timeout=3)
        soup = BeautifulSoup(full_page.content, "html.parser")
        rub = soup.find("span", class_="text-2xl")
        await message.edit(f"<b>{name} now is </b><code> {rub} </code><b> $</b>")
    except Exception as e:
        await message.edit(format_exc(e))


modules_help["currency"] = {
    "currency [currency]*": "Transfer from any state currency to the dollar. Don't use more than 10 times per minute",
    "cc [currency]*": "Transfer from any state currency to the dollar. Don't use more than 10 times per minute",
}

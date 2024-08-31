import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import asyncio
from aiogram import Bot

# Get API token and chat ID from environment variables
API_TOKEN = os.getenv('API_TOKEN')
chat_id = os.getenv('CHAT_ID')

# Set up Telegram bot
bot = Bot(token=API_TOKEN)

# Set up user-agent string
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.3',
}

# Set up list of URLs to track
urls = [
    'https://www.rrbguwahati.gov.in/',
    'https://rrbkolkata.gov.in/lst5news.php',
    'https://rrbsecunderabad.gov.in/',
    'https://www.rrbchennai.gov.in/',
    'https://www.rrbsiliguri.gov.in/',
    'https://www.rrbmumbai.gov.in/important.php',
    'https://www.rrbahmedabad.gov.in/news.htm',
    'https://rrbbhopal.gov.in/',
    'https://www.rrbcdg.gov.in/',
    'http://www.rrbmalda.gov.in/',
    'https://www.rrbjammu.nic.in/',
    'https://rrbajmer.gov.in/',
    'https://rrbald.gov.in/rrb.asp',
    'https://www.rrbbnc.gov.in/',
    'https://rrbbilaspur.gov.in/notice.html',
    'https://www.rrbgkp.gov.in/',
    'https://www.rrbmuzaffarpur.gov.in/',
    'https://www.rrbpatna.gov.in/Default.aspx',
    'https://rrbranchi.gov.in/?p=packages',
    'https://rrbthiruvananthapuram.gov.in/'
]

known_pdf_links_file = 'rrballlinks.txt'
known_pdf_links = set()

if os.path.isfile(known_pdf_links_file):
    with open(known_pdf_links_file, 'r', encoding='utf-8') as f:
        known_pdf_links = set(f.read().splitlines())

async def main():
    try:
        while True:
            for url in urls:
                try:
                    response = requests.get(url, headers=headers, timeout=10, verify=False)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    links = soup.find_all('a', href=True)

                    for link in links:
                        href = link['href']
                        absolute_url = urljoin(url, href).replace(" ", "%20")

                        if absolute_url.endswith('.pdf') and absolute_url not in known_pdf_links:
                            await bot.send_message(chat_id=chat_id, text=absolute_url)
                            known_pdf_links.add(absolute_url)

                    print(f'Successfully scraped {url}')

                except Exception as e:
                    print(f'Error while accessing {url}: {e}')

            with open(known_pdf_links_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(known_pdf_links))

            await asyncio.sleep(120)
    finally:
        await bot.close()

if __name__ == '__main__':
    asyncio.run(main())

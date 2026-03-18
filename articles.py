import requests 
import textwrap 
from bs4 import BeautifulSoup

url = input("Вкажіть посилання на статтю: ")
msg = f"Ваше посилання: {url}. Починаємо обробку"
print(msg)

responce = requests.get(url)
soup = BeautifulSoup(responce.text, 'html.parser')
header = soup.find('h1')
paragraphs = soup.find_all('p')

with open ("article.txt", "w", encoding="utf-8") as f: 
    f.write(header.text)
    for paragraph in paragraphs:
        f.write(f"\n\n{textwrap.fill(paragraph.text, width=80)}")

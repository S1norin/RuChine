import requests
from bs4 import BeautifulSoup

user_input = 'Боль'
soup = BeautifulSoup(requests.get(f"https://ruwordnet.ru/ru/search/{user_input}").text, 'html.parser')
soup.head.clear()
counter = 0

print(soup.find("div", class_="sense").next_sibling == "\n")
for i in soup.find("div", class_="sense"):
    #    print((soup.find("div", class_="sense").find_all("div", class_="sense")))
    parsed = BeautifulSoup(str(i), 'html.parser')
    result = BeautifulSoup(str(parsed), 'html.parser').find_all("div", class_="sense")
    for words in result:
        if not ("." in words.get_text(strip=True) and "i" in words.get_text(strip=True)):
            print(words.get_text(strip=True).strip(","))

for i in soup.find("div", class_="sense").next_siblings:
    #    print((soup.find("div", class_="sense").find_all("div", class_="sense")))
    parsed = BeautifulSoup(str(i), 'html.parser')
    result = BeautifulSoup(str(parsed), 'html.parser').find_all("div", class_="sense")
    for words in result:
        if not ("." in words.get_text(strip=True) and "i" in words.get_text(strip=True)):
            print(words.get_text(strip=True).strip(","))

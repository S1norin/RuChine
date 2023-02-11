import requests
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer

user_input = input()
soup = BeautifulSoup(requests.get(f"https://ruwordnet.ru/ru/search/{user_input}").text, 'html.parser')
soup.head.clear()

printed = []

if None == soup.find("div", class_="sense"):
    print(f"Слова {user_input.lower()} нет в RuWordNet. Введите другое.")
else:
    for i in soup.find("div", class_="sense"):
        parsed = BeautifulSoup(str(i), 'html.parser')
        result = BeautifulSoup(str(parsed), 'html.parser').find_all("div", class_="sense")
        for words in result:
            if not ("." in words.get_text(strip=True) and "i" in words.get_text(strip=True)) \
                    and not (words.get_text(strip=True).strip(",") in printed):
                print(words.get_text(strip=True).strip(","))
                printed.append(words.get_text(strip=True).strip(","))

    for i in soup.find("div", class_="sense").next_siblings:
        #    print((soup.find("div", class_="sense").find_all("div", class_="sense")))
        parsed = BeautifulSoup(str(i), 'html.parser')
        result = BeautifulSoup(str(parsed), 'html.parser').find_all("div", class_="sense")
        for words in result:
            if not ("." in words.get_text(strip=True) and "i" in words.get_text(strip=True)):
                print(words.get_text(strip=True).strip(","))

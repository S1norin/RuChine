import spacy
import requests
from bs4 import BeautifulSoup
from sys import stdin

user_input = [sentence.strip() for sentence in stdin]
output = []
for sentence in user_input:
    nlp = spacy.load("ru_core_news_lg")
    doc = nlp(sentence)
    for token in doc:
        soup = BeautifulSoup(requests.get(f"https://ruwordnet.ru/ru/search/{token.lemma_}").text, 'html.parser')
        soup.head.clear()

        printed = []

        if None == soup.find("div", class_="sense"):
            pass
            # print(f"Слова {token.lemma_.lower()} нет в RuWordNet. Введите другое.")
        else:
#            print("------------------------------------------")
            for i in soup.find("div", class_="sense"):
                lst_of_words_and_synonyms = []
                parsed = BeautifulSoup(str(i), 'html.parser')
                result = BeautifulSoup(str(parsed), 'html.parser').find_all("div", class_="sense")
                for words in result:
                    if not ("." in words.get_text(strip=True) and "i" in words.get_text(strip=True)) \
                            and not (words.get_text(strip=True).strip(",") in printed):
                        lst_of_words_and_synonyms.append(words.get_text(strip=True).strip(","))
                        printed.append(words.get_text(strip=True).strip(","))
                if not (lst_of_words_and_synonyms == []):
                    output.append([token.lemma_, *lst_of_words_and_synonyms])
print(output)


'''
for i in soup.find("div", class_="sense").next_siblings:
    print((soup.find("div", class_="sense").find_all("div", class_="sense")))
    parsed = BeautifulSoup(str(i), 'html.parser')
    result = BeautifulSoup(str(parsed), 'html.parser').find_all("div", class_="sense")
    for words in result:
        if not ("." in words.get_text(strip=True) and "i" in words.get_text(strip=True)):
            print(words.get_text(strip=True).strip(","))
'''

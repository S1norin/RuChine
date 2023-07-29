import spacy
import lingcorpora
import requests
import pymorphy2
from bs4 import BeautifulSoup
from sys import stdin
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bert_score import score


def inflect(tag_source, word_to_inflect):
    if tag_source.tag.POS == word_to_inflect.tag.POS == "NOUN":
        tags = [tag_source.tag.case, tag_source.tag.number]
        if tags[1 == "Pltm"]:
            try:
                return word_to_inflect.inflect({"NOUN", tags[0], "plur"}).word
            except AttributeError:
                return None
        try:
            return word_to_inflect.inflect({"NOUN", tags[0], tags[1]}).word
        except AttributeError:
            print(tags, word_to_inflect)
            return None

    elif (tag_source.tag.POS == "ADJF" or tag_source.tag.POS == "ADJS" or tag_source.tag.POS == "COMP") and (
            word_to_inflect.tag.POS == "ADJF" or word_to_inflect.tag.POS == "ADJS" or word_to_inflect.tag.POS == "COMP"):
        tags = [tag_source.tag.gender, tag_source.tag.case, tag_source.tag.number]
        return word_to_inflect.inflect({tags[0], tags[1], tags[2]}).word

    elif tag_source.tag.POS == "VERB" or tag_source.tag.POS == "INFN":
        tags = [tag_source.tag.gender, tag_source.tag.mood, tag_source.tag.number, tag_source.tag.person,
                tag_source.tag.tense]
        if tags[4] != 'past':
            if word_to_inflect.inflect({"VERB", tags[1], tags[2], tags[3], tags[4]}) is None:
                return None
            return word_to_inflect.inflect({"VERB", tags[1], tags[2], tags[3], tags[4]}).word
        else:
            if word_to_inflect.inflect({tags[0], tags[1], tags[2], tags[4]}) is None:
                return None
            return word_to_inflect.inflect({tags[0], tags[1], tags[2], tags[4]}).word

    elif tag_source.tag.POS == "PRTF" and word_to_inflect.tag.POS == "PRTF":
        tags = [tag_source.tag.gender, tag_source.tag.case, tag_source.tag.number]
        try:
            return word_to_inflect.inflect({"PRTF", tags[0], tags[1], tags[2]}).word
        except ValueError:
            print(tags, word_to_inflect)
            return None
    elif word_to_inflect.tag.POS == "PRTS" and tag_source.tag.POS == "PRTS":
        tags = [tag_source.tag.gender, tag_source.tag.number]
        try:
            return word_to_inflect.inflect({"PRTS", tags[0], tags[1]}).word
        except AttributeError:
            print(tags, word_to_inflect)
            return None


def is_foreign(word):
    dr = webdriver.Chrome(ChromeDriverManager().install())
    dr.get(f"https://gufo.me/dict/foreign_words/{word.lower()}")
    req = requests.Session()
    foreign_db = BeautifulSoup(dr.page_source, 'html.parser')
    foreign_db.header.clear()
    if foreign_db.body.div.find("section", class_="site-error") is None:
        return True
    else:
        return False


def update_found_list(words):
    for word in words:
        if word not in found:
            found.add(word)  # Проверка дупликатов в текущей итерации


# user_input = [sentence.strip() for sentence in stdin]
user_input = [
    "Когда среди монстров в лабиринте начали происх+одить аномальные явления, Отс запросил помощь своих союзников из Империи Ренксандт в поиске и устранении причины проблемы. Приняв запрос, Империя отправила группу рыцарей в лабиринт для расследования."]
output = []
synonyms = {}
morph = pymorphy2.MorphAnalyzer()

for sentence in user_input:
    nlp = spacy.load("ru_core_news_lg")
    doc = nlp(sentence)
    for token in doc:
        soup = BeautifulSoup(requests.get(f"https://ruwordnet.ru/ru/search/{token.lemma_}").text, 'html.parser')
        soup.head.clear()
        added = set()
        if soup.find("div", class_="sense") is None:
            continue
        else:
            for i in soup.find("div", class_="sense"):
                found, result = set(), list()
                soup_parsed = BeautifulSoup(str(i), 'html.parser').find_all("div", class_="sense")
                if soup_parsed != []:
                    synonyms_current = [word.get_text(strip=True).strip(",.") for word in soup_parsed if
                                        not "i" in word.get_text(strip=True) and word.get_text(strip=True).strip(
                                            ",.") not in found]
                    update_found_list([word.get_text(strip=True).strip(",.") for word in soup_parsed if
                                       not "i" in word.get_text(
                                           strip=True)])  # на этот момент сформирован список синонимов и дубликатов
                    synonyms[token.lemma_] = synonyms_current
                    for replacement in synonyms_current:
                        if len(replacement.split()) > 1:  # Проверка на два слова
                            continue
                        else:
                            original_parsed = morph.parse(token.text)[0]
                            replacement_parsed = morph.parse(replacement)[0]
                            sentence_with_suggested_word = sentence[:]
                            # замена слова в предложении
                            output.append(
                                sentence_with_suggested_word.replace(token.text, replacement))

oleg = score(output, user_input * len(output), lang="ru", verbose=True)
oleg = oleg[2]
oleg_sorted, oleg_indices = oleg.sort(descending=True)

# get the indices as a list
oleg_indices_list = [i.item() for i in oleg_indices]

# print the sorted tensor and indices
print(oleg_sorted)
print(oleg_indices_list)

# print the corresponding elements from output
for i in oleg_indices_list:
    print(oleg[i], output[i])

print(synonyms)

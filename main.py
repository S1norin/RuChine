'''def Gloss():


    import spacy
from spacy.lang.ru.examples import sentences

Glossary = "ROOT, acl, advcl, advmod, amod, appos, aux, case, cc, ccomp, compound, conj, cop, csubj,  dep, det, discourse, expl, fixed, flat, iobj, list, mark, nmod, nsubj, nummod, obj, obl, orphan, parataxis, punct, xcomp".split(
    ", ")
for i in Glossary:
    print(i, "-", spacy.explain(i))
'''
import requests
from bs4 import BeautifulSoup

while True:
    output = []
    soup = BeautifulSoup(requests.get(f"https://ruwordnet.ru/ru/search/Боль").text, 'html.parser')
    soup.head.clear()
    print((soup.find("div", class_="sense").find_all("div", class_="sense")))
    result = soup.find("div", class_="sense").find_all("div", class_="sense")
    print(result)
    print("***************************************************************************")
    print("------------------------------------")
    for i in result:
        if i.get_text(strip=True).endswith(","):
            output.append(i.get_text(strip=True)[:-1])
            continue
        output.append(i.get_text(strip=True))
    print(output)
    soup.find("div", class_="sense").nextSibling

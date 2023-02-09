'''def Gloss():


    import spacy
from spacy.lang.ru.examples import sentences

Glossary = "ROOT, acl, advcl, advmod, amod, appos, aux, case, cc, ccomp, compound, conj, cop, csubj,  dep, det, discourse, expl, fixed, flat, iobj, list, mark, nmod, nsubj, nummod, obj, obl, orphan, parataxis, punct, xcomp".split(
    ", ")
for i in Glossary:
    print(i, "-", spacy.explain(i))
'''
'''import requests
from bs4 import BeautifulSoup



soup = BeautifulSoup(requests.get(f"https://ruwordnet.ru/ru/search/Боль").text, 'html.parser')
soup.head.clear()
counter = 0

for j in soup.find("div", class_="sense"):
#    print((soup.find("div", class_="sense").find_all("div", class_="sense")))
    output = []
    result = soup.find("div", class_="sense").find_all("div", class_="sense")
#    print(result)
    print("***************************************************************************")
    print("------------------------------------")
    for i in result:
        output.append(i.get_text(strip=True).strip(","))
    print(output)
    counter += 1
    print(counter)
    soup.nextsibling
'''

import requests
from bs4 import BeautifulSoup

soup = BeautifulSoup(requests.get(f"https://ruwordnet.ru/ru/search/Боль").text, 'html.parser')
soup.head.clear()
counter = 0

for j in soup.find("div", class_="sense").next_elements:
    #    print((soup.find("div", class_="sense").find_all("div", class_="sense")))
    j = BeautifulSoup(j, 'html.parser')
    result = j.get_text(strip=True).strip(",")
    print(result)
print("***************************************************************************")
print("------------------------------------")
'''    for i in result:
        output.append(i.get_text(strip=True).strip(","))
    print(output)
    counter += 1
    print(counter)
'''

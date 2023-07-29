import requests
import json
import csv

IAM_TOKEN = 't1.9euelZqdz52KjZ6TzcjMkIqPjseUne3rnpWajZaXjJvNksqLjsadycaVmpTl9PcpQXdZ-e9ZSk-K3fT3aW90WfnvWUpPis3n9euelZqLx5GZnIvJjpHMx5aQyovOyO_8xeuelZqLx5GZnIvJjpHMx5aQyovOyA.2fggj-PCEjrrMCoWpBeVxXNl-EN-wQaKumtBHxyybEnPmkCtfBNF8qGqlOgoLsbjqPIJeYVNLX8srQ6RyiofDQ'
folder_id = 'b1g2niaicl9kdmfrn5r4'
target_language = 'ru'
oleg = requests.get(f'https://ruscorpora.ru/ru/api/export?query=%7B%22params%22%3A%7B%22pageParams%22%3A%7B%22page%22%3A%220%22%2C%22docsPerPage%22%3A%2210%22%2C%22snippetsPerPage%22%3A%2250%22%2C%22snippetsPerDoc%22%3A%220%22%7D%2C%22sampling%22%3A%220%22%2C%22noDiacritic%22%3Atrue%2C%22format%22%3A%22csv%22%7D%2C%22corpus%22%3A%7B%22type%22%3A%22PARA%22%2C%22lang%22%3A%22eng%22%7D%2C%22resultType%22%3A%5B%22CONCORDANCE%22%5D%2C%22exactForm%22%3A%7B%22sectionValues%22%3A%5B%7B%22conditionValues%22%3A%5B%7B%22fieldName%22%3A%22req%22%2C%22text%22%3A%7B%22v%22%3A%22{input()}%22%7D%7D%5D%7D%5D%7D%7D')
oleg.encoding = "utf-8"
request_result = oleg.text.split("\n")
request_result = [x.split(';') for x in request_result[1:]]
for row in request_result:
    print(row[21])
    texts = [row[23]]
    body = {
        "targetLanguageCode": target_language,
        "texts": texts,
        "folderId": folder_id,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(IAM_TOKEN)
    }
    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
        json = body,
        headers = headers
    )
    response_json = json.loads(response.text)
    translations = response_json['translations']
    translated_texts = [t['text'] for t in translations]

    print(translated_texts)



'''response_json = json.loads(response.text)
translations = response_json['translations']
translated_texts = [t['text'] for t in translations]

print(translated_texts)'''

'''def update_found_list(words):
    for word in words:
        if word not in found:
            found.add(word)  # Проверка дупликатов в текущей итерации


# user_input = [sentence.strip() for sentence in stdin]
user_input = [
    "А если серьёзно, то я тут не вижу в реплике Сумики ничего, что действительно оправдывало бы выбор не самого простого для произношения в стрессовой ситуации словосочетания не обязан"]
output = ["oleg", "petr"]
synonyms = {}


oleg = score(user_input * 2, user_input * 2,  lang="ru", verbose=True)
print(oleg, oleg[0], oleg[1], oleg[2])
r, i, f, j = oleg[0], oleg[1], oleg[2], output
for a, b in oleg[2], output:
    print(a, b)


print(synonyms)
'''
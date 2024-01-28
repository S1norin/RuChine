# Установка
Для работы программы вам потребуется
- Python
- [Pandas](https://pandas.pydata.org/)
- [SpaCy](https://spacy.io/)
	- Модель `ru_core_news_lg` (https://spacy.io/models/ru#ru_core_news_lg)

# Запуск
Программа запускается исполнением файла `main.py`

# Остальные файлы
- `RuCorpora.py` - программа, с которой извлекались тексты из [НКРЯ](https://ruscorpora.ru/) и отправлялись на перевод в Yandex.Cloud для составления списка `word_similarity.csv`
- `word_similarity.csv` - список схожести слов, необходимый для работы `main.py`. Содержит в себе пары слов и их векторную схожесть, построенную *SpaCy* 
- `stopwords-ru.txt` - файл, содержащий стоп-слова. Взят с репозитория [stopwords-ru](https://github.com/stopwords-iso/stopwords-ru)

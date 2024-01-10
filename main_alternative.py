import spacy
import pandas

df = pandas.read_csv("finalized_word_similarity.csv", delimiter="|")
nlp = spacy.load("ru_core_news_lg")
user_input = "огда прибывает гость или посторонний, обычно их поприветствовать выходит глава внешнего павильона Гым Гухо. Внешний зал также является частью Внешнего Павильона. Большинство событий, которые происходили за пределами Альянса Нефритовых Небес, входили в юрисдикцию Внешнего Павильона."
doc = nlp(user_input)
core_arguments = ["nsubj", "nsubj:pass", "obj", "iobj", "csubj", "csubj:pass", "ccomp", "xcomp"]
non_core_dependents = ["obl", "obl:agent", "expl", "advcl", "advmod", "discourse", "aux", "aux:pass", "cop", "mark"]
nominal_dependents = [ "nmod", "appos", "nummod", "nummod:gov", "acl", "acl:relcl", "amod", "det"]
stopwords_to_print = []
nsubj_pass_list = []
aux_pass_list = []
csubj_pass_list = []
passive_flag = True
tok_l = doc.to_json()["tokens"]
with open("stopwords-ru.txt", encoding="utf-8") as file:
    stopwords_list = [i.strip() for i in file.readlines()]


def check_synonyms(token, threshold):
    current_result = df.loc[((df["Word-1"] == token.lemma_) | (df["Word-2"] == token.lemma_)) & (df["Score"] > threshold)]
    if current_result.shape[0] > 0:
        print("---------------------------------")
        print(token.lemma_)
        if token.lemma_ in current_result["Word-1"]:
            result = current_result[current_result["Word-2"] != token.lemma_]
            print(result[["Word-2", "Score"]])
        else:
            result = current_result[current_result["Word-1"] != token.lemma_]
            print(result[["Word-1", "Score"]])
        print("---------------------------------")

for token in doc:
    if token.dep_ in core_arguments:
        if token.dep_ == "nsubj:pass":
            nsubj_pass_list.append(token)
        if token.dep_ == "csubj:pass":
            csubj_pass_list.append(token)
        check_synonyms(token, 0.5)
    elif token.dep_ in non_core_dependents:
        if token.dep_ == "aux:pass":
            aux_pass_list.append(token)


    elif token.dep_ in nominal_dependents:
        check_synonyms(token, 0.4)
    if token.lemma_ in stopwords_list:
        stopwords_to_print.append(token)
if stopwords_to_print:
    print("В вашем предложении есть стоп-слова, захламляющие текст")
    print(*stopwords_to_print, sep=", ")


for t in tok_l:
    head = tok_l[t["head"]]
    if "pass" in t['dep']:
        if passive_flag:
            print("В вашем предложении используется пассивный залог, затрудняющий восприятие текста")
        print(user_input[t['start']:t['end']], user_input[head['start']:head['end']])
        passive_flag = False



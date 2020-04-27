import requests
from lxml import html
import re
from prettytable import PrettyTable
from snowballstemmer import EnglishStemmer

words = {}

r = requests.get("https://habr.com/en/company/wargaming/blog/436180/")
h = html.fromstring(r.text)

content = h.xpath('//*[@id="post-content-body"]')[0]

text = html.tostring(content).decode()

text = re.sub('\<[^()]*\>', '', text)
text = re.sub(r"[^A-Za-zА-Яа-я]+", ' ', text)

texts = text.split(" ")



for t in texts:
    if t == '':
        continue

    t = t.lower()
    t = EnglishStemmer().stemWord(t)

    if t in words:
        words[t] += 1
    else:
        words[t] = 1


table = PrettyTable(["Слово", "Количество"])

for t in words:
    table.add_row( [t, words[t] ] )

table.sortby = "Количество"
table.reversesort = True

print(table)
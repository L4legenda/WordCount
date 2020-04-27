import requests # библиотека для запросов
from lxml import html # библиотека для обработки html
import re # библиотека для регулярных выражений
from prettytable import PrettyTable #Для составления таблиц
from snowballstemmer import EnglishStemmer # Для поиска основы слова

words = {} # Храним все слова и их количество


#Страница с обработкой слов
r = requests.get("https://habr.com/en/company/wargaming/blog/436180/")
h = html.fromstring(r.text) #Перевод текста в html

content = h.xpath('//*[@id="post-content-body"]')[0] #область где обрабатывает текст

text = html.tostring(content).decode() #Переводим все в текст

text = re.sub('\<[^()]*\>', '', text) # Вжух магия
text = re.sub(r"[^A-Za-zА-Яа-я]+", ' ', text) # Вжух магия
# Вот и чистый текст без символов


texts = text.split(" ") # делем текст на отдельные слова



for t in texts: # Проходимся по словам
    if t == '': # Если слова нет, то пропускает итерацию
        continue

    t = t.lower() # Преобразует слово в нижний регистр
    t = EnglishStemmer().stemWord(t) # Ищет основу слова

    if t in words: # Если слово уже есть то прибавляет в количество
        words[t] += 1
    else: # Если слова нет, то создает его в списке и добавляет значение 1
        words[t] = 1

# Создает таблицу с колонками ["Слово", "Количество"]
table = PrettyTable(["Слово", "Количество"])

#Перебираем все слова
for t in words:
    table.add_row( [t, words[t] ] ) #Добавляем в таблицу

table.sortby = "Количество" #Сортируем по столбцу "Количество"
table.reversesort = True #Реверсируем столбец

print(table) # Выводим результат.
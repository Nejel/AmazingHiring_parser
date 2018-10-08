# coding: utf-8

import docx
import re
import os
import csv
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np


cwd = os.getcwd() + '\\'
filename = 'results.csv'
content = [] # глобальная переменная для контента перед записью в csv
url = []
name = []
description = []

def Search(fullText): # функция поиска по тексту. Вызывается функцией получения текста
    #print('Search', fullText)
    findURL = re.findall('https://\S+|http://\S+', str(fullText), flags = 0)
    print('SearchURL', findURL)
    for i in findURL:
        url.append(i)
    findRecruit = re.findall('Таня|Валя|Никита|Даша Мелкова|[А-Я][а-я]\S+ [А-Я][а-я]\S+\bЛаборатория \b', str(fullText), flags = 0)
    print('Searchrecruit', findRecruit)
    for x in findRecruit:
        name.append(x)
    finddescription = re.findall('У нас \S+|Тут \S+|Описание .+', str(fullText), flags = 0)
    for y in finddescription:
        description.append(y)
        #hmhm = ''.join(y)
        #print('hmhm: ', hmhm)
    searchresults = url, name, description
    print('searchresults', ''.join(str(searchresults)))
    return searchresults

def getText(filename): # функция получения текста из файла.
                        # Вызывается главной функцией ReadFolderAndFiles
    doc = docx.Document(filename)
    fullText = []
    i = 0
    while i < 1:
        for para in doc.paragraphs:
            #print(type(fullText)) # list
            fullText.append(para.text)
        URLsearchResults = Search(fullText) # tuple # вызываем поиск по тексту
        fullText = URLsearchResults
        i += 1
    return fullText # list

def ReadFolderAndFiles(content):
    #foldername = (input('Enter a folder name: ')) # ждем ввода папки
    foldername = ('vacancies') # по умолчанию установлена папка vacancies
    cwd2 = cwd + foldername # собираем конструктор пути файла
    for x in (os.listdir(cwd2)):
        filename = cwd2 + '\\' + x # собираем конструктор пути файла
        print(filename)
        #print(getText(filename))
        content.append(getText(filename)) # list # добавляем в конец листа
        #fullcontent = ''.join(content)
    return content # происходит выход из функции после завершения цикла for, в глобальное пространтсов возвращается значение контент


ReadFolderAndFiles(content) # вызываем функцию с параметром, чтобы вернуть значение

#df = pd.DataFrame({
#'a': url,
#'b': name,
#'c': description
#})

#writer = ExcelWriter('Results.xlsx')
#df.to_excel(writer,'Sheet1',index=False)
#writer.save()

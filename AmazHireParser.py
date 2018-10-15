# coding: utf-8

# import docx # pip install python-docx
import re
import sqlite3
import os
import csv
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np

import openpyxl
import os
import selenium
import stat
import bs4
import time
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys


cwd = os.getcwd() + '\\'
filename = 'results.csv'
content = [] # глобальная переменная для контента перед записью в csv
url = []
name = []
description = []

def PutToDB(linktoprofile, heading1):
    print('1')
    #writeprofile


def Search(candicemail): # функция поиска по тексту. Вызывается функцией получения текста
    #print('Search', fullText)
    global browser
    candicemailconstr = str(re.sub(r'@', '%40', candicemail))
    print(candicemailconstr)
    URLconstr = ('https://search.amazinghiring.com/profiles/?q=booleanText[0]:' + candicemailconstr)
    browser.get(URLconstr)


    #Emailtofindinsert = browser.find_element_by_css_selector('#app > div > div.Layout-container___2p9Cf > div.Layout-content___Jsbfq > div > div > div > div > div.Container-content___tnlBM > div > div.SearchForm-wrapper___3jwDD.SearchForm-wrapper_active___2x94e > div > div:nth-child(1) > div.Group-inner___2Na1X > div > div > div > div > div > div > div')


    #Emailtofindinsert.send_keys(candicemail)

    #NaityButton = browser.find_element_by_css_selector('#app > div > div.Layout-container___2p9Cf > div.Layout-content___Jsbfq > div > div > div > div > div.Container-content___tnlBM > div > div.SearchForm-wrapper___3jwDD.SearchForm-wrapper_active___2x94e > div > div:nth-child(3) > div:nth-child(2) > button > span').click()

    time.sleep(15)

    #FindProfile = browser.find_element_by_css_selector('#app > div > div.Layout-container___2p9Cf > div.Layout-content___Jsbfq > div > div > div.Search-main___2MzEQ > main > div.Profiles-profiles___60VKV > div.ShortProfile-wrapper_visited___3Rudd > div > div.Card-grid___1E537.Card-grid_emptyTags___308lk > div.Card-content___31v2o > div > div.ShortProfile-body___3VBbs > div > div.MainInfo-title___3gHQf > div.MainInfo-title-content___1Ek61 > a')

    #FindProfile = browser.find_element_by_class_name('MainInfo-link___1wBnD')

    # class = MainInfo-link___1wBnD
    #profileresults = browser.find_element_by_partial_link_text("https://search.amazinghiring.com/profiles/")
    #print('profileresults', profileresults)

    try:
        linktoprofile = driver.find_element_by_class_name('MainInfo-link___1wBnD')
        #heading1 = driver.find_element_by_tag_name('h1')
        #print(heading1)
    except:
        print('Nothing was found')
    #class = MainInfo-link___1wBnD
    #тут надо записать в переменную URL профиля кандика
    PutToDB(linktoprofile, heading1)


    '''
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
    '''

def getText(filename): # функция получения текста из файла.
                        # Вызывается главной функцией ReadFolderAndFiles
    os.chdir('C:\\Users\\Alex\\Desktop\\Learning\\Python\\Saske\\AmazingHiring_parser\\workdir')
    workbook = openpyxl.load_workbook('Testlist.xlsx')
    #sheet = workbook.get_sheet_by_name('Sheet1')
    #DeprecationWarning: Call to deprecated function get_sheet_by_name (Use wb[sheetname]).
    sheet = workbook["Sheet1"]
    print(sheet)
    imax = 3
    for i in range (2, imax):
        #Candicemail = str(sheet['A'+str(i)].value)
        #Candicemail = sheet['A2']
        candicemail = sheet.cell(row = i, column = 1)
        print(candicemail.value)
        candicemail = str(candicemail.value)
        URLsearchResults = Search(candicemail) # tuple # вызываем поиск по тексту
        print('gettext', candicemail)
    return URLsearchResults

    #doc = docx.Document(filename)
    #fullText = []
    #i = 0
    #while i < 1:
    #    for para in doc.paragraphs:
    #        #print(type(fullText)) # list
    #        fullText.append(para.text)
    #    URLsearchResults = Search(fullText) # tuple # вызываем поиск по тексту
    #    fullText = URLsearchResults
    #    i += 1
    #return fullText # list

def ReadFolderAndFiles(content): # вызываем функцию с параметром, чтобы вернуть значение
    #foldername = (input('Enter a folder name: ')) # ждем ввода папки
    foldername = ('workdir') # по умолчанию установлена папка workdir
    cwd2 = cwd + foldername # собираем конструктор пути файла
    for x in (os.listdir(cwd2)):
        filename = cwd2 + '\\' + x # собираем конструктор пути файла
        print(filename)
        print(getText(filename))
        content.append(getText(filename)) # list # добавляем в конец листа
        #fullcontent = ''.join(content)
    return content # происходит выход из функции после завершения цикла for, в глобальное пространтсов возвращается значение контент

def OpenBrowser():
    global browser
    # спрашиваем логин пароль
    username = input('USERNAME:', )
    password = input('PASSWD:', )

    # открываем броузер

    browser.get('https://search.amazinghiring.com/login/?next=/')
    time.sleep(1)
    # логинимся
    Emailinsert = browser.find_element_by_css_selector('#app > div > div:nth-child(3) > div > div.Login-centerBlock___3BZag > form > div:nth-child(4) > div:nth-child(1) > input')
    #Emailinsert = browser.find_element_by_css_selector('#email')
    Passwordinsert = browser.find_element_by_css_selector('#app > div > div:nth-child(3) > div > div.Login-centerBlock___3BZag > form > div:nth-child(4) > div:nth-child(2) > input')
    #Passwordinsert = browser.find_element_by_css_selector('#password')
    Emailinsert.send_keys(username)
    Passwordinsert.send_keys(password)
    time.sleep(0.3)
    Passwordinsert.send_keys(Keys.ENTER)
    time.sleep(3)
    ReadFolderAndFiles(content)


conn = sqlite3.connect('db.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Counts')
cur.execute('''CREATE TABLE Counts (org TEXT, count INTEGER)''')

browser = webdriver.Chrome()
OpenBrowser()


#df = pd.DataFrame({
#'a': url,
#'b': name,
#'c': description
#})

#writer = ExcelWriter('Results.xlsx')
#df.to_excel(writer,'Sheet1',index=False)
#writer.save()

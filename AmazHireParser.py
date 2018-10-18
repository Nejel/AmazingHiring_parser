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
content = []


def PutToDB(linktoprofile, candicemail):
    global cur
    global conn
    print('Trying to put him in DB')
    cur.execute('SELECT amazeprofile FROM Counts WHERE email = ? ', (candicemail,))
    row = cur.fetchone()
    try:
        print('Im trying', linktoprofile)
        cur.execute('INSERT INTO Counts (email, count, amazeprofile) VALUES (?, 1, ?)', (candicemail, linktoprofile)) # что-то здесь нечисто
        print('After this line')
        conn.commit()
        print('After conn commit line')
    except:
        print('Something went wrong')

def Search(candicemail):
    global browser
    candicemailconstr = str(re.sub(r'@', '%40', candicemail))
    print(candicemailconstr)
    URLconstr = ('https://search.amazinghiring.com/profiles/?q=booleanText[0]:' + candicemailconstr)
    browser.get(URLconstr)
    time.sleep(10)

    try:
        linktoprofile = browser.find_element_by_xpath("//a[contains(@href,'profile')]").get_attribute("href")
        print('I found some guy', linktoprofile)
        #linktoprofile.click()
        #time.sleep(1)
        #finalllylink = browser.getCurrentUrl() # не работает
        #print(browser.current_url)

        #print('Finally link', browser.current_url)
        #main_window = browser.current_window_handle
        #browser.switch_to_window(main_window)
        #browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)

        #finallinktoprofile = browser.current_url
        #print('Finally link2', finallinktoprofile)
        #linktoprofile.getAttribute(href)

        PutToDB(linktoprofile, candicemail)
    except:
        print('Nothing was found')

def getText(filename): # функция получения текста из файла.
                        # Вызывается главной функцией ReadFolderAndFiles
    global cur
    global conn
    os.chdir('C:\\Users\\Alex\\Desktop\\Learning\\Python\\Saske\\AmazingHiring_parser\\workdir')
    workbook = openpyxl.load_workbook('Testlist.xlsx')
    #sheet = workbook.get_sheet_by_name('Sheet1')
    #DeprecationWarning: Call to deprecated function get_sheet_by_name (Use wb[sheetname]).
    sheet = workbook["Sheet1"]
    print(sheet)
    row_count = sheet.max_row
    print(row_count)
    imax = int(row_count)
    for i in range (2, imax):
        #Candicemail = str(sheet['A'+str(i)].value)
        #Candicemail = sheet['A2']
        candicemail = sheet.cell(row = i, column = 1)
        print(candicemail.value)
        candicemail = str(candicemail.value)
        cur.execute('SELECT count FROM Counts WHERE email = ? ', (candicemail,))
        row = cur.fetchone()
        if row is None:
            cur.execute('INSERT INTO Counts (email, count) VALUES (?, 1)', (candicemail,))
            conn.commit()
            URLsearchResults = Search(candicemail)
        else:
            #break
            print('We are going ELSE in getText')
            cur.execute('UPDATE Counts SET count = count + 1 WHERE email = ? ', (candicemail,))
            conn.commit()
        print('gettext', candicemail)
    #return URLsearchResults


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
    input('It\'s time to accept cookies')
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
#cur.execute('DROP TABLE IF EXISTS Counts')
cur.execute('''CREATE TABLE IF NOT EXISTS Counts (email TEXT, count INTEGER, amazeprofile TEXT)''')
browser = webdriver.Chrome()
OpenBrowser()

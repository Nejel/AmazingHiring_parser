# coding: utf-8

import re
import sqlite3
import os
import openpyxl
import selenium
import bs4
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

def OpenBrowser():
    global browser
    # открываем броузер
    browser.get('https://search.amazinghiring.com/login/?next=/')
    time.sleep(1)
    input('It\'s time to accept cookies and press Enter')
    # логинимся
    Emailinsert = browser.find_element_by_css_selector('#app > div > div:nth-child(3) > div > div.Login-centerBlock___3BZag > form > div:nth-child(4) > div:nth-child(1) > input')
    Passwordinsert = browser.find_element_by_css_selector('#app > div > div:nth-child(3) > div > div.Login-centerBlock___3BZag > form > div:nth-child(4) > div:nth-child(2) > input')
    Emailinsert.send_keys(username)
    Passwordinsert.send_keys(password)
    time.sleep(0.3)
    Passwordinsert.send_keys(Keys.ENTER)
    time.sleep(3)
    ReadFolderAndFiles()

def ReadFolderAndFiles():
    global cwd
    global cwdstr
    for x in (os.listdir(cwd)):
        filename = cwdstr + '\\' + x # собираем конструктор пути файла
        print(filename)
        #print(getText(filename))
        content.append(ExcelWorks(filename)) # list # добавляем в конец листа
        #fullcontent = ''.join(content)
    return content # происходит выход из функции после завершения цикла for, в глобальное пространтсов возвращается значение контент

def ExcelWorks(filename):
    global cur
    global conn
    global linktoprofile
    global skills
    workbook = openpyxl.load_workbook('Testlist.xlsx')
    sheet = workbook["Sheet1"]
    print('looking at the list', sheet)
    row_count = sheet.max_row
    print('count of the emails', (int(row_count)-1))
    imax = int(row_count)
    for i in range (2, imax):
        candicemail = sheet.cell(row = i, column = 1)
        print(candicemail.value)
        candicemail = str(candicemail.value)
        cur.execute('SELECT count FROM Counts WHERE email = ? ', (candicemail,))
        row = cur.fetchone()
        #linktoprofile = []
        if row is None:
            cur.execute('INSERT INTO Counts (email, count) VALUES (?, 1)', (candicemail,))
            conn.commit()
            Search(candicemail)
            print('before insertions', linktoprofile)
            # insert linktoprofile to xlsx
            sheet.cell(row = i, column = 2).value = linktoprofile
            sheet.cell(row = i, column = 3).value = skills
            workbook.save('Testlist.xlsx')
        else:
            print('It looks like we have alredy found', candicemail)
            cur.execute('UPDATE Counts SET count = count + 1 WHERE email = ? ', (candicemail,))
            conn.commit()

def Search(candicemail):
    global browser
    global linktoprofile
    global skills
    candicemailconstr = str(re.sub(r'@', '%40', candicemail))
    URLconstr = ('https://search.amazinghiring.com/profiles/?q=booleanText[0]:' + candicemailconstr)
    browser.get(URLconstr)
    time.sleep(10)
    try:
        linktoprofile = browser.find_element_by_xpath("//a[contains(@href,'profile')]").get_attribute("href")
        print('I found some guy', linktoprofile)
        try:
            skills = browser.find_element_by_xpath("//*[contains(@class,'Skills-skill__skill')]").text
            print('skills found: ', skills)
        except:
            print('unluck to find any skills')#
        PutToDB(linktoprofile, candicemail, skills)
    except:
        print('Nothing was found')
    return linktoprofile

def PutToDB(linktoprofile, candicemail, skills):
    global cur
    global conn
    print('Trying to put him in DB')
    cur.execute('SELECT amazeprofile FROM Counts WHERE email = ? ', (candicemail,))
    row = cur.fetchone()
    try:
        print('Im trying', linktoprofile)
        cur.execute('INSERT INTO Counts (email, count, amazeprofile, skill) VALUES (?, 1, ?, ?)', (candicemail, linktoprofile, skills)) # что-то здесь нечисто
        print('After this line')
        conn.commit()
        print('After conn commit line')
    except:
        print('Something went wrong')
    return linktoprofile


username = input('USERNAME:', )
password = input('PASSWD:', )
linktoprofile = 'Nothing was found'
skills = 'skills wasnt found'
cwd = os.chdir(os.getcwd() + '\\workdir')
cwdstr = str(cwd)
whattofind = open('whattofind.txt', 'r')
whattofindfile = whattofind.read()
print('I\'am looking for:', whattofindfile.split(','))
whattofindfilesearch = whattofindfile.split(',')
content = []
conn = sqlite3.connect('db.sqlite')
cur = conn.cursor()
#cur.execute('DROP TABLE IF EXISTS Counts')
cur.execute('''CREATE TABLE IF NOT EXISTS Counts (email TEXT, count INTEGER, amazeprofile TEXT, skill TEXT)''')
browser = webdriver.Chrome()
OpenBrowser()

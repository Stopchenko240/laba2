from csv import reader
import xml.dom.minidom as minidom
import os


def open_table():
    try:
        with open('books-en.csv', 'r') as csvfile:
            table = list(reader(csvfile, delimiter=';'))
            table = table[1:]
            return table
    except FileNotFoundError:
        print('Файл не найден!')
        return 0


def find_string(string, search_line):
    lower_case = string.lower()
    index = lower_case.find(search_line.lower())
    return index
  

def long_titles(table):
    flag = 0
    for row in table:
        if len(row[1]) > 30:
            flag += 1
    print(f'Записей с названием длиннее 30 символов: {flag}')
    input('Нажмите Enter')


def search(table):
    search_line = input('Введите автора: ')
    if search_line in ['0', '']:
        return 0

    flag = 0
    for row in table:
        if find_string(row[2], search_line) != -1:
            price = float(row[6].replace(',', '.'))
            if price <= 200:
                print(f'{row[2]} - {row[1]}, цена {row[6]} руб.')
                flag += 1

    if flag == 0:
        print('Ничего не найдено!')
    else:
        print(f'Найдено позиций: {flag}')
    input('Нажмите Enter')


def bibliography(table):
    books = table[:20]
    output = open('result.txt', 'w')
    number = 1
    for row in books:
        author = row[2].rstrip('.')
        output.write(f'{number}. {author}. {row[1]} - {row[3]}\n')
        number += 1
    output.close()
    print('Ссылки записаны в файл result.txt')
    input('Нажмите Enter')


def currency():
    try:
        xml_file = open('currency.xml', 'r', encoding='windows-1251')
    except FileNotFoundError:
        print('Файл не найден!')
        return 0

    xml_data = xml_file.read()
    dom = minidom.parseString(xml_data)
    dom.normalize()

    elements = dom.getElementsByTagName('Valute')
    currency_dict = {}

    for node in elements:
        for child in node.childNodes:
            if child.nodeType == 1:
                if child.tagName == 'NumCode':
                    if child.firstChild.nodeType == 3:
                        num_code = int(child.firstChild.data)
                if child.tagName == 'CharCode':
                    if child.firstChild.nodeType == 3:
                        char_code = child.firstChild.data
        currency_dict[num_code] = char_code

    for num_code in currency_dict:
        print(num_code, '-', currency_dict[num_code])
    
    xml_file.close()
    input('Нажмите Enter')


table = open_table()

while True:
    os.system('cls')
    if table == 0:
        break
    print('Меню:\n1 - Названия длиннее 30 символов\n2 - Поиск по автору (до 200 руб.)\n3 - Библиографические ссылки\n4 - Валюты из XML\n0 - Выход')
    menu = input('Выберите пункт меню: ')
    match menu:
        case '1':
            long_titles(table)
        case '2':
            search(table)
        case '3':
            bibliography(table)
        case '4':
            currency()
        case '0':
            break
        case _:
            print('Нет пункта меню, нажмите Enter')
            input()

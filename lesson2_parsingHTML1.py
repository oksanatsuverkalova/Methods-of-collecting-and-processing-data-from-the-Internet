from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re
from time import sleep

vacancy = input('Введите название вакансии: ')
# параметры
params = {'clusters':'true',
         'enable_snippets':'true',
          'L_save_area':'true',
          'area':1,
          'from':'cluster_area',
          'only_with_salary':'false',
          'showCluster':'true',
          'text':vacancy
          }
user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}
main_link = 'https://hh.ru/search/vacancy/advanced?customDomain=1'


response = requests.get(main_link+'/search/vacancy', headers=user_agent, params=params)
soup = bs(response.text,'html.parser')
vacancy_sh = []
# цикл по страницам
flag = True
while flag == True:

    vacancy_blok = soup.find('div',{'class':'vacancy-serp-wrapper HH-SearchVacancyDropClusters-XsHiddenOnClustersOpenItem'})
    vacancy_list = vacancy_blok.find_all('div', {'class': 'vacancy-serp-item'})

    for vacancy in vacancy_list:
        vacancy_data = {}
        vacancy_data['name'] = vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'}).getText()
        vacancy_data['link'] = vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'})['href']
        vacancy_data['vac_id'] = int((re.search(r'\d+',vacancy_data['link'] )).group())   # добавим ID вакансии
        price_blok = vacancy.find('span', {'data-qa' : 'vacancy-serp__vacancy-compensation'})

        #заполнение полей с ценой
        if (price_blok) is not None:
            price = price_blok.contents[0].replace('\xa0', '') # удалим пробелы

            result = (re.split(r'[\., ,-]', price))            #разобьем строку сразу по всем разделителям
            i = 0
            if result[i] == 'от' and result[i+1] == 'до':
                vacancy_data['min'] = result[i + 1]
                vacancy_data['max'] = result[i + 3]
                vacancy_data['cur'] = result[i + 4]
            elif result[i] == 'от':
                vacancy_data['min'] = result[i + 1]
                vacancy_data['max'] = ''
                vacancy_data['cur'] = result[i + 2]
            elif result[i] == 'до':
                vacancy_data['min'] = ''
                vacancy_data['max'] = result[i + 1]
                vacancy_data['cur'] = result[i + 2]
            else:
                vacancy_data['min'] = result[i]
                vacancy_data['max'] = result[i + 1]
                vacancy_data['cur'] = result[i + 2]
        vacancy_sh.append(vacancy_data)

    #проверим ессть ли следующая страница
    button_next = vacancy_blok.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})
    #если страница есть, получим ссылку и выполним снова get запрос
    if button_next is not None:
        button_next = vacancy_blok.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})['href']
        response = requests.get(main_link + button_next, headers=user_agent)
        soup = bs(response.text, 'html.parser')
        flag = True
    #если следующей страницы нет, то выходим из цикла
    else:
        flag = False
pprint(vacancy_sh)
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re


hh_f = dict()
hh_f['vacancies'] = ['div', {'class': 'vacancy-serp-item'}]
hh_f['vacancy_tag'] = ['a', {'class': 'bloko-link'}]
hh_f['salary'] = ['span', {'data-qa': 'vacancy-serp__vacancy-compensation'}]
hh_f['employer'] = ['a', {'data-qa': 'vacancy-serp__vacancy-employer'}]
hh_f['address'] = ['span', {'data-qa': 'vacancy-serp__vacancy-address'}]
hh_f['pager_next'] = ['a', {'data-qa': 'pager-next'}]


superjob_f = dict()
superjob_f['vacancies'] = ['div', {'class': 'f-test-vacancy-item'}]
superjob_f['vacancy_tag'] = ['a', {'class': ['icMQ_','_6AfZ9']}]
superjob_f['salary'] = ['span', {'class': '_1OuF_ _1qw9T f-test-text-company-item-salary'}]
superjob_f['employer'] = ['span', {'class': '_1h3Zg _3Fsn4 f-test-text-vacancy-item-company-name e5P5i _2hCDz _2ZsgW _2SvHc'}]
superjob_f['address'] = ['span', {'class': '_1h3Zg f-test-text-company-item-location e5P5i _2hCDz _2ZsgW'}]
superjob_f['pager_next'] = ['a', {'class': 'icMQ_ bs_sM _3ze9n f-test-button-dalshe f-test-link-Dalshe'}]


def salary_processing(vacancy_dict, vacancy, tags_f):
    try:
        salary = vacancy.find(*tags_f['salary'])
        salary = salary.text

        if salary == 'По договорённости':
            return

        salary = str.replace(salary, '\u202f', '')
        salary = re.sub('(?<=\d)\xa0(?=\d)', '', salary)
        salary_split_list = salary.split()

        try:
            if salary_split_list[0] == 'от':
                vacancy_dict['min_salary'] = salary_split_list[1]
            elif salary_split_list[0] == 'до':
                vacancy_dict['max_salary'] = salary_split_list[1]
            else:
                vacancy_dict['min_salary'] = salary_split_list[0]
                vacancy_dict['max_salary'] = salary_split_list[2]
        except:
            pass

        vacancy_dict['valute'] = salary_split_list[-1]
    except AttributeError:
        pass


def vacancy_processing(vacancy, source, tags_f):
    vacancy_dict = dict()
    vacancy_dict['source'] = source

    vacancy_tag = vacancy.find(*tags_f['vacancy_tag'])
    vacancy_dict['name'] = vacancy_tag.text
    vacancy_dict['url'] = vacancy_tag.get('href')
    vacancy_dict['url'] = vacancy_dict['url'][:str.find(vacancy_dict['url'], '?')]

    salary_processing(vacancy_dict, vacancy, tags_f)

    try:
        employer = vacancy.find(*tags_f['employer']).text
        vacancy_dict['employer'] = str.replace(employer, '\xa0', ' ')
    except AttributeError:
        pass

    try:
        vacancy_dict['address'] = vacancy.find(*tags_f['address']).text
    except AttributeError:
        pass

    return vacancy_dict


def get_vacancies_list_2(input_word, main_url, url_next, tags_f):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    pager_next = url_next + input_word
    vacancies_list = []

    for i in range(1):
        url = main_url + pager_next
        print(url)
        response = requests.get(url, headers=headers)
        dom = bs(response.text, 'html.parser')
        vacancies = dom.find_all(*tags_f['vacancies'])

        for vacancy in vacancies:
            vacancy_dict = vacancy_processing(vacancy, source=main_url, tags_f=tags_f)
            vacancies_list.append(vacancy_dict)

        try:
            pager_next = dom.find(*tags_f['pager_next']).get('href')
        except AttributeError:
            pass

    return vacancies_list


def get_vacancies_list(input_word):
    main_url = "https://hh.ru"
    url_next = "/search/vacancy?text="
    vacancies_list_hh = get_vacancies_list_2(input_word, main_url, url_next, hh_f)

    main_url = "https://www.superjob.ru"
    url_next = "/vacancy/search/?keywords="
    vacancies_list_superjob = get_vacancies_list_2(input_word, main_url, url_next, superjob_f)

    return vacancies_list_hh + vacancies_list_superjob


vacancies_list = get_vacancies_list("python")
df = pd.DataFrame(vacancies_list)
print(df)
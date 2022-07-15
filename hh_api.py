import json
import datetime
import requests
from operator import itemgetter


url_api = 'https://api.hh.ru/'
url_vacancy = f'{url_api}vacancies'
# url_areas = f'{url_api}areas'
# pprint.pprint(requests.get(url_areas).json())
search_line = input('Введите название вакансии для поиска: ')
# search_line = 'python developer'
params = {
    'text': search_line,
    'area': 1,
    'page': 0
}
result_vacancy = requests.get(url_vacancy, params=params).json()
items_vacancy = result_vacancy['items']
all_skills = []
summ_salary = 0
count_salary = 0
for item_vacancy in items_vacancy:
    result_url_vacancy = requests.get(item_vacancy['url']).json()

    if result_url_vacancy['salary'] != None:
        if result_url_vacancy['salary']['from'] != None:
            summ_salary += result_url_vacancy['salary']['from']
            count_salary += 1

    result_skill_url_vacancy = result_url_vacancy['key_skills']
    for index in range(len(result_skill_url_vacancy)):
        all_skills.append(result_skill_url_vacancy[index]['name'])

statistics_skill_dict = {}
all_skills = sorted(all_skills)
unique_skill = sorted(list(set(all_skills)))
print(result_vacancy['found'], 'вакансий')
statistics_skill_dict.update({'found_vacancy': result_vacancy['found']})
print('Средний начальный уровень з/п:', summ_salary//count_salary)
statistics_skill_dict.update({'average_salary': summ_salary//count_salary})
print('Требования:', end=' ')
statistics_skill = []
all_skills_count = len(all_skills)
i = 0
for skill in unique_skill:
    print(skill, end='') if i == 0 else print(', ', skill, end='')
    skill_count = all_skills.count(skill)
    statistics_skill.append([skill, skill_count, round(skill_count/all_skills_count*100, 2)])
    i = 1

statistics_skill = sorted(statistics_skill, key=itemgetter(1), reverse=True)
print('\n')

for skill in statistics_skill:
    print(skill[0], ': ', skill[1], ' (', skill[2], '%)', sep='')
    statistics_skill_dict.update({skill[0]: [skill[1], skill[2]]})

result = json.dumps(statistics_skill_dict)
file_name = search_line + ' ' + str(datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")) + '.json'
with open(file_name, 'w') as f:
    json.dump(result, f)


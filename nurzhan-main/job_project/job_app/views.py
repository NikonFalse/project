import os
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.messages.context_processors import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
import requests
import json
from django.views.generic import CreateView
from .models import JobInformation
import csv
import itertools


def sign_in(request):
    if request.method == 'GET':
        return render(request, 'sign-in.html')
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('main-page')
    messages.warning(request, 'Неверный логин или пароль')
    return render(request, 'sign-in.html')

class SignUp(CreateView):
    success_url = ('/sign-in/')
    form_class = UserCreationForm
    template_name = "sign-up.html"

def main_page(request):
    return render(request, 'main-page.html')


def demand_page(request):
    model = JobInformation.objects.all()
    information = {}
    vacancies_information = {}
    python_information = {}
    python_vacancies_information = {}
    for m in model:
        count = 0
        if m.year not in information.keys():
            years = JobInformation.objects.filter(year=m.year)
            salary = 0
            for year in years:
                salary += year.salary
                count += 1
            salary //= len(years)
            information[m.year] = salary
            vacancies_information[m.year] = count

    for m in model.filter(name__icontains='Python'):
        count = 0
        if m.year not in python_information.keys():
            years = JobInformation.objects.filter(year=m.year, name__icontains='Python')
            salary = 0
            for year in years:
                salary += year.salary
                count += 1
            salary //= len(years)
            python_information[m.year] = salary
            python_vacancies_information[m.year] = count
    context = {
        'information': information,
        'vacancies_information': vacancies_information,
        'python_information': python_information,
        'python_vacancies_information': python_vacancies_information
    }
    return render(request, 'demand.html', context)


def skills_page(request):
    skills = {}
    skills_storage = []
    model = JobInformation.objects.exclude(skills='')
    for m in model:
        formated_data = ' '.join((m.skills.split(' '))).split('\n')
        for skill in formated_data:
            skills_storage.append(skill)
    for skill in skills_storage:
        if skill not in skills.keys():
            skills[skill] = 1
        elif skill in skills.keys():
            skills[skill] += 1
    skills_formated = sorted(skills.items(), key=lambda x: x[1], reverse=True)
    context = {
        'skills': dict(skills_formated[:10])
    }
    return render(request, 'skills.html', context)


def geography_page(request):
    model = JobInformation.objects.all()
    city_salaries = {}
    city_vacancies = {}
    for m in model:
        count = 0
        if m.city not in city_salaries.keys():
            city_salaries[m.city] = 0
            city_vacancies[m.city] = 0
        else:
            city_salaries[m.city] += m.salary
            city_vacancies[m.city] += 1
    for key, salary in city_salaries.items():
        try:
            city_salaries[key] = (salary // city_vacancies[key])
        except:
            city_salaries[key] = 0
    city_salaries_formated=(dict(itertools.islice(city_salaries.items(), 0 ,14)))
    city_salaries = sorted(city_salaries_formated.items(), key=lambda x: x[1], reverse=True)

    city_vacancies_sorted =sorted(city_vacancies.items(), key=lambda x: x[1], reverse=True)
    context = {
        'city_salaries': dict(city_salaries),
        'city_vacancies': dict(city_vacancies_sorted[:15])
    }
    return render(request, 'geography.html', context)


def get_vacancies(request):
    req = requests.get('https://api.hh.ru/vacancies?text=python программист&date_from=2022-12-01&date_to=2022-12-31')
    data = req.content.decode()
    req.close()
    raw_vacancies = json.loads(data)
    vacancies = []
    for vacancy in list(raw_vacancies['items'])[:11]:
        vacancy_req = requests.get(vacancy['url'])
        vacancy_data = vacancy_req.content.decode()
        vacancy_req.close()
        vacancy_object = json.loads(vacancy_data)
        vacancy_object['created_at'] = vacancy_object['created_at'][:10]
        vacancy_object['created_at'] = datetime.strptime(vacancy_object['created_at'], "%Y-%m-%d")
        vacancies.append(vacancy_object)
    context = {
        'vacancies': vacancies
    }
    return render(request, 'vacancies.html', context=context)

# Парсер
# path = os.path.join(os.path.dirname(__file__), 'vacancies_with_skills.csv')
# with open(path, encoding='utf-8') as r_file:
#     file_reader = csv.reader(r_file, delimiter=",")
#     next(file_reader)
#     for row in file_reader:
#         if {row[3]} == {''} or {row[4]} == {'USD'}:
#             continue
#         name = row[0]
#         skill = row[1]
#         salary = int(float(row[3]))
#         city = row[5]
#         year = row[6][:4]
#         JobInformation.objects.create(name=name,skills=skill,salary=salary,city=city,year=year)

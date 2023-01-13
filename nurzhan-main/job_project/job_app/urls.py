from django.urls import path
from .views import main_page, sign_in, get_vacancies, demand_page, geography_page, skills_page,SignUp

urlpatterns = [
    path('', main_page, name='main-page'),
    path('sign-in/', sign_in, name='sign-in'),
    path('vacancies/', get_vacancies, name='vacancies'),
    path('demand/', demand_page, name='demand'),
    path('geography/', geography_page, name='geography'),
    path('skills/', skills_page, name='skills'),
    path('sign-up/',SignUp.as_view(),name='sign-up')
]

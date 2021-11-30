from django.urls import path
from . import views

app_name = 'student_grade'

urlpatterns = [
    path('', views.accuracy_analysis, name="accuracy_analysis"),
    path('error/', views.error_analysis, name="error_analysis"),
    path('lang/', views.translation_page, name='trans_func')
]


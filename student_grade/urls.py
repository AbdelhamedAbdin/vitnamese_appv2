from django.urls import path
from . import views
from django.contrib import admin

app_name = 'student_grade'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.accuracy_analysis, name="accuracy_analysis"),
    path('error/', views.error_analysis, name="error_analysis"),
    path('lang/', views.translation_page, name='trans_func')
]


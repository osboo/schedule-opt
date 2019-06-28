from django.urls import path
from . import views

urlpatterns = [
    path('sheduleForTeacher', views.sheduleForTeacher, name='sheduleForTeacher'),
    path('sheduleForGroup', views.sheduleForGroup, name='sheduleForGroup'),
    path('shedule', views.shedule, name='shedule'),
    path('mainPage', views.mainPage, name='mainPage'),
    path('teacherWishes', views.teacherWishes, name='teacherWishes'),
]

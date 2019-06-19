from django.contrib import admin
from schedules.models import Teacher, Day, Group, LessonType, Room, Schedule, TeacherSubject, TimeTable, TypedSubject
# Register your models here.

imported_models = (Teacher, Day, Group, LessonType, Room, Schedule, TeacherSubject, TimeTable, TypedSubject)
for m in imported_models:
    admin.site.register(m)
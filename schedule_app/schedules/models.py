from django.db import models


# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=200)
    number_of_students = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class LessonType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class TypedSubject(models.Model):
    name = models.CharField(max_length=200)
    lesson_type = models.ForeignKey(LessonType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=200)
    worker_id = models.IntegerField(default=0)
    hours_payload = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class TimeTable(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class Day(models.Model):
    id = 0
    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)


class Room(models.Model):
    building_id = models.IntegerField(default=0)
    room_type = models.ForeignKey(LessonType, on_delete=models.CASCADE)


class TeacherSubject(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(TypedSubject, on_delete=models.CASCADE)


class Schedule(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    typed_subject = models.ForeignKey(TypedSubject, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    time = models.ForeignKey(TimeTable, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

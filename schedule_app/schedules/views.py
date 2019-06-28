from django.shortcuts import render

# Create your views here.
def sheduleForTeacher(request):
    return render(request, 'shedules/sheduleForTeacher.html', {})
def sheduleForGroup(request):
    return render(request, 'shedules/sheduleForGroup.html', {})
def shedule(request):
    return render(request, 'shedules/shedule.html', {})
def mainPage(request):
    return render(request, 'shedules/mainPage.html', {})
def teacherWishes(request):
    return render(request, 'shedules/teacherWishes.html', {})
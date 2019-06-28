from .models import Teacher
from .models import Group
from .models import TeacherSubject
from .models import TypedSubject
from .models import Day
from .models import TimeTable
from .models import LessonType

import itertools

import itertools
from pulp import *
problem = LpProblem("schedule-opt", LpMaximize)
from faker import Faker
fake = Faker()
from collections import namedtuple

N_l = 20  # number of teachers
N_g = 20  # number of groups
N_s = 20  # number of courses
N_d = 12  # number of days
N_t = 8  # number of times per day
L = [fake.name() for _ in range(N_l)]
G = "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,z,y,z"[0:2 * N_g].split(',')[:-1]
types = ['lection', 'lab', 'practice']
subjs = [fake.job().replace(',', '')[0:15] for _ in range(N_s)]
D = "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,z,y,z"[0:2 * N_d].split(',')[:-1]
T = "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,z,y,z"[0:2 * N_t].split(',')[:-1]

def get_all_sp_keys(L, G, types, subjs, D, T):
    return itertools.product(L, G, types, subjs, D, T)

def get_all_gdt_keys(GG, DD, TT):
    return itertools.product(GG, DD, TT)


def get_all_ldt_keys(LL, DD, TT):
    return itertools.product(LL, DD, TT)


SP = LpVariable.dicts("SP", get_all_sp_keys(L, G, types, subjs, D, T), 0, 1, cat=pulp.LpInteger)
Ig = LpVariable.dicts("Ig", get_all_gdt_keys(G, D, T[:-1]), -1, 1, cat=pulp.LpInteger)
Il = LpVariable.dicts("Il", get_all_ldt_keys(L, D, T[:-1]), -1, 1, cat=pulp.LpInteger)
one = LpVariable("one", 1, 1, cat=pulp.LpInteger)
zero = LpVariable("zero", 0, 0, cat=pulp.LpInteger)


def get_x_by_gdt(g, d, t, SP):
    s = lpSum([SP[key] for key in itertools.product(L, [g], types, subjs, [d], [t])])
    return s


def get_x_by_ldt(l, d, t, SP):
    s = lpSum([SP[key] for key in itertools.product([l], G, types, subjs, [d], [t])])
    return s


def get_x_by_ldt(l, d, t, SP):
    s = lpSum([SP[key] for key in itertools.product([l], G, types, subjs, [d], [t])])
    return s


def sum_x_by_g(g, SP):
    sum = lpSum([SP[key] for key in itertools.product(L, [g], types, subjs, D, T)])
    return sum


def sum_x_by_l(l, SP):
    sum = lpSum([SP[key] for key in itertools.product([l], G, types, subjs, D, T)])
    return sum


alpha = 1.0
beta = 1.0
gamma = 1.0


def get_c(key):
    return 1.0

#Problem
all_lectures = [alpha * get_c(key) * SP[key] for key in get_all_sp_keys(L, G, types, subjs, D, T)]
all_groups_no_gaps = [beta * Ig[key] for key in get_all_gdt_keys(G, D, T[:-1])]
all_teachers_no_gaps = [gamma * Il[key] for key in get_all_ldt_keys(L, D, T[:-1])]
all_lectures + all_groups_no_gaps + all_teachers_no_gaps
problem += lpSum(all_lectures + all_groups_no_gaps + all_teachers_no_gaps)
#Constraints
#Minimize gaps between lessons for teacher
def next_letter(symbol):
    return T[(T.index(symbol) + 1) % len(T)]

for (teacher, day, time) in itertools.product(L, D, T[:-1]):
    # problem += get_x_by_ldt(teacher, day, time, SP) + get_x_by_ldt(teacher, day, time + 1, SP) -1 >= Il[teacher, day, time]
    problem += get_x_by_ldt(teacher, day, time, SP) + get_x_by_ldt(teacher, day, next_letter(time), SP) - Il[
        teacher, day, time] >= 1
#Minimize gaps between lessons for group

for (group, day, time) in itertools.product(G, D, T[:-1]):
    # problem += get_x_by_gdt(group, day, time, SP) + get_x_by_gdt(group, day, time + 1, SP) -1 >= Ig[group, day, time]
    problem += get_x_by_gdt(group, day, time, SP) + get_x_by_gdt(group, day, next_letter(time), SP) - Ig[
        group, day, time] >= 1
#with open('problem.txt', 'w') as f: print(problem, file=f)

#Amount of lessons for group must be no more than payload in plan
for g in G:
    problem += sum_x_by_g(g, SP) <= len(D) * 3
#Amount of lessons for teacher must be no more than payload in plan
for teacher in L:
    problem += sum_x_by_l(teacher, SP) <= len(D) * 3

#One lesson per time slot for one group
def sum_x_for_group_at_dt(g, d, t, SP):
    s = 0
    for key in itertools.product(L, [g], types, subjs, [d], [t]):
        s += SP[key]
    return s

for key in get_all_gdt_keys(G, D, T):
    s = sum_x_for_group_at_dt(*key, SP)
    problem += s <= 1
    problem += s >= 0
#One lesson per time slot for one teacher
def sum_x_for_teacher_at_dt(l, d, t, SP):
    s = 0
    for key in itertools.product([l], G, types, subjs, [d], [t]):
        s += SP[key]
        return s
for key in get_all_ldt_keys(L, D, T):
    s = sum_x_for_teacher_at_dt(*key, SP)
    problem += s <= 1
    problem += s >= 0
#No more than 3 lessons for one group per day

def sum_x_for_group_per_day(g, d, SP):
    s = 0
    for key in itertools.product(L, [g], types, subjs, [d], T):
        s += SP[key]
    return s


for (group, day) in itertools.product(G, D):
    problem += sum_x_for_group_per_day(group, day, SP) <= 3

#No more than 4 lessons for one teacher per day
def sum_x_for_teacher_per_day(l, d, SP):
    s = 0
    for key in itertools.product([l], G, types, subjs, [d], T):
        s += SP[key]
    return s
for (teacher, day) in itertools.product(L, D):
    problem += sum_x_for_teacher_per_day(teacher, day, SP) <= 4

#No more than 2 lessons of one subject for group per day
def sum_x_of_same_subject_for_group_per_day(g, d, subj, SP):
    s = 0
    for key in itertools.product(L, [g], types, [subj], [d], T):
        s += SP[key]
    return s

for (group, day, subj) in itertools.product(G, D, subjs):
    problem += sum_x_of_same_subject_for_group_per_day(group, day, subj, SP) <= 2#Solution
#need to fix it problem.solve(solver=pulp.glpk(options=['--log', 'lessons.log']))
# problem.solve(solver=solvers.GLPK(options=['--log', 'lessons.log', '--wmps', 'lessons.mps', '--check']))

def print_solution(problem):
    print("Status:", LpStatus[problem.status])
    for v in problem.variables():
        if (v.varValue > 0.0):
            print(v.name, "=", v.varValue)
            # print("Total Cost =", pulp.value(problem.objective))


print_solution(problem)
print(value(problem.objective))
#Match lessons to rooms
TheSix = namedtuple('TheSix', ['teacher', 'group', 'lesson_type', 'subject', 'day', 'time'])

def get_tuple(v):
    # SP_('Shane_Gordon',_0,_'lab',_'Paramedic',_0,_'b')
    x = v.name.split(',_')  # ["SP_('Shane_Gordon'", '0', "'lab'", "'Paramedic'", '0', "'b')"]
    start = "'"
    end = "'"
    return TheSix(*list(map(lambda s: s[s.find(start) + len(start):s.rfind(end)].replace('_', ' '), x)))

def extract_optimal_solution(problem):
    optimals = [get_tuple(v) for v in problem.variables() if v.varValue > 0.0 and v.name.startswith('SP')]
    return optimals

N_r = 26
R = "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,z,y,z"[0:2 * N_r].split(',')[:-1]

#TypedRoom
TypedRoom = namedtuple('TypedRoom', ['room', 'type'])
lection_rooms_number = 3
lab_rooms_number = 3
practice_rooms_number = 3
lections_rooms = list(map(lambda room: TypedRoom(room=room, type='lection'), R[0:lection_rooms_number]))
lab_rooms = list(
    map(lambda room: TypedRoom(room=room, type='lab'), R[lection_rooms_number:lection_rooms_number + lab_rooms_number]))
practice_rooms = list(map(lambda room: TypedRoom(room=room, type='practice'), R[
                                                                              lection_rooms_number + lab_rooms_number: lection_rooms_number + lab_rooms_number + practice_rooms_number]))
available_rooms = lections_rooms + lab_rooms + practice_rooms
lessons = extract_optimal_solution(problem)
problem_match = LpProblem("match-to-rooms", LpMaximize)
Z = LpVariable.dicts("Z", list(
    map(lambda pair: (tuple(pair[0]), tuple(pair[1])), itertools.product(lessons, available_rooms))), 0, 1,
                     cat=pulp.LpInteger)
#Rooms have priorities for appropriate lessons
priority = {
    'lection': {'lection': 1.0},
    'lection': {'practice': 0.5},
    'lection': {'lab': 0.0},

    'practice': {'lection': 0.0},
    'practice': {'practice': 1.0},
    'practice': {'lab': 0.0},

    'lab': {'lection': 0.0},
    'lab': {'practice': 0.5},
    'lab': {'lab': 1.0},
}  # from room type to lesson type


def get_c(key):
    return priority[key[1].type][key[0].lesson_type]


problem_match += lpSum([get_c(key) * Z[(key[0], key[1])] for key in itertools.product(lessons, available_rooms)])


def get_z_by_lesson(lesson, Z):
    s = lpSum([Z[(key[0], key[1])] for key in itertools.product([lesson], available_rooms)])
    return s

def get_lessons_by_day_time(d, t, lessons):
    return list(filter(lambda lesson: lesson.day == d and lesson.time == t, lessons))


def get_z_by_day_time(d, t, Z):
    lessons_at_moment = get_lessons_by_day_time(d, t, lessons)
    if len(lessons_at_moment) > 0:
        return lpSum([Z[(key[0], key[1])] for key in itertools.product(lessons_at_moment, available_rooms)])
    return None


for (d, t) in itertools.product(D, T):
    contraint = get_z_by_day_time(d, t, Z)
    if contraint:
        problem_match += contraint <= 1
for lesson in lessons:
    problem_match += get_z_by_lesson(lesson, Z) == 1
#Solution
#need to fix it with open('problem_match.txt', 'w') as f:
    #need to fix it print(problem_match, file=f)
#need to fix it problem_match.solve(solver=solvers.GLPK(options=['--log', 'match.log', '--wmps', 'match.mps']))
print(value(problem_match.objective))
print_solution(problem_match)

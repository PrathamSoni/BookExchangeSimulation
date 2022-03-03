import random
from scipy.stats import binom

from classes import *
from collections import Counter

total_undergrads = 6366


class Student:
    def __init__(self, id):
        self.id = id
        self.classes = []
        self.past_classes = []
        self.units = 0

    def move_quarter(self):
        self.past_classes.extend(self.classes)
        self.delete_quarter()

    def delete_quarter(self):
        self.classes = []
        self.units = 0

    def __str__(self):
        return f"student {self.id}, units {self.units}, classes: {[str(c) for c in self.classes]}"


def get_class_without_full(classes):
    out = [c for c in classes if c.capacity > 0]
    # print(out)
    random.shuffle(out)
    # out.sort(key=lambda x:x.units)
    return out


def get_remaining_students(students):
    out = [student for student in students if student.units < 12]
    random.shuffle(out)
    # out.sort(key=lambda x:x.units)
    return out


def get_nonfull_students(students, units):
    out = [student for student in students if student.units + units < 23]
    random.shuffle(out)
    # out.sort(key=lambda x:x.units)
    return out


def make_students(stop):
    students = []
    for i in range(total_undergrads):
        students.append(Student(i))

    q = 0
    for year in range(4):
        quarters = get_quarters()

        for q_idx, quarter in enumerate(quarters):
            q += 1
            early_stop = False
            while not early_stop:
                r_students = get_remaining_students(students)
                if len(r_students) == 0:
                    break

                for student in r_students:
                    try:
                        c = get_class_without_full(quarter)[0]
                        c.capacity -= 1
                        c.students.add(student)
                        student.classes.append(c)
                        student.units += c.units
                    except:
                        early_stop = True

            while True:
                r_classes = get_class_without_full(quarter)
                if len(r_classes) == 0:
                    break

                for c in r_classes:
                    r_students = get_nonfull_students(students, c.units)
                    for i in range(c.capacity):
                        student = r_students[i]
                        student.classes.append(c)
                        student.units += c.units
                        c.capacity -= 1
                        c.students.add(student)

            for student in students[:(year + 1) * total_undergrads // 4]:
                student.move_quarter()
            for student in students[(year + 1) * total_undergrads // 4:]:
                student.delete_quarter()

            if year == 3 and q_idx == stop:
                break

    return students


# students = make_students(0)
# print(sorted(Counter([len(s.past_classes + s.classes) for s in students]).items()))
# students = make_students(1)
# print(sorted(Counter([len(s.past_classes + s.classes) for s in students]).items()))
# students = make_students(2)
# print(sorted(Counter([len(s.past_classes + s.classes) for s in students]).items()))
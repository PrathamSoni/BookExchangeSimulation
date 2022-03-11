from classes import *

total_undergrads = 6366


class Student:
    def __init__(self, id):
        self.id = id
        self.classes = []
        self.past_classes = []
        self.units = 0
        self.alpha = 0
        self.donated = 0
        self.received = 0

    def move_quarter(self):
        self.past_classes.extend(self.classes)
        self.delete_quarter()

    def delete_quarter(self):
        self.classes = []
        self.units = 0

    def __str__(self):
        return f"student {self.id}, units {self.units}, classes: {[str(c) for c in self.classes]}"


def get_class_without_full(classes):
    out = [c for c in classes if c.temp_capacity > 0]
    random.shuffle(out)
    return out


def get_remaining_students(students):
    out = [student for student in students if student.units < 12]
    random.shuffle(out)
    return out


def get_nonfull_students(students, units):
    out = [student for student in students if student.units + units < 23]
    random.shuffle(out)
    return out


def make_students(stop):
    students = []
    for i in range(total_undergrads):
        students.append(Student(i))

    q = 0
    quarters = get_quarters()
    for year in range(4):
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
                        c.temp_capacity -= 1
                        c.students.append(student)
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
                    for i in range(c.temp_capacity):
                        student = r_students[i]
                        student.classes.append(c)
                        student.units += c.units
                        c.temp_capacity -= 1
                        c.students.append(student)

            if year == 3 and q_idx == stop:
                break

            for student in students[:(year + 1) * total_undergrads // 4]:
                student.move_quarter()
            for student in students[(year + 1) * total_undergrads // 4:]:
                student.delete_quarter()

            for c in quarter:
                c.clear()

    for i in range(total_undergrads):
        students[i].alpha = random.randint(0, len(students[i].past_classes))

    return students, quarter

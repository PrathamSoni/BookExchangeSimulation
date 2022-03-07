import random
from scipy.stats import binom
from collections import Counter


class Class:
    def __init__(self, id, capacity, units):
        self.id = id
        self.capacity = capacity
        self.temp_capacity = self.capacity
        self.units = units
        self.students = []
        self.prior_students = []

    def __str__(self):
        return f"class {self.id}, capacity {self.capacity}"

    def clear(self):
        self.temp_capacity = self.capacity
        self.prior_students.extend(self.students)
        self.students = []


def make_distrib():
    distribution = []
    for i in range(477):
        distribution.append(random.randint(5, 9))

    for i in range(463):
        distribution.append(random.randint(10, 19))

    for i in range(143):
        distribution.append(random.randint(20, 29))

    for i in range(76):
        distribution.append(random.randint(30, 39))

    for i in range(50):
        distribution.append(random.randint(40, 49))

    for i in range(100):
        distribution.append(random.randint(50, 99))

    for i in range(68):
        distribution.append(random.randint(100, 800))

    random.shuffle(distribution)
    return distribution


def make_classes():
    distrib = make_distrib()
    ret = []
    units = []
    for i, cap in enumerate(distrib):
        while True:
            unit = binom.rvs(10, .5)
            if unit <= 3:
                break
        unit += 2

        units.append(unit * cap)
        ret.append(Class(i, cap, unit))
    return ret


def get_quarters():
    classes = make_classes()
    n = len(classes)
    return classes[:n // 3], classes[n // 3: 2 * n // 3], classes[2 * n // 3:]

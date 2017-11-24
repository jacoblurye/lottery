"""Implements the Lottery class.
"""

from random import randint

from course import Course
from student import Student

class Lottery(object):
    """
        Assigns students to courses.
    """
    def __init__(self, n_courses, n_students, min_cap=12, max_cap=50):
        """
            Create a new lottery.

            params
            ------
            n_courses: int
                The number of courses in the lottery.
            min_cap  : int, default 12
                The lowest allowed enrollment cap.
            max_cap  : int, default 50
                The highest allowed enrollment cap.
        """
        self.n_courses = n_courses
        self.n_students = n_students
        self.min_cap = min_cap
        self.max_cap = max_cap

        self.courses = []
        self._init_courses()

        self.students = []
        self._init_students()

    def _init_courses(self):
        make_new_course = lambda: Course(randint(self.min_cap, self.max_cap))
        self.courses = [make_new_course() for _ in xrange(self.n_courses)]

    def _init_students(self):
        make_new_student = lambda: Student(randint(1, 4), self.n_courses)
        self.students = [make_new_student() for _ in xrange(self.n_students)]

    def run(self):
        """
            Return an allocation of students to courses.
        """
        raise AssertionError("Lottery.run not implemented")


class EfficientLottery(Lottery):
    """
        An impossible mechanism that allocates according to student's true preferences.
        Used as a point of comparison to possible course assignment mechanisms.
    """
    
    def run(self):
        pass



class RandomLottery(Lottery):
    """
        Simplified model of current Harvard lottery system.
        Students apply to 
    """

    def run(self):
        pass


class SignallingLottery(Lottery):
    pass

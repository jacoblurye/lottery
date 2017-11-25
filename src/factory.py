"""Factory for generating students and courses.
"""

from random import randint, seed

from student import Student 
from course import Course

class Factory(object):
    """
        Generate a set of students and courses based on certain parameters.
    """
    def __init__(self, n_courses, n_students, min_cap, max_cap):
        """
            params
            ------
            n_courses: int
                The number of courses in the catalog.
            n_students: int
                The number of students in the college.
            min_cap  : int
                The lowest allowed enrollment cap.
            max_cap  : int
                The highest allowed enrollment cap.
        """
        self.n_courses = n_courses
        self.n_students = n_students
        self.min_cap = min_cap
        self.max_cap = max_cap

    def generate(self, seed_int=None):
        """
            Generate course catalog and students with requested preferences.
        """
        if seed_int:
            seed(seed_int)
        courses = self._init_courses()
        students = self._init_students()
        return courses, students

    def _init_courses(self):
        make_new_course = lambda n: Course(n, randint(self.min_cap, self.max_cap))
        return [make_new_course(i) for i in xrange(self.n_courses)]

    def _init_students(self):
        make_new_student = lambda: Student(randint(1, 4), self.n_courses)
        return [make_new_student() for _ in xrange(self.n_students)]

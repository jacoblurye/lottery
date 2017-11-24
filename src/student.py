"""Implements the student class
"""

from random import random, randint, sample

class Student(object):
    """
        A student with course preferences.
    """

    def __init__(self, year, n_courses):
        """
            params
            ------
            year : int
                1, 2, 3, or 4.
            n_courses : int 
                Number of courses to choose from.
        """
        self.year = year
        self.preferences = {}
        self._init_preferences(n_courses)

    def _init_preferences(self, n_courses):
        """

            Initialize students' preferences over between 2 and 6 courses.

            params
            ------
            n_courses : int
                The number of courses to choose from.
        """

        n_apply = randint(2, 6)
        lottery_courses = sample(range(n_courses), n_apply)

        # Students' preferences are distributed Unif(0, year)
        # i.e., for sophomores, we have Unif(0, 2)
        for course in lottery_courses:
            self.preferences[course] = random() * self.year

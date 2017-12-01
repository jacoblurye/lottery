"""Implements the student class
"""

from random import random, randint, sample
from collections import defaultdict

from numpy.random import normal

import constants as const

class Student(object):
    """
        A student with course preferences.
    """

    def __init__(self, year, courses, noise=1):
        """
            params
            ------
            year : int
                1, 2, 3, or 4.
            courses : list[Course]
                List of courses to choose from.
        """
        self.year = year
        self.noise = noise
        self.courses = courses

        # Randomly choose subjects to be interested in
        self.subjects = set(
            sample(const.SUBJECTS, randint(const.MIN_SUBJECTS, const.MAX_SUBJECTS))
        )

        self.preferences = []
        self._init_preferences()

        self.offered_courses = set()
        self.enrolled_courses = set()
        self.top_2 = set()

    def _init_preferences(self):
        """
            Initialize students' preferences over the given courses.

            params
            ------
            n_courses : int
                The number of courses to choose from.
        """
        for course in self.courses:
            # If student is interested in course's subject
            if course.subject in self.subjects:
                # Student's value is normally distributed around course quality
                value = course.quality + normal(scale=self.noise)
                # Only lottery for courses with positive value
                if value >= 0:
                    self.preferences.append((course, value))

        # Sort courses by highest preference
        self.preferences.sort(key=lambda c: c[1], reverse=True)

        self.top_2 = set(self.preferences[:2])

    def get_tradable_courses(self):
        """
            Get all course slots the student is willing to trade.
            If this returns an empty list, the student exits the market.
        """
        # Enroll in any offered courses that are top-preferred
        while (self.preferences
               and len(self.enrolled_courses) < const.MAX_COURSES
               and self.preferences[-1] in self.offered_courses):
            self.enrolled_courses.add(self.preferences[-1])
            self.offered_courses.remove(self.preferences[-1])
            self.pop_top_preference()

        # Return any remaining courses
        return self.offered_courses

    def top_preference(self):
        """
            Get student's top preferred course that they haven't been offered. 
            (For use by TTC)
        """
        # Preferences exhausted -- student will exit the market
        if not self.preferences:
            return None

        return self.preferences[-1]

    def pop_top_preference(self):
        """
            Remove student's top preference course.
        """
        self.preferences.pop()

    def offer_spot(self, course):
        """
            How a Course offers a spot to a Student.
        """
        self.offered_courses.add(course)

    def remove_spot(self, course):
        """
            Remove a Course spot offer.
        """
        self.offered_courses.remove(course)

    def get_studycard(self):
        """
            Enroll in up to 4 most valuable offered courses.
        """
        accepts = self.preferences[0:const.MAX_COURSES]
        return accepts

    def get_studycard_value(self):
        """
            Return total utility of study card to student.
        """
        studycard = self.get_studycard()
        return sum([self.preferences[c] for c in studycard])

    def get_token(self, course):
        """
            Return true if the course is one of the student's top 2.
        """
        return course in self.top_2

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

    def __init__(self, year, courses, noise=const.NOISE):
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

        self.interested = set()
        self.preferences = []
        self.preference_dict = {}
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
                    self.interested.add(course)
                    self.preferences.append((course, value))

        # Sort courses by highest preference
        self.preferences.sort(key=lambda c: c[1])

        self.preference_dict = defaultdict(int, dict(self.preferences))
        self.top_2 = set(self.preferences[-2:])

    def get_tradable_courses(self):
        """
            Get all course slots the student is willing to trade.
            If this returns an empty list, the student exits the market.
        """

        # Enroll in any offered courses that are top-preferred
        while (self.preferences
               and self.has_room()
               and self.preferences[-1][0] in self.offered_courses):
            self.enrolled_courses.add(self.preferences[-1][0])
            self.offered_courses.remove(self.preferences[-1][0])
            self.preferences.pop()

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

        return self.preferences[-1][0]

    def offer_spot(self, course):
        """
            How a Course offers a spot to a Student.
        """
        self.offered_courses.add(course)

    def get_studycard(self):
        """
            View MAX_COURSES most valuable offered courses.
        """
        all_courses = list(self.offered_courses.union(self.enrolled_courses))
        all_courses.sort(key=lambda c: self.preference_dict[c], reverse=True)
        accepts = list(all_courses)[0:const.MAX_COURSES]
        return accepts

    def get_studycard_destructive(self):
        """
            Enroll in up to MAX_COURSES most valuable courses, 
            and permanently remove self from the other course lists.
        """
        accepts = self.get_studycard()

        rejects = [c for c in self.offered_courses if c not in accepts]

        # Add accepted courses to accepts
        for course in accepts:
            self.enroll(course)

        # Remove self from course lists (freeing up spots)
        for course in rejects:
            self.remove_spot(course)
            course.unenroll(self)

        return accepts

    def enroll(self, course):
        """
            Officially enroll in a course
        """
        self.enrolled_courses.add(course)

    def remove_spot(self, course):
        """
            Remove a Course spot offer.
        """
        self.offered_courses.remove(course)

    def get_studycard_value(self):
        """
            Return total utility of study card to student.
        """
        studycard = self.get_studycard()
        return sum([self.preference_dict[c] for c in studycard])

    def get_token(self, course):
        """
            Return true if the course is one of the student's top 2.
        """
        return course in self.top_2

    def has_room(self):
        """
            Return true if student has room in their studycard.
        """
        return len(self.enrolled_courses) < const.MAX_COURSES

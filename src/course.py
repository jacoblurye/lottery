"""Implements the course class.
"""

from random import random, choice

import constants as const

class Course(object):
    """
        A course with a capacity and desirability.
    """

    def __init__(self, number, cap):
        """
            Create a new course with given capacity and desirability.
        """
        self.number = number
        self.cap = cap

        # Initialize course subject
        self.subject = choice(const.SUBJECTS)

        # Initialize course quality (0 to 5)
        self.quality = random() * 5

        self.n_enrolled = 0
        self.enrolled = []

    def enroll(self, student):
        """
            Add a student to the course if there's room. 
        """
        # If the cap is reached, or the student isn't interested
        # don't enroll the student
        if self.n_enrolled >= self.cap:
            return False
        self.n_enrolled += 1
        self.enrolled.append(student)
        student.offer_spot(self)
        return True

    def unenroll(self, student):
        """
            Remove a student from the course if they choose not to enroll.
        """
        if student in self.enrolled:
            self.enrolled.remove(student)
            self.n_enrolled -= 1

    def spots(self):
        """
            Return # of free spots remaining in the course.
        """
        return self.cap - self.n_enrolled

    def has_room(self):
        """
            Return True if course hasn't reached its enrollment cap.
        """
        return self.n_enrolled < self.cap

    def __repr__(self):
        return str(self.number)
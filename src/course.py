"""Implements the course class.
"""

class Course(object):
    """
        A course with a capacity and desirability.
    """

    def __init__(self, cap, des=.5):
        """
            Create a new course with given capacity and desirability.
        """
        self.cap = cap
        self.des = des

        self.n_enrolled = 0

    def enroll(self, student):
        """
            Add a student to the course if there's room. 
        """
        if self.n_enrolled >= self.cap:
            return False
        self.n_enrolled += 1
        return True
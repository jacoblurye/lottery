"""Implements the course class.
"""

class Course(object):
    """
        A course with a capacity and desirability.
    """

    def __init__(self, number, cap, des=.5):
        """
            Create a new course with given capacity and desirability.
        """
        self.number = number
        self.cap = cap
        self.des = des

        self.n_enrolled = 0
        self.enrolled = []

    def enroll(self, student):
        """
            Add a student to the course if there's room. 
        """
        # If the cap is reached, or the student isn't interested
        # don't enroll the student
        if self.n_enrolled >= self.cap or not student.preferences[self.number]:
            return False
        self.n_enrolled += 1
        self.enrolled.append(student)
        student.offer_spot(self.number)
        return True
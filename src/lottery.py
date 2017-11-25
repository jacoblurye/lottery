"""Implements the Lottery class.
"""

from random import randint

from numpy.random import choice

from course import Course
from student import Student

class Lottery(object):
    """
        Assigns students to courses.
    """
    def __init__(self, courses, students):
        """
            Create a new lottery.
        """
        self.courses = courses
        self.students = students

        self.n_courses = len(courses)
        self.n_students = len(students)

    def run(self):
        """
            Return an allocation of students to courses.
        """
        raise AssertionError("Lottery.run not implemented")


class EfficientLottery(Lottery):
    """
        An deterministic, unrealistic mechanism that allocates according to student's true preferences.
        Used as a point of comparison to possible course assignment mechanisms.
    """

    def run(self):
        """
            Return an optimal allocation of students to courses.
        """

        # Courses offer spots to students with highest true values
        for i in xrange(self.n_courses):
            get_student_pref = lambda s: s.preferences[i]
            sorted_students = sorted(self.students, key=get_student_pref, reverse=True)
            for student in sorted_students:
                self.courses[i].enroll(student)

        n_enrolled = 0 
        for student in self.students:
            n_enrolled += len(student.get_studycard())

        print n_enrolled
        
        # Return total utility to students
        return sum([student.get_studycard_value() for student in self.students])


class RandomLottery(Lottery):
    """
        A simplified model of current Harvard lottery system.
    """

    def run(self):
        """
            Return a random allocation of students to courses, weighted by year.
        """
        # Courses offer spots to students through weighted random lottery
        for i in xrange(self.n_courses):
            interested_students = [s for s in self.students if s.preferences[i] > 0]
            years = [s.year for s in interested_students]
            norm = float(sum(years))
            weights = [y / norm for y in years]
            chosen_students = choice(interested_students, self.courses[i].cap, replace=False, p=weights)
            for student in chosen_students:
                self.courses[i].enroll(student)

        n_enrolled = 0
        for student in self.students:
            n_enrolled += len(student.get_studycard())

        print n_enrolled

        # Return total utility to students
        return sum([student.get_studycard_value() for student in self.students])


class SignallingLottery(Lottery):
    pass

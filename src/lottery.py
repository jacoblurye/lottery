"""Implements the Lottery class.
"""

from random import randint

from numpy.random import choice

import constants as const
from ttc import TTC
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

        # Return utility to students
        return self.students


class RandomLottery(Lottery):
    """
        A simplified model of current Harvard lottery system.
    """

    def run(self):
        """
            Return a random allocation of students to courses, weighted by year.
        """

        courses_with_room = set([c for c in self.courses if c.has_room()])
        students_with_room = [s for s in self.students if s.has_room() and s.interested & courses_with_room]

        # Run the lottery loop repeatedly until we've assigned as many people as we can
        while courses_with_room and students_with_room:
            
            # Courses offer spots to students through weighted random lottery
            for course in courses_with_room:

                # Collect all students who are interested in the course's subject
                interested_students = [s for s in students_with_room if course in s.interested]

                if not interested_students:
                    continue
                
                # Construct the weights on students
                years = [s.year for s in interested_students]
                norm = float(sum(years))
                weights = [y / norm for y in years]
                
                cap = min(len(interested_students), course.spots())

                # Offer spots to randomly chosen students in the course
                chosen_students = choice(interested_students, cap, replace=False, p=weights)
                for student in chosen_students:
                    course.enroll(student)

                # Students make acceptances and rejections
                for student in students_with_room:
                    student.get_studycard_destructive()

                courses_with_room = set([c for c in self.courses if c.has_room()])
                students_with_room = [s for s in self.students if s.has_room() and s.interested & courses_with_room]

        # Return students
        return self.students


class TTCLottery(RandomLottery):
    """
        Random lottery + TTC.
    """

    def run(self):
        """
            Run the Harvard lottery, then trade results with TTC.
        """
        self.students = super(TTCLottery, self).run()

        ttc = TTC(self.students)
        ttc.run()

        return self.students


class SignallingLottery(Lottery):
    """
        A mechanism wherein students can signal interest to their top 2 favorite courses.
    """

    def run(self):
        """
            Return an interest-informed allocation of students to courses.
        """
        # Courses offer spots to oldest interested students first
        for course in xrange(self.n_courses):
            # Students who might enter the lottery
            interested_students = [s for s in self.students if s.preferences[course] > 0]

            # Sort students by interest then by year
            interested_students = sorted(
                interested_students,
                key=lambda s: (s.get_token(course), s.year), 
                reverse=True
            )

            for student in interested_students[:self.courses[course].cap]:
                self.courses[course].enroll(student)

        return self.students


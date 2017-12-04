from copy import deepcopy
from collections import defaultdict

from ttc import TTC
from course import Course 
from student import Student
from factory import Factory
from lottery import RandomLottery, TTCLottery

def example():
    courses = [
        Course(0, 2),
        Course(1, 1),
        Course(2, 3),
        Course(3, 1),
    ]

    students = [Student(i, courses) for i in xrange(6)]

    # Set up preferences
    def pref_sort(p): return sorted(p, key=lambda t: t[1])
    students[0].preference_dict = defaultdict(int, {
        courses[0]: 4,
        courses[3]: 3,
        courses[1]: 2,
        courses[2]: 1
    })
    students[0].preferences = pref_sort(students[0].preference_dict.items())
    students[1].preference_dict = defaultdict(int, {
        courses[1]: 4,
        courses[2]: 3,
    })
    students[1].preferences = pref_sort(students[1].preference_dict.items())
    students[2].preference_dict = defaultdict(int, {
        courses[2]: 4,
        courses[0]: 3,
        courses[1]: 2,
    })
    students[2].preferences = pref_sort(students[2].preference_dict.items())
    students[3].preference_dict = defaultdict(int, {
        courses[0]: 4,
        courses[2]: 3,
    })
    students[3].preferences = pref_sort(students[3].preference_dict.items())
    students[4].preference_dict = defaultdict(int, {
        courses[2]: 4,
        courses[0]: 3,
        courses[3]: 2,
    })
    students[4].preferences = pref_sort(students[4].preference_dict.items())
    students[5].preference_dict = defaultdict(int, {
        courses[1]: 4,
        courses[2]: 3,
        courses[3]: 2,
    })
    students[5].preferences = pref_sort(students[5].preference_dict.items())

    # Set up offered courses
    students[0].offered_courses.update([courses[1], courses[2]])
    students[1].offered_courses.update([courses[2]])
    students[2].offered_courses.update([courses[0]])
    students[3].offered_courses.update([courses[2]])
    students[4].offered_courses.update([courses[0]])
    students[5].offered_courses.update([courses[3]])

    orig_utils = sum([s.get_studycard_value() for s in students])

    ttc = TTC(students)
    ttc.run()
    ttc_utils = [s.get_studycard_value() for s in ttc.students]

    print orig_utils
    print sum(ttc_utils)
    print sum([len(set(s.get_studycard())) for s in ttc.students])


if __name__ == '__main__':
    #example()

    diffs = []
    for i in xrange(1):
        f = Factory(50, 500, 12, 12)
        courses, students = f.generate(123)
        rl = RandomLottery(courses, students)
        rl_stud = rl.run()
        rl_utils = [s.get_studycard_value() for s in rl.students]

        ttc = TTC(rl_stud)
        ttc.run()
        ttc_utils= [s.get_studycard_value() for s in ttc.students]
        diffs.append(sum(ttc_utils) - sum(rl_utils))
    
    print sum(diffs)

    # print "Welfare under random lottery: ", sum(rl_utils)
    # print "Welfare under random lottery + TTC: ", sum(ttc_utils)
    # print sum([len(s.get_studycard()) for s in rl.students])
    # print sum([len(set(s.get_studycard())) for s in ttc.students])
    # print max([t - r for t, r in zip(ttc_utils, rl_utils)])
    # print sum([t - r for t, r in zip([len(set(s.get_studycard())) for s in ttc.students], [len(s.get_studycard()) for s in rl.students])]) / float(len(rl.students))

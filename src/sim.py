"""Compare RandomLottery with RandomLottery+TTC
"""
import argparse
from copy import deepcopy

import numpy as np

from ttc import TTC
from course import Course
from student import Student
from factory import Factory
from lottery import RandomLottery

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument("--n_courses", type=int, default=10,
                    help="# of courses in the lottery")
parser.add_argument("--n_students", type=int, default=30,
                    help="# of students in the lottery")
parser.add_argument("--min_cap", type=int, default=2,
                    help="minimum course enrollment cap")
parser.add_argument("--max_cap", type=int, default=3,
                    help="maximum course enrollment cap")
parser.add_argument("--iters", type=int, default=1,
                    help="# of iterations to run comparison")

def random_vs_ttc(n_courses, n_students, min_cap, max_cap, iters):
    """
        Compare RandomLottery outcome with RL+TTC outcome.
    """

    f = Factory(n_courses, n_students, min_cap, max_cap)

    student_diffs = []
    total_diffs = []
    mean_student_diffs = []
    for i in xrange(iters):
        courses, students = f.generate()

        # Run the RandomLottery
        rl = RandomLottery(courses, students)
        rl_students = rl.run()
        rl_utils = [s.get_studycard_value() for s in rl.students]
        rl_welfare = sum(rl_utils)

        # Run TTC on the output of RandomLottery
        ttc = TTC(deepcopy(rl_students))
        ttc.run()
        ttc_utils = [s.get_studycard_value() for s in ttc.students]
        ttc_welfare = sum(ttc_utils)
        
        # Compute summary statistics
        total_diff = (ttc_welfare - rl_welfare) / float(ttc_welfare + rl_welfare) * 100
        total_diffs.append(total_diff)
        student_diff = [(t - r) / float(t + r) * 100 if t +
                        r else 0 for t, r in zip(ttc_utils, rl_utils)]
        student_diffs.append(student_diff)
        mean_student_diff = np.mean(student_diff)
        mean_student_diffs.append(mean_student_diff)
    
    print
    print "=========================================="
    print "Overall Welfare Improvement (%): "
    print "mean: ", np.mean(total_diffs), "std: ", np.std(total_diffs)
    print "=========================================="
    print "Mean Individual Welfare Improvement (%):"
    print "mean: ", np.mean(mean_student_diffs), "std: ", np.std(mean_student_diffs)
    print "=========================================="
    print

    return student_diffs, total_diffs, mean_student_diffs

def main():
    args = parser.parse_args()
    random_vs_ttc(
        args.n_courses, 
        args.n_students, 
        args.min_cap,
        args.max_cap,
        args.iters
    )

if __name__ == '__main__':
    main()
from copy import deepcopy

from ttc import TTC
from factory import Factory
from lottery import RandomLottery, EfficientLottery, SignallingLottery

if __name__ == '__main__':
    f = Factory(20, 1000, 12, 20)
    courses, students = f.generate(123)
    rl = RandomLottery(courses, students)
    rl_stud = rl.run()

    ttc = TTC(deepcopy(rl_stud))
    ttc.run()

    rl_welfare = sum([s.get_studycard_value() for s in rl.students])
    ttc_welfare = sum([s.get_studycard_value() for s in ttc.students])
    print "Welfare under random lottery: ", rl_welfare
    print "Welfare under random lottery + TTC: ", ttc_welfare

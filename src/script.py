from lottery import RandomLottery, EfficientLottery, SignallingLottery
from factory import Factory

if __name__ == '__main__':
    f = Factory(20,100,12,12)
    courses, students = f.generate(123)
    rl = RandomLottery(courses, students)
    rl_stud = rl.run()
    courses, students = f.generate(123)
    el = EfficientLottery(courses, students)
    el_stud = el.run()
    courses, students = f.generate(123)
    sl = SignallingLottery(courses, students)
    sl_stud = sl.run()

from lottery import RandomLottery, EfficientLottery
from factory import Factory

if __name__ == '__main__':
    f = Factory(10,100,12,12)
    courses, students = f.generate(321)
    rl = RandomLottery(courses, students)
    print rl.run()
    courses, students = f.generate(321)
    el = EfficientLottery(courses, students)
    print el.run()

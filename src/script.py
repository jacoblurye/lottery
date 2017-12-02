from lottery import RandomLottery, EfficientLottery, SignallingLottery
from factory import Factory

if __name__ == '__main__':
    f = Factory(50,1000,12, 50)
    courses, students = f.generate(123)
    rl = RandomLottery(courses, students)
    rl_stud = rl.run()
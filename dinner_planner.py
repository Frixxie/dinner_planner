import csv
from random import choices

class DinnerObj():
    def __init__(self, dinner, typp, pri):
        if not self.check_args(dinner, int(pri), int(typp)):
            raise Exception("Wrong type args")
        self.name = dinner
        self.pri = int(pri)
        self.type = int(typp)

    def check_args(self, dinner, pri, typp):
        """
        Prob need better type checking for this
        """
        if not isinstance(dinner, str):
            return False
        if not isinstance(pri, int):
            return False
        if not isinstance(typp, int):
            return False
        return True


    def __str__(self):
        return f"{self.name}, {self.type}, {self.pri}"

class DinnerPlanner():
    def __init__(self, input_file, skiplines, num_days, non_repeat):
        self.dinners = self.load(input_file, skiplines)
        self.weights = self.create_weights()
        self.num_days = num_days
        self.non_repeat = non_repeat

    def plan_dinners(self):
        dinners = list()
        for i in range(self.num_days):
            dinner = choices(self.dinners, self.weights, k=1)[0]
            print(i, dinner.name)

    def load(self, input_file, skiplines):
        """
        Reads dinners from disk and retruns a list of dinner objects
        """
        dinners = list()
        with open(input_file) as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            index = 0
            for row in reader:
                if index < skiplines:
                    index += 1
                    continue
                dinners.append(DinnerObj(row[0], row[1], row[2]))
        return dinners

    def create_weights(self):
        weights = list()
        for dinner in self.dinners:
            weights.append(dinner.pri)
        return weights


if __name__ == '__main__':
    dp = DinnerPlanner("example_dinners.csv", 1, 3000, 1)
    dp.plan_dinners()

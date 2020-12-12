import csv
import getopt
import sys
from random import choices

class DinnerObj():
    def __init__(self, dinner, typp, pri):
        if not self.check_args(dinner, int(pri), typp):
            raise Exception("Wrong type args")
        self.name = dinner
        self.pri = int(pri)
        self.type = typp

    def check_args(self, dinner, pri, typp):
        """
        Prob need better type checking for this
        """
        if not isinstance(dinner, str):
            return False
        if not isinstance(pri, int):
            return False
        if not isinstance(typp, str):
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
        redraws = 0
        while len(dinners) < self.num_days:
            dinner = choices(self.dinners, self.weights, k=1)[0]
            if self.check_order(dinner, dinners) and self.check_types(dinner, dinners):
                dinners.append(dinner)            
            else:
                redraws += 1
            if len(dinners) % 7 == 0:
                if not self.check_week(dinners):
                    for _ in range(7):
                        dinners.pop()
        for dinner in dinners:
            print(dinner)
        print("redraws", redraws)

    def check_week(self, dinners):
        num_fish = 0
        num_vegan = 0
        for dinner in dinners:
            if dinner.type == 'fish':
                num_fish += 1
            if dinner.type == 'vegan':
                num_vegan += 1
        # print(num_fish, num_vegan)
        if num_fish >= 3 and num_vegan >= 1:
            return True
        return False

    def check_types(self, dinner, dinners):
        if len(dinners) < 1:
            return True
        elif dinner.type == dinners[len(dinners) - 1].type:
            return False
        return True

    def check_order(self, dinner, dinners):
        if len(dinners) < 1:
            return True
        if len(dinners) < self.non_repeat:
            for other_dinner in dinners:
                if other_dinner.name == dinner.name:
                    return False
        else:
            idx = len(dinners) - 1
            for i in range(self.non_repeat):
                if dinner.name == dinners[idx - i].name:
                    return False
        return True

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

def parse_opts():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hn:r:t")
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    num_days = None
    non_repeat = None
    typesystem = None
    for o, a in opts:
        if o == "-h":
            print("will make help func soon")
            sys.exit(1)
        elif n == "-n":
            num_days = int(a)
        elif r == "-r":
            non_repeat = int(a)
        elif t == "-t":
            typesystem = True
        else:
            assert False, "unhandled option!"
    return num_days, non_repeat, typesystem




if __name__ == '__main__':
    dp = DinnerPlanner("example_dinners.csv", 1, 14, 2)
    dp.plan_dinners()

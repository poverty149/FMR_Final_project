
import itertools
from ggsolver.models import TSys
import random


class intersection(TSys):
    """"
    Class to model the intersection as a deterministic transition system. Only implemented for one car for now, so not
    fully implemented
    """
    def __init__(self):
        super(intersection, self).__init__(is_deterministic=True)

    def states(self):
        """
        Returns a list of states
        """
        trajectories = ["S","R","L","N"]
        states = []
        for i in range(1,13):
            for j in range(0,4):
                states.append((i,trajectories[j]))

        return states

    def actions(self):
        """
        Returns a list of possible actions
        """
        return ["aS","aR","aL","aN"]

    def delta(self, state, inp):
        """
        Defines the transition function
        """
        one_act_states = {(4, "S"): (8, "S"), (8, "S"): (11, "S"), (11, "S"): (13, "N"),
                      (4, "L"): (9, "L"), (9, "L"): (10, "L"), (10, "L"): (13, "N"),
                      (4, "R"): (3, "R"), (3, "R"): (13, "N"),

                      (8, "S"): (9, "S"), (9, "S"): (10, "S"), (10, "S"): (13, "N"),
                      (8, "L"): (5, "L"), (5, "L"): (2, "L"), (2, "L"): (13, "N"),
                      (8, "R"): (11, "R"), (11, "R"): (13, "N"),

                      (9, "S"): (5, "S"), (5, "S"): (2, "S"), (2, "S"): (13, "N"),
                      (9, "L"): (4, "L"), (4, "L"): (3, "L"), (3, "L"): (13, "N"),
                      (9, "R"): (10, "R"), (10, "R"): (13, "N"),

                      (5, "S"): (4, "S"), (4, "S"): (3, "S"), (3, "S"): (13, "N"),
                      (5, "L"): (8, "L"), (8, "L"): (11, "L"), (11, "L"): (13, "N"),
                      (5, "R"): (2, "R"), (2, "R"): (13, "N"),
                      }
        if one_act_states.get(state) != None:
            return one_act_states[state]

        if state[1] == "N":
            if state[0] == 13:
                return (13,"N")
            if state[0] == 1 and inp[1] != "N":
                return (4,inp[1])
            elif state[0] == 1 and inp[1] == "N":
                return (1,"N")

            if state[0] == 6 and inp[1] != "N":
                return (5,inp[1])
            elif state[0] == 1 and inp[1] == "N":
                return (6,"N")

            if state[0] == 7 and inp[1] != "N":
                return (8,inp[1])
            elif state[0] == 1 and inp[1] == "N":
                return (7,"N")

            if state[0] == 12 and inp[1] != "N":
                return (9,inp[1])
            elif state[0] == 1 and inp[1] == "N":
                return (12,"N")




        pass

    def atoms(self):
        return ["exited","collision"]


    def label(self, state):
        """
        not all APs can be properly labeled since this TS is currently only for one car, and the "collision" AP
        requires multiple cars
        """
        aps = []
        if state[0] == 13:
            aps.append("exited")
        return aps


if __name__ == '__main__':
    tsys = intersection()
    state = (7,"N")
    print(state)
    for i in range(1,5):
        act = random.choice(tsys.actions())
        print(act)
        state = tsys.delta(state,act)
        print(state)




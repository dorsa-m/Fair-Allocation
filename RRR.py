import random
from itertools import permutations, product

C = 20


class Agent:
    def __init__(self, m):
        self.m = m
        pref = random.sample(range(C + 1), m)
        total = sum(pref)
        normalized_pref = [x / total for x in pref]
        self.preferences = normalized_pref
        self.bundle = []
        self.welfare = 0

    def reset(self):
        self.bundle = []
        self.welfare = 0

    def make_choice(self, available_items):
        masked_preferences = [self.preferences[i] if i in available_items else -1 for i in range(self.m)]
        max_index, max_value = max(enumerate(masked_preferences), key=lambda x: x[1])
        self.bundle.append(max_value)
        return max_index


def play_round(agents, available_items, permutation):
    end_flag = False
    for agent_index in permutation:
        if not available_items:
            end_flag = True
            return end_flag
        agent = agents[agent_index]
        chosen_item = agent.make_choice(available_items)
        available_items.remove(chosen_item)
    return end_flag


# if expected = True, pay attention that m = nk
def RRR(agents, m, expected=True):
    n = len(agents)
    if not expected:
        available_items = list(range(m))
        end_flag = False
        perm_list = []
        while not end_flag:
            perm = random.sample(range(n), n)
            perm_list.append(perm)
            end_flag = play_round(agents, available_items, perm)
        print(f'RRR perm is {perm_list}')
        return perm_list
    else:
        k = int(m / n)
        perm_list = list(permutations(range(n)))
        all_random_cases = list(product(perm_list, repeat=k))
        for case in all_random_cases:
            available_items = list(range(m))
            for round in range(k):
                perm = case[round]
                play_round(agents, available_items, perm)
        return None


def QRRR(agents, m, expected=True):
    n = len(agents)
    if not expected:
        perm = random.sample(range(n), n)
        available_items = list(range(m))
        end_flag = False
        while not end_flag:
            end_flag = play_round(agents, available_items, perm)
        print(f'QRRR perm is {perm}')
        return perm
    else:
        k = int(m / n)
        perm_list = list(permutations(range(n)))
        for perm in perm_list:
            available_items = list(range(m))
            for round in range(k):
                play_round(agents, available_items, perm)
        return None


def value_conversion(values, second_list, index_show=True):
    if not index_show:
        letter_mapping = {value: chr(ord('A') + i) for i, value in enumerate(values)}
        result_letters = [letter_mapping.get(value) for value in second_list]
        return result_letters
    else:
        values = sorted(values, reverse=True)
        result_index = [values.index(value)+1 for value in second_list]
        return result_index


def sort_letters(values):
    letters = [chr(ord('A') + i) for i in range(len(values))]
    sorted_data = sorted(zip(letters, values), key=lambda x: x[1], reverse=True)
    sorted_letters = [letter for letter, _ in sorted_data]
    return sorted_letters


def SW_analysis(agents, name, verbose=False):
    # Total_SW = 0
    Obtained_SW = 0
    for i, agent in enumerate(agents):
        # Total_SW += sum(agent.preferences)
        agent.welfare = sum(agent.bundle) / len(agent.bundle)
        Obtained_SW += agent.welfare
        if verbose:
            print(f'Agent {i + 1} preferences:')
            print(agent.preferences)
            print(sort_letters(agent.preferences))
            print(f'Agent {i + 1} performance in {name}:')
            # print(agent.bundle)
            print(value_conversion(agent.preferences, agent.bundle))
            # print(value_conversion(agent.preferences, agent.bundle, False))
            print('**********')
    if verbose:
        print(f'E_Obtained_SW = {Obtained_SW}')
        print('#############################End of Analysis#############################')
    return Obtained_SW


def main():
    m = 6
    n = 2

    repeat = 1
    for i in range(repeat):
        agents = []
        for i in range(n):
            agents.append(Agent(m))
        RRR(agents, m)
        r_1 = SW_analysis(agents, 'RRR', True)
        for agent in agents:
            agent.reset()
        QRRR(agents, m)
        r_2 = SW_analysis(agents, 'QRRR', True)
        for agent in agents:
            agent.reset()
        print(r_1 >= r_2)


if __name__ == "__main__":
    main()

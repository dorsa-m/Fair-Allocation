import random
import matplotlib.pyplot as plt
from collections import Counter
from itertools import permutations, product


class Agent:
    def __init__(self, m, values):
        self.m = m
        self.preferences = values
        self.bundle = []

    def reset(self):
        self.bundle = []

    def make_choice(self, available_items):
        masked_preferences = [self.preferences[i] if i in available_items else -1 for i in range(self.m)]
        max_index, max_value = max(enumerate(masked_preferences), key=lambda x: x[1])
        return max_index


def egal_sw(agents_list):
    welfares = []
    for agent in agents_list:
        welfare = sum([agent.preferences[i] for i in agent.bundle])
        welfares.append(welfare)
    min_value = min(welfares)
    argmin_index = welfares.index(min_value)
    return argmin_index, min_value


def sort_letters(values):
    letters = [chr(ord('A') + i) for i in range(len(values))]
    sorted_data = sorted(zip(letters, values), key=lambda x: x[1], reverse=True)
    sorted_letters = [letter for letter, _ in sorted_data]
    return sorted_letters


def show_agents(agents_list):
    for i, agent in enumerate(agents_list):
        print(f'Agent {i + 1} preferences:')
        print(agent.preferences)
        print(sort_letters(agent.preferences))
    print('********************End of Preferences****************')
    for i, agent in enumerate(agents_list):
        print(f'Agent {i + 1} bundle:')
        print([chr(ord('A') + i) for i in agent.bundle])


def generate_values(n, m):
    values = [[random.randint(0, 20) for _ in range(m)] for _ in range(n)]
    normalized_values = [[value / sum(row) for value in row] for row in values]
    return normalized_values


def initialize_agents(values, m, n):
    return [Agent(m, values[i]) for i in range(n)]


def MRR(n, m):
    # initialize injustice matrix
    # values = generate_values(n, m)
    values = [[8, 2, 7, 1, 6, 5, 4, 3], [8, 2, 7, 1, 6, 5, 4, 3], [2, 8, 7, 1, 6, 5, 4, 3], [2, 8, 7, 6, 5, 1, 4, 3]]
    agents = initialize_agents(values, m, n)
    injustice_matrix = [[0 for _ in range(n)] for _ in range(n)]
    imbalanced_agents = []
    available_items = list(range(m))

    while available_items:
        # Check if the list of imbalanced agents is full, make it empty if so
        if len(imbalanced_agents) == n:
            imbalanced_agents = []

        # Ask each non-imbalanced agent to choose their most valuable item
        tie_list = {item: [] for item in available_items}
        for agent_idx in range(n):
            if agent_idx not in imbalanced_agents:
                chosen_item = agents[agent_idx].make_choice(available_items)
                tie_list[chosen_item].append(agent_idx)

        # Handle ties
        for item, tie_group in tie_list.items():
            if len(tie_group) == 1:
                winner = tie_group[0]
                agents[winner].bundle.append(item)
                imbalanced_agents.append(winner)
                available_items.remove(item)
            if len(tie_group) > 1:
                winner = handle_tie(tie_group, injustice_matrix)
                winner_agent = agents[winner]
                winner_agent.bundle.append(item)
                update_injustice_matrix(winner, tie_group, injustice_matrix)
                imbalanced_agents.append(winner)
                available_items.remove(item)
    return agents


def handle_tie(tie_group, injustice_matrix):
    # Calculate the sum of injustice scores for each agent in the tie group
    sum_scores = [sum(injustice_matrix[agent][other_agent] for other_agent in tie_group) for agent in tie_group]

    # Find the agent with the minimum sum of scores
    min_score = min(sum_scores)
    min_score_agents = [agent for agent, score in zip(tie_group, sum_scores) if score == min_score]
    chosen_agent = random.choice(min_score_agents)
    return chosen_agent


def update_injustice_matrix(winner, tie_group, injustice_scores):
    # Add one to every entry corresponding to other members of the tie group except the winner
    for agent in tie_group:
        if agent == winner:
            for other_agent in tie_group:
                if other_agent != winner:
                    injustice_scores[agent][other_agent] += 1

    # Subtract one from row j, i_th entry of the injustice matrix for j in the tie group
    for other_agent in tie_group:
        if other_agent != winner:
            injustice_scores[other_agent][winner] -= 1


def play_round(agents, available_items, permutation):
    end_flag = False
    for agent_index in permutation:
        if not available_items:
            end_flag = True
            return end_flag
        agent = agents[agent_index - 1]
        chosen_item = agent.make_choice(available_items)
        agent.bundle.append(chosen_item)
        available_items.remove(chosen_item)
    return end_flag


def calculate_permutation_lists(m, n):
    # Generate all permutations of 1 to n
    all_permutations = list(map(list, permutations(range(1, m + 1))))
    # Generate all possible pairs of permutations using Cartesian product
    product_permutations = product(all_permutations, repeat=n)
    res = list(map(list, product_permutations))
    return res


def picking_sequences(values, n, m, perm, same_seq=True):
    # values = generate_values(n, m)
    # values = [[8, 2, 7, 1, 6, 5, 4, 3], [8, 2, 7, 1, 6, 5, 4, 3], [2, 8, 7, 1, 6, 5, 4, 3], [2, 8, 7, 6, 5, 1, 4, 3]]
    agents = initialize_agents(values, m, n)
    available_items = list(range(m))
    end_flag = False
    while not end_flag:
        if same_seq:
            end_flag = play_round(agents, available_items, perm)
        else:
            if not perm:
                return agents
            end_flag = play_round(agents, available_items, perm[0])
            perm.pop(0)
    return agents


def draw_frequency(data, i):
    # Use Counter to count the frequency of each sublist
    list_counter = Counter(map(tuple, data))

    # Separate keys and values
    lists = [tuple(key) for key in list_counter.keys()]
    frequencies = list(list_counter.values())
    # print(len(frequencies))
    # if min(frequencies) == max(frequencies):
    #     print("All the same!")
    #     return
    plt.bar(list(range(len(lists))), [f/sum(frequencies) for f in frequencies])
    plt.xticks(range(len(lists)), lists, rotation='vertical')
    plt.xlabel('Lists')
    plt.ylabel('Frequency')
    plt.title(f'Frequency of Each Bundle for agent {i+1}')
    plt.show()

n = 2
m = 4

all_borda_valuations = calculate_permutation_lists(m, n)
all_bundles_agent_1 = []
all_bundles_agent_2 = []
for valuation in all_borda_valuations:
    # res = picking_sequences(valuation,n,m,[[1,2],[1,2],[2,2]],False)
    res = picking_sequences(valuation, n, m, [[1, 2], [2,1]], False)
    # res = picking_sequences(valuation, n, m, [1, 2])
    # show_agents(res)
    agent = res[0]
    bundle = [agent.preferences[i] for i in agent.bundle]
    all_bundles_agent_1.append(bundle)
    agent = res[1]
    bundle = [agent.preferences[i] for i in agent.bundle]
    all_bundles_agent_2.append(bundle)
    # print(bundle)
    # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
draw_frequency(all_bundles_agent_1, 0)
draw_frequency(all_bundles_agent_2, 1)

# # random.seed(6)
# # res = MRR(4, 8)
#
# # res = picking_sequences(4,8,[1,2,3,4])
# res = picking_sequences(2, 4, [[1, 2], [1, 2]])
# show_agents(res)
# print('***********************************')
# print('Egalitarian SW:')
# print(egal_sw(res))

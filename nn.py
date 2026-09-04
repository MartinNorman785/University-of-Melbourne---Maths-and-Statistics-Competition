import random
import pickle
import numpy as np
import math
import matplotlib.pyplot as plt

PRECISION = 10


class Player:
    def __init__(self): 
        self.total = 0 

    def draw(self):
        return random.uniform(0, 1)


class Connection:
    def __init__(self, weight):
        self.weight = weight

    def value(self, input_value):
        return self.weight * input_value

    def __repr__(self):
        return "Cntn: W=" + str(round(self.weight, 3))


class Node:
    def __init__(self, bias):
        self.bias = bias
    def sigmoid(self, x):
         return 1 / (1 + math.exp(-x))
    def value(self, inputs):
        return self.sigmoid(sum(inputs) + self.bias)

    def __repr__(self):
        return "Node: T=" + str(round(self.bias, 3))


class Network:
    NODES_STRUCTURE = [2, 3, 1]
    DIRECTION_CHANGES = 50
    STEP_TRIALS = 100000
    DEFAULT_TRAINING_TIMES = 100

    def __init__(self):
        self.length = 0
        self.nodes = []
        for i in range(len(self.NODES_STRUCTURE)):
            layer = []
            for _ in range(self.NODES_STRUCTURE[i]):
                node = Node(random.gauss(0, 1))
                if i > 0:
                    connections = [Connection(random.gauss(0, 1)) for _ in self.nodes[-1]]
                    self.length += len(connections)
                else:
                    connections = []
                layer.append((node, connections))
            self.nodes.append(layer)
            self.length += len(layer)
        try:
            with open('ai.pickle', 'rb') as file:
                self.ai_p2 = pickle.load(file)
        except:
            self.ai_p2 = None

    def run(self, inputs):
        for l, layer in enumerate(self.nodes):
            results = []
            if l > 0:
                for node, connections in layer:
                    results.append(node.value([conn.value(inputs[i]) for i, conn in enumerate(connections)]))
                inputs = results
        return results

    def get_random_direction(self):
        return [random.gauss(0, 1)/self.DIRECTION_CHANGES for _ in range(self.length)]

    def make_copy(self):
        new_net = Network()
        new_net.length = self.length
        new_net.nodes = []
        for i in range(len(self.NODES_STRUCTURE)):
            layer = []
            for j in range(self.NODES_STRUCTURE[i]):
                node = Node(self.nodes[i][j][0].bias)
                if i > 0:
                    connections = [Connection(self.nodes[i][j][1][k].weight) for k in range(len(self.nodes[i][j][1]))]
                else:
                    connections = []
                layer.append((node, connections))
            new_net.nodes.append(layer)
        return new_net

    def move_in_direction(self, direction):
        i = 0
        for layer in self.nodes:
            for node, connections in layer:
                node.bias += direction[i]
                i += 1
                for conn in connections:
                    conn.weight += direction[i]
                    i += 1

    def fitness(self, seed):
        random.seed(seed)
        p = Player()
        total_reward = 0
        for _ in range(self.STEP_TRIALS):
            p1 = p.draw()
            p2 = p.draw()
            turn = 1
            p1_passed = False
            p2_passed = False
            while p1 < 1 and p2 < 1 and (not p1_passed or not p2_passed):
                if turn % 2 == 1 and not p1_passed:
                    if p2 > p1 or (not p2_passed and self.run([p1, p2])[0] > 0.5):
                        p1 += p.draw()
                    else:
                        p1_passed = True
                elif not p2_passed:
                    if self.other_choice(p1_passed, p2, p1):
                        p2 += p.draw()
                    else:
                        p2_passed = True
                turn += 1
            # Result logic
            if p1 > 1:
                reward = -1
            elif p2 > 1:
                reward = 1
            elif p1 > p2:
                # Win, bonus if margin is safe
                reward = 1
            elif p2 > p1:
                reward = -1
            else:
                reward = 0  # Tie
            total_reward += reward
        return total_reward

    def other_choice(self, passed, score, other_score):
        if score > other_score:
            return True
        elif passed:
            return False
        else:
            return score < -0.5048 * other_score + 0.5722
        

    def run_training_step(self):
        seed = random.randint(0, 10000)
        direction = self.get_random_direction()

        random.seed(seed)
        base_fitness = self.fitness(seed)

        best_fitness = base_fitness
        best_step = 0

        for i in range(1, self.DIRECTION_CHANGES + 1):
            for sign in [-1, 1]:
                test_net = self.make_copy()
                test_net.move_in_direction([sign * i * x for x in direction])
                random.seed(seed)
                f = test_net.fitness(seed)
                if f > best_fitness:
                    best_fitness = f
                    best_step = sign * i

        if best_step != 0:
            self.move_in_direction([best_step * x for x in direction])


    def run_training(self, times=DEFAULT_TRAINING_TIMES):
        for _ in range(times):
            self.run_training_step()


if __name__ == "__main__":
    with open('ai2.pickle', 'rb') as file:
        n = pickle.load(file)

    for _ in range(1):
        n.run_training()
        with open("ai.pickle", "wb") as f:
            pickle.dump(n, f)

    n.run_training()
    with open("ai2.pickle", "wb") as f:
        pickle.dump(n, f)

    # Generate heatmap
    probs = [[n.run([x / PRECISION, y / PRECISION])[0] if x > y else 0
              for y in range(PRECISION)] for x in range(PRECISION)]

    plt.imshow(probs, cmap='viridis', origin='lower')
    plt.colorbar(label='NN Output')
    plt.title('Neural Network Decision Map')
    plt.xlabel('y / PRECISION')
    plt.ylabel('x / PRECISION')
    plt.savefig("nn.png")
    plt.show()
    print("Plot saved as nn.png")

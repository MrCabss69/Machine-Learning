import random
import math

class MCTS:
    def __init__(self, maze):
        self.maze    = maze
        self.visits  = {}                                                       # Tracks number of visits to each node
        self.parents = {}                                                       # Tracks the parent of each node
        self.rewards = {}                                                       # Tracks the average reward for each node

    def select_best_action(self):
        root = self.maze.player
        best_move = None
        best_value = float('-inf')
        for move in self._get_possible_moves(root):
            if move in self.visits:
                value = self.rewards.get(move, 0) / self.visits[move]
                if value > best_value:
                    best_value = value
                    best_move = move
        return best_move
    
    def solve(self):
        root = self.maze.player
        self.visits[root] = 1
        self.parents[root] = None
        
        while not self._is_terminal(root):
            leaf_node = self._select(root)
            reward = self._simulate(leaf_node)
            self._backpropagate(leaf_node, reward)
            
    def _select(self, node):
        while self._get_possible_moves(node):
            if not self._is_fully_explored(node):
                return self._expand(node)
            else:
                node = self._best_child(node)
        return node

    def _expand(self, node):
        move = self._get_pending_move(node)
        self.visits[move] = 1
        self.parents[move] = node
        return move

    def _simulate(self, node):
        while not self._is_terminal(node):
            node = random.choice(self._get_possible_moves(node))
        return self._calculate_reward(node)

    def _backpropagate(self, node, reward):
        while node is not None:
            self.visits[node] += 1
            self.rewards[node] = (self.rewards.get(node, 0) * (self.visits[node] - 1) + reward) / self.visits[node]
            node = self.parents[node]

    def _best_child(self, node, Cp=1.0):
        best_score = float('-inf')
        best_move = None
        for move in self._get_possible_moves(node):
            if move in self.visits:
                avg_reward = self.rewards[move] / self.visits[move]
                exploration_term = 2 * Cp * math.sqrt((2 * math.log(self.visits[node]) / self.visits[move]))
                score = avg_reward + exploration_term
            else:
                score = float('inf')
            if score > best_score:
                best_score = score
                best_move = move
        return best_move
    
    def select_best_action(self):
        best_value = float('-inf')
        best_action = None
        for move in self._get_possible_moves(self.maze.player):
            if move not in self.visits:
                self.visits[move] = 0
                self.rewards[move] = 0

            if self.visits[move] > 0:
                value = self.rewards[move] / self.visits[move]
            else:
                value = float('inf')
            if value > best_value:
                best_value = value
                best_action = move

        return best_action

    
    def _get_pending_move(self, node):
        moves = self._get_possible_moves(node)
        untried_moves = [move for move in moves if move not in self.visits.keys()]
        return random.choice(untried_moves) if untried_moves else None

    def _get_possible_moves(self, node):
        return list(self.maze.grid.neighbors(node))

    def _calculate_reward(self, node):
        return -1 * (abs(node[0] - self.maze.end[0]) + abs(node[1] - self.maze.end[1]))

    def _is_terminal(self, node):
        return node == self.maze.end or all(move in self.visits for move in self._get_possible_moves(node))

    def _is_fully_explored(self, node):
        return all(move in self.visits for move in self._get_possible_moves(node))
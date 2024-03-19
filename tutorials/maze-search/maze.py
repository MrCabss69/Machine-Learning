import networkx as nx
import numpy as np 
import matplotlib.pyplot as plt

class Maze:
    def __init__(self, N=5):
        self.N       = N
        self.end     = (N-1,N-1)
        self.start   = (0,0)
        self.player  = (0,0)
        self.bariers = []
        self.grid    = self.generate()

    def generate(self):
        while True:
            G = nx.grid_2d_graph(self.N, self.N)
            all_nodes = list(G.nodes())
            all_nodes.remove(self.start)
            all_nodes.remove(self.end)
            barriers = np.random.choice(range(len(all_nodes)), size=2*self.N, replace=False)
            barriers = [all_nodes[i] for i in barriers]
            G.remove_nodes_from(barriers)
            if nx.has_path(G, self.start, self.end):
                return G

    def display(self):
        pos     = {(x, y): (y, -x) for x, y in self.grid.nodes()}
        fig, ax = plt.subplots(figsize=(5, 5))
        nx.draw(self.grid, pos=pos, ax=ax, node_size=100, node_color='lightgray')
        nx.draw_networkx_nodes(self.grid, pos=pos, nodelist=[self.player], node_color='green', node_size=150, label='Jugador')
        nx.draw_networkx_nodes(self.grid, pos=pos, nodelist=[self.end], node_color='red', node_size=150, label='Meta')
        ax.legend()
        plt.grid(True)
        plt.axis('equal')
        plt.show()
        
        
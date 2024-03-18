import heapq

class GraphSearchAlgorithm:
    def __init__(self, maze):
        self.maze = maze
        self.solution = None

    def solve(self, start=None, end=None, hn=lambda x,y: 0):
        """
        Soluciona el laberinto utilizando el algoritmo A* con Dijkstra como caso predeterminado.
        
        :param start: Punto de inicio para la búsqueda. Si es None, se usan todos los nodos como inicio.
        :param end: Punto final deseado. Si es None, se buscan caminos a todos los nodos alcanzables desde 'start'.
        :param hn: Función heurística para estimar el costo desde un nodo al objetivo (por defecto 0, que convierte el algoritmo en Dijkstra).
        
        :return: El camino solución como una lista de nodos desde 'start' a 'end', o un diccionario de todos los caminos mínimos si 'start' es None.
        """
        if start is None:
            self.solution = {}
            for node in self.maze.grid.nodes:
                self.core(node, end, hn)
        else:
            return self.core(start, end, hn)
        return self.solution

    def core(self, start, end, hn):
        paths = {}
        distances = {start: 0}
        queue = []
        heapq.heappush(queue, (0, start))

        while queue:
            _, current_node = heapq.heappop(queue)

            if current_node == end:
                return self._reconstruct_path(paths, current_node)

            for neighbor in self.maze.grid.neighbors(current_node):
                tentative_g = distances[current_node] + 1
                if neighbor not in distances or tentative_g < distances[neighbor]:
                    distances[neighbor] = tentative_g
                    f = tentative_g + hn(neighbor, end)
                    heapq.heappush(queue, (f, neighbor))
                    paths[neighbor] = current_node

        if end is None:  # Si 'end' es None, reconstruimos los caminos a todos los nodos alcanzados
            for node in distances:
                self.solution[node] = self._reconstruct_path(paths, node)
                

    def _reconstruct_path(self, paths, end):
        path = [end]
        while end in paths:
            end = paths[end]
            path.append(end)
        return path[::-1]

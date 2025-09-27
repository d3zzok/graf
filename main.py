import time
import random
import heapq
import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
import numpy as np


class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []
        self.adjacency_list = {i: [] for i in range(vertices)}
        self.distance_matrix = [[float('Inf')] * vertices for _ in range(vertices)]

        # Инициализация матрицы расстояний для Флойда-Уоршалла
        for i in range(vertices):
            self.distance_matrix[i][i] = 0

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])
        self.adjacency_list[u].append((v, w))
        self.adjacency_list[v].append((u, w))  # для неориентированного графа

        # Обновление матрицы расстояний для Флойда-Уоршалла
        self.distance_matrix[u][v] = w
        self.distance_matrix[v][u] = w

    def bellman_ford(self, src):
        start_time = time.time()

        dist = [float('Inf')] * self.V
        dist[src] = 0
        predecessor = [-1] * self.V

        for _ in range(self.V - 1):
            for u, v, w in self.graph:
                if dist[u] != float('Inf') and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    predecessor[v] = u

        # Проверка на отрицательные циклы
        for u, v, w in self.graph:
            if dist[u] != float('Inf') and dist[u] + w < dist[v]:
                print("Граф содержит отрицательный цикл")
                return None, None, time.time() - start_time

        execution_time = time.time() - start_time
        return dist, predecessor, execution_time

    def dijkstra(self, src):
        start_time = time.time()

        dist = [float('Inf')] * self.V
        dist[src] = 0
        predecessor = [-1] * self.V
        visited = [False] * self.V

        priority_queue = [(0, src)]

        while priority_queue:
            current_dist, u = heapq.heappop(priority_queue)

            if visited[u]:
                continue

            visited[u] = True

            for v, w in self.adjacency_list[u]:
                if not visited[v]:
                    new_dist = current_dist + w
                    if new_dist < dist[v]:
                        dist[v] = new_dist
                        predecessor[v] = u
                        heapq.heappush(priority_queue, (new_dist, v))

        execution_time = time.time() - start_time
        return dist, predecessor, execution_time

    def floyd_warshall(self):
        start_time = time.time()

        # Создаем копию матрицы расстояний
        dist = [row[:] for row in self.distance_matrix]
        next_node = [[-1] * self.V for _ in range(self.V)]

        # Инициализация матрицы next_node
        for i in range(self.V):
            for j in range(self.V):
                if i != j and dist[i][j] != float('Inf'):
                    next_node[i][j] = j
                else:
                    next_node[i][j] = -1

        # Алгоритм Флойда-Уоршалла
        for k in range(self.V):
            for i in range(self.V):
                for j in range(self.V):
                    if dist[i][k] != float('Inf') and dist[k][j] != float('Inf'):
                        if dist[i][j] > dist[i][k] + dist[k][j]:
                            dist[i][j] = dist[i][k] + dist[k][j]
                            next_node[i][j] = next_node[i][k]

        execution_time = time.time() - start_time
        return dist, next_node, execution_time

    def get_path(self, predecessor, target):
        path = []
        current = target

        while current != -1:
            path.append(current)
            current = predecessor[current]

        return path[::-1]

    def get_floyd_path(self, next_node, source, target):
        if next_node[source][target] == -1:
            return []

        path = [source]
        while source != target:
            source = next_node[source][target]
            path.append(source)

        return path


def input_graph_manual():
    """Ручной ввод графа пользователем"""
    print("\n=== РУЧНОЙ ВВОД ГРАФА ===")

    while True:
        try:
            V = int(input("Введите количество вершин: "))
            if V <= 0:
                print("Количество вершин должно быть положительным числом!")
                continue
            break
        except ValueError:
            print("Пожалуйста, введите целое число!")

    graph = Graph(V)

    print("\nВведите ребра графа (формат: u v w)")
    print("Где u - начальная вершина, v - конечная вершина, w - вес")
    print("Для завершения ввода введите 'end'")

    edge_count = 0
    while True:
        try:
            user_input = input(f"Ребро {edge_count + 1}: ").strip()
            if user_input.lower() == 'end':
                if edge_count == 0:
                    print("Граф должен содержать хотя бы одно ребро!")
                    continue
                break

            parts = user_input.split()
            if len(parts) != 3:
                print("Неверный формат! Используйте: u v w")
                continue

            u, v, w = int(parts[0]), int(parts[1]), int(parts[2])

            if u < 0 or u >= V or v < 0 or v >= V:
                print(f"Вершины должны быть в диапазоне [0, {V - 1}]!")
                continue

            if w <= 0:
                print("Вес должен быть положительным числом!")
                continue

            graph.add_edge(u, v, w)
            edge_count += 1
            print(f"Добавлено ребро: {u} -> {v} (вес: {w})")

        except ValueError:
            print("Ошибка ввода! Убедитесь, что вводите целые числа.")
        except KeyboardInterrupt:
            print("\nВвод прерван пользователем.")
            break

    print(f"\nГраф создан: {V} вершин, {edge_count} ребер")
    return graph


def input_graph_auto():
    """Автоматическая генерация графа"""
    print("\n=== АВТОМАТИЧЕСКАЯ ГЕНЕРАЦИЯ ГРАФА ===")

    while True:
        try:
            V = int(input("Введите количество вершин: "))
            if V <= 0:
                print("Количество вершин должно быть положительным числом!")
                continue

            # Предлагаем разумное количество ребер
            max_edges = V * (V - 1) // 2
            suggested_edges = min(V * 3, max_edges)

            E = int(input(f"Введите количество ребер (макс: {max_edges}, рекомендовано: {suggested_edges}): "))
            if E < V - 1:
                print(f"Для связности графа нужно минимум {V - 1} ребер!")
                continue
            if E > max_edges:
                print(f"Максимальное количество ребер для {V} вершин: {max_edges}")
                continue

            max_weight = int(input("Введите максимальный вес ребра (по умолчанию 100): ") or "100")
            break
        except ValueError:
            print("Пожалуйста, введите целое число!")

    graph = generate_random_graph(V, E, max_weight)
    print(f"\nСгенерирован граф: {V} вершин, {E} ребер")
    return graph


def generate_random_graph(vertices, edges, max_weight=100):
    graph = Graph(vertices)

    # Гарантируем связность графа
    for i in range(1, vertices):
        weight = random.randint(1, max_weight)
        graph.add_edge(i - 1, i, weight)

    # Добавляем случайные ребра
    added_edges = vertices - 1
    attempts = 0
    max_attempts = edges * 10  # Ограничение на попытки

    while added_edges < edges and attempts < max_attempts:
        u = random.randint(0, vertices - 1)
        v = random.randint(0, vertices - 1)
        if u == v:
            continue

        # Проверяем, нет ли уже такого ребра
        edge_exists = False
        for edge in graph.graph:
            if (edge[0] == u and edge[1] == v) or (edge[0] == v and edge[1] == u):
                edge_exists = True
                break

        if not edge_exists:
            weight = random.randint(1, max_weight)
            graph.add_edge(u, v, weight)
            added_edges += 1

        attempts += 1

    if added_edges < edges:
        print(f"Предупреждение: добавлено только {added_edges} из {edges} ребер (ограничение плотности графа)")

    return graph


def run_algorithms_on_graph(graph):
    """Запуск алгоритмов на заданном графе"""
    print("\n=== ЗАПУСК АЛГОРИТМОВ ===")

    # Показываем информацию о графе
    print(f"Граф: {graph.V} вершин, {len(graph.graph)} ребер")

    # Ввод начальной и конечной вершин
    while True:
        try:
            source = int(input(f"Введите начальную вершину (0-{graph.V - 1}): "))
            if source < 0 or source >= graph.V:
                print(f"Вершина должна быть в диапазоне [0, {graph.V - 1}]!")
                continue

            target = int(input(f"Введите конечную вершину (0-{graph.V - 1}): "))
            if target < 0 or target >= graph.V:
                print(f"Вершина должна быть в диапазоне [0, {graph.V - 1}]!")
                continue

            if source == target:
                print("Начальная и конечная вершины не должны совпадать!")
                continue

            break
        except ValueError:
            print("Пожалуйста, введите целое число!")

    print(f"\nПоиск кратчайшего пути от вершины {source} до вершины {target}")
    print("-" * 50)

    # Запускаем алгоритмы
    algorithms = [
        ("Беллман-Форд", graph.bellman_ford),
        ("Дейкстра", graph.dijkstra),
        ("Флойд-Уоршалл", lambda src: graph.floyd_warshall())
    ]

    results = []

    for name, algorithm in algorithms:
        print(f"\n{name}:")
        print("-" * 30)

        start_time = time.time()

        if name == "Флойд-Уоршалл":
            dist_matrix, next_node, exec_time = algorithm(source)
            if dist_matrix is not None:
                path = graph.get_floyd_path(next_node, source, target)
                distance = dist_matrix[source][target]
                print(f"Кратчайшее расстояние: {distance}")
                print(f"Путь: {' -> '.join(map(str, path))}")
                print(f"Время выполнения: {exec_time:.6f} сек")
                results.append((name, exec_time, path, distance))
        else:
            dist, pred, exec_time = algorithm(source)
            if dist is not None:
                path = graph.get_path(pred, target)
                print(f"Кратчайшее расстояние: {dist[target]}")
                print(f"Путь: {' -> '.join(map(str, path))}")
                print(f"Время выполнения: {exec_time:.6f} сек")
                results.append((name, exec_time, path, dist[target]))

        # Проверяем, достижима ли конечная вершина
        if name != "Флойд-Уоршалл" and dist[target] == float('Inf'):
            print(f"Вершина {target} недостижима из вершины {source}!")

    # Визуализация для небольших графов
    if graph.V <= 20:
        visualize_graph_with_paths(graph, results, source, target)

    return results


def visualize_graph_with_paths(graph, results, source, target):
    """Визуализация графа с путями от всех алгоритмов"""
    try:
        G = nx.Graph()

        for u, v, w in graph.graph:
            G.add_edge(u, v, weight=w)

        pos = nx.spring_layout(G, seed=42)

        # Создаем субплотов для каждого алгоритма
        fig, axes = plt.subplots(1, len(results), figsize=(5 * len(results), 4))
        if len(results) == 1:
            axes = [axes]

        colors = ['red', 'blue', 'green']

        for i, (name, exec_time, path, distance) in enumerate(results):
            ax = axes[i]

            # Рисуем все ребра
            nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.2, edge_color='gray')

            # Выделяем путь
            if len(path) > 1:
                path_edges = [(path[j], path[j + 1]) for j in range(len(path) - 1)]
                nx.draw_networkx_edges(G, pos, edgelist=path_edges,
                                       ax=ax, edge_color=colors[i], width=3)

            # Рисуем узлы
            nx.draw_networkx_nodes(G, pos, ax=ax, node_color='lightblue',
                                   node_size=400)

            # Выделяем начальную и конечную вершины
            nx.draw_networkx_nodes(G, pos, nodelist=[source], ax=ax,
                                   node_color='green', node_size=500)
            nx.draw_networkx_nodes(G, pos, nodelist=[target], ax=ax,
                                   node_color='red', node_size=500)

            nx.draw_networkx_labels(G, pos, ax=ax, font_size=8)

            ax.set_title(f'{name}\nВремя: {exec_time:.4f} сек\nРасстояние: {distance}',
                         fontsize=10)
            ax.axis('off')

        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Ошибка при визуализации: {e}")


def performance_comparison():
    """Сравнение производительности алгоритмов"""
    print("\n=== СРАВНЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ ===")

    sizes = [50, 100, 200, 300]
    bellman_times = []
    dijkstra_times = []
    floyd_times = []

    for V in sizes:
        E = V * 3

        print(f"Тестирование на графе с {V} вершинами...")
        graph = generate_random_graph(V, E)
        source = 0
        target = min(10, V - 1)

        # Беллман-Форд
        _, _, bellman_time = graph.bellman_ford(source)
        bellman_times.append(bellman_time)

        # Дейкстра
        _, _, dijkstra_time = graph.dijkstra(source)
        dijkstra_times.append(dijkstra_time)

        # Флойд-Уоршалл (только для небольших графов)
        if V <= 200:
            _, _, floyd_time = graph.floyd_warshall()
            floyd_times.append(floyd_time)
        else:
            floyd_times.append(float('nan'))

    # Построение графика
    plt.figure(figsize=(10, 6))

    valid_sizes = [sizes[i] for i in range(len(sizes)) if not np.isnan(floyd_times[i])]
    valid_floyd = [floyd_times[i] for i in range(len(sizes)) if not np.isnan(floyd_times[i])]

    plt.plot(sizes, bellman_times, 'ro-', label='Беллман-Форд')
    plt.plot(sizes, dijkstra_times, 'bo-', label='Дейкстра')
    if valid_sizes:
        plt.plot(valid_sizes, valid_floyd, 'go-', label='Флойд-Уоршалл')

    plt.xlabel('Количество вершин')
    plt.ylabel('Время выполнения (сек)')
    plt.title('Сравнение производительности алгоритмов')
    plt.legend()
    plt.grid(True)
    plt.yscale('log')
    plt.show()


def main_menu():
    """Главное меню программы"""
    graph = None

    while True:
        print("\n" + "=" * 50)
        print("ЛАБОРАТОРНАЯ РАБОТА: АЛГОРИТМЫ ДИНАМИЧЕСКОЙ МАРШРУТИЗАЦИИ")
        print("=" * 50)
        print("1. Ввести граф вручную")
        print("2. Сгенерировать граф автоматически")
        print("3. Запустить алгоритмы на текущем графе")
        print("4. Сравнение производительности алгоритмов")
        print("5. Показать информацию о графе")
        print("6. Выход")

        choice = input("\nВыберите опцию (1-6): ").strip()

        if choice == '1':
            graph = input_graph_manual()

        elif choice == '2':
            graph = input_graph_auto()

        elif choice == '3':
            if graph is None:
                print("Сначала создайте граф (опции 1 или 2)!")
            else:
                run_algorithms_on_graph(graph)

        elif choice == '4':
            performance_comparison()

        elif choice == '5':
            if graph is None:
                print("Граф не создан!")
            else:
                print(f"\nИнформация о графе:")
                print(f"Количество вершин: {graph.V}")
                print(f"Количество ребер: {len(graph.graph)}")
                print("Ребра графа:")
                for u, v, w in graph.graph:
                    print(f"  {u} -> {v} (вес: {w})")

        elif choice == '6':
            print("Выход из программы...")
            break

        else:
            print("Неверный выбор! Пожалуйста, выберите опцию от 1 до 6.")


if __name__ == "__main__":
    main_menu()

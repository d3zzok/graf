import time
import random
from main import Graph, generate_random_graph


def stress_test():
    """Стресс-тест на больших графах"""
    print("СТРЕСС-ТЕСТ НА БОЛЬШИХ ГРАФАХ")
    print("=" * 50)

    test_cases = [
        (100, 500),
        (200, 1000),
        (500, 2500),
        (1000, 5000)
    ]

    for V, E in test_cases:
        print(f"\nТестируем граф: {V} вершин, {E} ребер")

        graph = generate_random_graph(V, E)
        source = 0
        target = min(50, V - 1)  # Чтобы не слишком далеко

        # Беллман-Форд
        start_time = time.time()
        dist_bf, pred_bf, _ = graph.bellman_ford(source)
        time_bf = time.time() - start_time

        # Дейкстра
        start_time = time.time()
        dist_dijkstra, pred_dijkstra, _ = graph.dijkstra(source)
        time_dijkstra = time.time() - start_time

        print(f"Беллман-Форд: {time_bf:.4f} сек")
        print(f"Дейкстра: {time_dijkstra:.4f} сек")
        print(f"Ускорение: {time_bf / time_dijkstra:.2f}x")

        # Проверка корректности
        if dist_bf[target] == dist_dijkstra[target]:
            print("✓ Результаты совпадают")
        else:
            print("✗ Результаты различаются!")


def negative_weight_test():
    """Тест с отрицательными весами"""
    print("\nТЕСТ С ОТРИЦАТЕЛЬНЫМИ ВЕСАМИ")
    print("=" * 50)

    graph = Graph(5)
    # Граф с отрицательными весами, но без отрицательных циклов
    edges = [
        (0, 1, 2), (0, 2, 4), (1, 2, -1),
        (1, 3, 3), (2, 3, 1), (2, 4, 5), (3, 4, 2)
    ]

    for u, v, w in edges:
        graph.add_edge(u, v, w)

    print("Беллман-Форд (работает с отрицательными весами):")
    dist_bf, pred_bf, time_bf = graph.bellman_ford(0)
    print(f"Расстояния: {dist_bf}")

    print("\nДейкстра (не работает с отрицательными весами):")
    try:
        dist_dijkstra, pred_dijkstra, time_dijkstra = graph.dijkstra(0)
        print(f"Расстояния: {dist_dijkstra}")
        print("Внимание: Результат может быть некорректным!")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    stress_test()
    negative_weight_test()

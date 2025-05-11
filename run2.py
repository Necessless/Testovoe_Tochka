import sys
import collections
import heapq
import time 
def get_input():
    """Чтение данных из стандартного ввода."""
    return [list(line.strip()) for line in sys.stdin]

def key_to_bit(value):
    """
    Преобразование значения ключа по алфавиту в битовую маску.
    """
    return 1 << (ord(value) - ord('a'))

def find_paths(x, y, map):
    """
    Реализация обхода лабиринта в ширину для построения графа.
    Алгоритм принимает координаты узла графа и сам лабиринт. 
    Возвращает все грани исходящие из данной точки графа.
    """
    width = len(map[0])
    height = len(map)
    start_state = ((y,x),0) #храним в деке состояния из координат и битовую маску необходимых ключей, чтобы добраться до данного ключа
    queue = collections.deque()
    moves = [(1,0),(-1,0), (0,1), (0,-1)]
    queue.append((start_state,0)) #добавляем к прошлому кортежу количество шагов

    visited = set()
    visited.add(start_state)

    edges = []

    while queue:
        (((robot_Y, robot_X), required_keys), steps) = queue.popleft()
        for dx, dy in moves:
            new_x = robot_X + dx
            new_y = robot_Y + dy 
            new_pos = (new_y, new_x)
            if new_pos in visited:
                continue
            visited.add(new_pos)
            if not (0 <= new_x < width) or not (0 <= new_y < height):
                continue
            cell = map[new_y][new_x]
            if cell == "#":
                continue 
            if 'A' <= cell <= 'Z':
                required_keys |= key_to_bit(cell.lower()) #добавляем ключ для этой двери в необходимые
            if 'a' <= cell <= 'z':
                if not (new_x == x and new_y == y):
                    edges.append((cell, steps + 1, required_keys)) #добавляем "соседство" между узлами графа
            
            new_state = (new_pos, required_keys)
            queue.append((new_state, steps + 1)) 
    return edges #возвращаем список соседей узла



def count_min_steps(start_positions, graph, map, total_keys, key_positions):
    """
    Реализация алгоритма Дейкстры для подсчета минимального количества шагов по 
    созданному ранее графу.
    """
    start_pos = tuple(start_positions)
    heap = [(0, 0, start_pos, 0)] #используем кучу из heapq чтобы всегда брать элемент с минимальным количеством шагов до него
    distance = {}
    counter = 0 #заводим счетчик, дабы heapq не ругался на сравнение tuple и int

    while heap:
        steps, _, positions, collected_keys = heapq.heappop(heap) #храним в куче шаги, счетчик, позиции соседей, собранные ключи
        state = (positions, collected_keys)
        if state in distance and distance[state] <= steps:
            continue
        distance[state] = steps
        if collected_keys == total_keys:
            return steps
        for index, (pos_Y, pos_X) in enumerate(positions): #проходим в цикле по позициям всех роботов в данный момент
            cell = map[pos_Y][pos_X]
            if cell == "@":
                cell = "@" + str(pos_X) + str(pos_Y) #дабы уникально идентифицировать каждого робота
            for key, cost, doors in graph[cell]: #проходим по каждому соседу данной точки
                bit_key = key_to_bit(key) #переводим ключ в биты 
                if collected_keys & bit_key: #если ключ уже собран, то переходим дальше
                    continue
                if (doors & ~collected_keys) != 0: #если нет необходимого ключа для дверей, то переходим дальше
                    continue
                new_positions = list(positions)
                new_positions[index] = key_positions[key] #переходим в следующую вершину графа
                counter += 1
                heapq.heappush(heap, (steps + cost, counter, tuple(new_positions), collected_keys | bit_key)) 
    return -1

def min_steps_to_collect_all_keys():
    """
    Решение задачи с использованием алгоритмов обхода лабиринта в ширину и Дейкстры.
    Использует битовую маску для хранения ключей и дверей для ускорения алгоритма.
    Сперва строим граф от роботов к ключам и от ключей к другим ключам, попутно считая необходимые двери.
    А затем находим минимальное количество шагов по графу. 
    """
    data = get_input()
    total_keys = 0  #используем битовую маску вместо множества для ускорения алгоритма
    graph = {}
    start_positions = []
    key_positions = {} #позиции ключей, для их дальнейшего использования в алгоритме
    for indexY,string in enumerate(data):
        for indexX, el  in enumerate(string):
            if el == "#" or el == ".":
                continue
            if el == "@":
                pos = el + str(indexX) + str(indexY) #опять же добавляем опознавательные символы каждому роботу
                start_positions.append((indexY, indexX))
                graph[pos] = find_paths(indexX, indexY, data) #строим ребра к соседям для каждого робота
            if 'a' <= el <= 'z':
                total_keys |= key_to_bit(el) #добавляем битовый ключ в маску
                key_positions[el] = (indexY, indexX)
                graph[el] = find_paths(indexX, indexY, data) #строим ребра до каждого соседа ключа
    min_steps = count_min_steps(start_positions, graph, data,total_keys, key_positions) #считаем минимальное количество шагов по графу
    print(min_steps)
        

if __name__ == '__main__':
    min_steps_to_collect_all_keys()
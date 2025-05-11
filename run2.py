import sys
import time 
import collections


def get_input():
    """Чтение данных из стандартного ввода."""
    return [list(line.strip()) for line in sys.stdin]

def convert_key_to_bit(key):
    return 1 << ord(key) - ord('a')

def min_steps_to_collect_all_keys(data):
    """
    Минимальное решение задачи, рассчитываю сделать другое, если успею конечно. 
    Вычисляет позиции роботов и хранит битовую маску ключей, которые нужно найти.
    Далее запускает небольшую модификацию алгоритма обхода б. дерева в ширину, храня позиции всех роботов. 
    Работает очень медленно, больше чем за минуту решает лабиринт 100x100. 
    Планирую сделать решение таковым:
    с помощью обхода в ширину найдем пути до ключей для каждого робота. Затем через алгоритм Дейкстры найдем минимальную сумму шагов. 
    """
    keys = 0
    robots = []
    max_Y = len(data) - 1
    min_Y = 0 
    max_X = len(data[0]) - 1
    min_X = 0
    moves = [(1,0),(-1,0), (0,1), (0,-1)]

    for indexY,string in enumerate(data):
        for indexX, el  in enumerate(string):
            if el == "#" or el == ".":
                continue
            if el == "@":
                robots.append((indexY, indexX))
                continue
            if 97 <= ord(el) <= 122:
                order = convert_key_to_bit(el)
                keys |= order
     
    queue = collections.deque()
    start_position = (tuple(robots), 0)
    queue.append((start_position, 0))
    visited = set()
    visited.add(start_position)

    while queue: 
        (robot_positions, collected_keys), steps_count = queue.popleft()
         
        if collected_keys == keys:
            return steps_count 
        
        for index, (robotY, robotX) in enumerate(robot_positions):
            for dx, dy in moves:
                new_x = robotX + dx
                new_y = robotY + dy 

                new_keys = collected_keys
                map_position = data[new_y][new_x]

                if not (min_X <= new_x <= max_X) or not (min_Y <= new_y <= max_Y):
                    continue

                if map_position == "#":
                    continue

                if "a" <= map_position <= "z":
                    new_keys |= convert_key_to_bit(map_position)
                
                if "A" <= map_position <= "Z":
                    if not (collected_keys & convert_key_to_bit(map_position.lower())):
                        continue

                new_positions = list(robot_positions)
                new_positions[index] = (new_y, new_x)
                new_state = (tuple(new_positions), new_keys)

                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, steps_count + 1))
    return -1





def main():
    data = get_input()
    start = time.time()
    result = min_steps_to_collect_all_keys(data)
    print(time.time() - start)


if __name__ == '__main__':
    main()
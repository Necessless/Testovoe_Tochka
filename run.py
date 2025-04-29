import json
from datetime import datetime 


def check_capacity(max_capacity: int, guests: list) -> bool:
    """
    Итоговая сложность O(n*log(n)).

    Принцип работы:
    Алгоритм сперва сортирует список за O(n*log(n)) по дате выезда гостя,
    переводя строку в дейттайм.
    Далее заводим указатель на минимальную дату выезда среди заселенных гостей.
    Также счетчик для заселения начальных гостей в пустой отель.
    В цикле за O(n) сравниваем дату заезда гостя с минимальной датой выезда,
    если она больше либо равна, то гостя заселяем.
    Увеличиваем указатель на один, чтобы снова получить минимальную дату выезда.
    Счетчик при этом остается неизменным, так как +1 -1 разницы не сделает.
    """
    guests.sort(key=lambda x: datetime.strptime(x['check-out'], "%Y-%m-%d"))
    curr = 0
    pt = 0 #указатель на заселенного с минимальной датой выезда гостя
    for guest in guests:
        curr_in = datetime.strptime(guest['check-in'], "%Y-%m-%d")
        min_out = datetime.strptime(guests[pt]['check-out'], "%Y-%m-%d")
        if curr < max_capacity: 
            curr += 1
            continue
        if curr_in >= min_out: #передвигаем указатель, если нынешний гость может быть заселён
            pt += 1
        else:
            return False
    return True


if __name__ == "__main__":
    max_capacity = int(input())
    n = int(input())
    guests = []
    for _ in range(n):
        guest_json = input()
        guest_data = json.loads(guest_json)
        guests.append(guest_data)
    result = check_capacity(max_capacity, guests)
    print(result)
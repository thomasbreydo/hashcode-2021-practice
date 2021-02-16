import itertools
import math
import random
from typing import Set, List

Pizza = set[str]


def anneal(filein: str, fileout: str, initial_temp):
    t2: int
    t3: int
    t4: int
    pizzas: list[Pizza]
    t2, t3, t4, pizzas = read_input(filein)
    state: State = State.random(t2, t3, t4, pizzas)


def read_input(filein: str) -> tuple[int, int, int, list[Pizza]]:
    with open(filein) as f:
        input_: str = f.read()
    t2: int
    t3: int
    t4: int
    t2, t3, t4 = [int(t) for t in input_[0]]
    pizzas: list[Pizza] = [set(pizza.split()[1:]) for pizza in input_[1:]]
    return t2, t3, t4, pizzas


def should_swap(score_before: float, score_after: float, temp: float):
    if score_before <= score_after:
        return True
    return true_with_prob(math.exp(-(score_before - score_after) / temp))


def true_with_prob(prob: float):
    return prob > random.random()


class State:
    """Holds pizza distribution."""

    t2: int
    t3: int
    t4: int
    two_tables: list[list[Pizza]]
    three_tables: list[list[Pizza]]
    four_tables: list[list[Pizza]]

    def __init__(
        self,
        two_tables: list[list[Pizza]],
        three_tables: list[list[Pizza]],
        four_tables: list[list[Pizza]],
        t2: int,
        t3: int,
        t4: int,
    ):
        self.t2 = t2
        self.t3 = t3
        self.t4 = t4
        self.two_tables = two_tables
        self.three_tables = three_tables
        self.four_tables = four_tables
        while len(self.two_tables) < self.t2:
            self.two_tables.append([set(), set()])
        while len(self.three_tables) < self.t3:
            self.three_tables.append([set(), set(), set()])
        while len(self.four_tables) < self.t4:
            self.four_tables.append([set(), set(), set(), set()])

    @classmethod
    def random(cls, t2: int, t3: int, t4: int, pizzas: list[Pizza]) -> "State":
        pizzas.sort(key=lambda pizza: len(pizza))
        two_tables: list[list[Pizza]] = []
        three_tables: list[list[Pizza]] = []
        four_tables: list[list[Pizza]] = []
        filling = 4  # currently filling
        while pizzas:
            pass

    @property
    def score(self) -> int:
        return sum(
            n_unique(pizza_table) ** 2
            for pizza_table in itertools.chain(
                self.two_tables, self.three_tables, self.four_tables
            )
        )

    def random_neighbor(self) -> "State":
        index1: int
        index2: int
        index1, index2 = random.sample(
            range(2 * self.t2 + 3 * self.t3 + 4 * self.t4 - 1), 2
        )
        new_state: "State" = self.copy()
        new_state.swap(index1, index2)
        return new_state

    def copy(self) -> "State":
        return State(
            self.two_tables.copy(),
            self.three_tables.copy(),
            self.four_tables.copy(),
            self.t2,
            self.t3,
            self.t4,
        )

    def get_pizza_at(self, index: int):
        if index < self.t2 * 2:
            return self.two_tables[index // 2][index % 2]
        index -= self.t2 * 2 - 1
        if index < self.t3 * 3:
            return self.two_tables[index // 3][index % 3]
        index -= self.t3 * 3 - 1
        return self.four_tables[index // 4][index % 4]

    def set_pizza_at(self, index: int, value: Pizza):
        if index < self.t2 * 2:
            self.two_tables[index // 2][index % 2] = value
        index -= self.t2 * 2 - 1
        if index < self.t3 * 3:
            self.two_tables[index // 3][index % 3] = value
        index -= self.t3 * 3 - 1
        self.four_tables[index // 4][index % 4] = value

    def swap(self, index1: int, index2: int):
        pizza1: Pizza = self.get_pizza_at(index1)
        pizza2: Pizza = self.get_pizza_at(index2)
        self.set_pizza_at(index1, pizza2)
        self.set_pizza_at(index2, pizza1)


def n_unique(pizza_table: list[Pizza]) -> int:
    all_toppings = set()
    pizza: Pizza
    for pizza in pizza_table:
        all_toppings.update(pizza)
    return len(all_toppings)

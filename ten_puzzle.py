import itertools
from typing import List, Any, Callable
import random
import pickle
import re
import os
import time

EASY_DATA = "./ten_puzzle_easy.txt"
EASY_ANS = "./ten_puzzle_easy_r.txt"


def random_list(n):
    return [random.randint(1, 9) for _ in range(n)]


def ten_puzzle_maker(n=4, m=10):
    time_sta = time.perf_counter()
    cnt = 0
    while True:
        if cnt == 1000:
            return None, None
        if time.perf_counter() - time_sta > 10:
            return None, None
        l = random_list(n)
        puzzle = TenPuzzle(n, m, l)
        if puzzle.is_easy():
            continue
        if puzzle.solve() != "":
            l.sort()
            # パズルが完成した
            f = open(EASY_DATA, "wb")
            pickle.dump(l, f)
            f = open(EASY_ANS, "wb")
            pickle.dump(m, f)
            return l, m
        cnt += 1


def ten_puzzle_clear():
    os.remove(EASY_DATA)
    os.remove(EASY_ANS)


def is_equation(s: str) -> bool:
    # 正規表現を使用して、与えられた文字列が指定された文字だけで構成されているかをチェックします
    # [1-9]は1から9までの数字、[-+*/()]は指定された記号を意味します
    pattern = r"^[1-9\-+*/()]+$"
    return bool(re.match(pattern, s))


def judge(e: str) -> int:
    """judge ten puzzle answer

    Args:
        e (str): equation string

    Returns:
        int: judge result
    """
    if os.path.isfile(EASY_DATA):
        input_numbers = [int(digit) for digit in re.findall(r"\d", e)]
        input_numbers.sort()
        f = open(EASY_DATA, "rb")
        list_row = list(pickle.load(f))
        list_row.sort()
        print("[ten_puzzle] input is", input_numbers, ", data is", list_row)
        if input_numbers != list_row:
            # ERROR INCOLLECT NUMBER
            return 1
        else:
            from .calc import in_and_out

            ans: float = in_and_out(e)
            f = open(EASY_ANS, "rb")
            d_ans = int(pickle.load(f))
            print("[ten_puzzle] input ans is", ans, ", data ans is", d_ans)

            if ans == d_ans:
                return 0
            else:
                # ERROR INCOLLECT ANSWER
                return 2
        # ERROR UNDEFINED
        return -2
    else:
        # FILE NOT FOUND
        return -1


class TenPuzzle:
    n: int
    m: float
    a: List[float]
    calc: List[Callable[[float, float], float]] = [
        lambda a, b: a + b,
        lambda a, b: a - b,
        lambda a, b: a * b,
        lambda a, b: a / b,
    ]
    sign = ["+", "-", "x", "/"]
    time_counter: float

    def __init__(self, n, m, a):
        self.n = n
        self.m = m
        self.a = a
        self.time_counter = 0

    def solver(self, arr) -> List[Any]:
        if self.time_counter == 0:
            self.time_counter = time.perf_counter()
        if time.perf_counter() - self.time_counter > 1:
            return []

        if len(arr) == 2:
            ans: List[Any] = []
            for i in range(len(self.calc)):
                try:
                    if self.calc[i](arr[0], arr[1]) == self.m:
                        ans.extend(["(", str(arr[0]), self.sign[i], str(arr[1]), ")"])
                        return ans
                except ZeroDivisionError:
                    return []
            return ans

        for i in range(len(arr) - 1):
            for j in range(len(self.calc)):
                try:
                    next: List[float] = (
                        arr[:i] + [self.calc[j](arr[i], arr[i + 1])] + arr[i + 2 :]
                    )
                except ZeroDivisionError:
                    return []
                ans = self.solver(next)
                if time.perf_counter() - self.time_counter > 1:
                    return []
                if len(ans) != 0:
                    try:
                        calc_result = self.calc[j](arr[i], arr[i + 1])
                    except ZeroDivisionError:
                        return []
                    k = ans.index(str(calc_result))
                    ans[k : k + 1] = [
                        "(",
                        str(arr[i]),
                        self.sign[j],
                        str(arr[i + 1]),
                        ")",
                    ]
                    return ans
        return []

    def is_easy(self) -> bool:
        # + or -で完成してしまう場合はTrue
        max_value: int = int(sum(self.a))
        if max_value < self.m:
            return False
        if (max_value - self.m) % 2 == 1:
            return False
        sa: int = (max_value - int(self.m)) // 2
        napsac: List[int] = [0] * (sa + 1)
        napsac[0] = 1
        for i in range(len(self.a)):
            for j in range(len(napsac)):
                if napsac[j] > 0 and j + self.a[i] < len(napsac):
                    napsac[j + int(self.a[i])] = 1
        if napsac[sa] == 1:
            return True
        else:
            return False

    def print(self, a: List[Any]):
        # 最外の括弧を外す
        del a[0]
        del a[len(a) - 1]
        for i in range(len(a) - 1, 1, -1):
            if a[i] == "+" or a[i] == "-":
                if a[i - 1] == ")":
                    # この括弧はいらない
                    del a[i - 1]
                    imos = 0
                    for j in range(i - 2, -1, -1):
                        if a[j] == ")":
                            imos += 1
                        if a[j] == "(":
                            if imos == 0:
                                del a[j]
                                break
                            else:
                                imos -= 1

        # print(''.join(a))
        return "".join(a)

    def solve(self):
        perm = list(itertools.permutations(self.a))
        for x in perm:
            x = list(x)
            ans = self.solver(x)
            if len(ans) != 0:
                return self.print(ans)
        return ""


if __name__ == "__main__":
    numbers, result = ten_puzzle_maker()
    print(numbers, result)
    print(judge("1+2+3+4"))


import sqlite3
import dogify_cli as c


def sum(a, b):
    print(a + b)


def mul(a, b):
    print(a * b)


c.register_functions(
    "sum", lambda a, b: sum(float(a), float(b)),
    "mul", lambda a, b: mul(float(a), float(b)))


if __name__ == '__main__':
    c.init()

import math
import random
from collections import OrderedDict

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.help_docs = {
            "pr": "pr(expr) - выводит значение выражения (print)",
            "ind": "ind() - ввод с клавиатуры (input)",
            "st": "st(expr) - преобразует в строку (str)",
            "in": "in(expr) - преобразует в целое (int)",
            "len": "len(expr) - длина строки/списка",
            "sr": "sr(expr) - разворот строки (reverse)",
            "square": "square(expr) - возводит в квадрат",
            "nosq": "nosq(expr) - проверка ненулевого (expr/expr)",
            "help": "help([name]) - справка по функциям",
            "bit": "bit(expr) - двоичное представление",
            "ab": "ab(expr) - абсолютное значение (abs)",
            "mx": "mx(...) - максимум (max)",
            "mn": "mn(...) - минимум (min)",
            "sm": "sm(...) - сумма (sum)",
            "fl": "fl(expr) - число с плавающей (float)",
            "rn": "rn(expr) - округление (round)",
            # Новые Python
            "list": "list(...) - создает список",
            "dict": "dict(key1,val1,key2,val2...) - словарь",
            "range": "range(start,end) - диапазон",
            "sort": "sort(list) - сортировка",
            "rev": "rev(list/str) - разворот",
            # C++ стиль
            "cout": "cout(expr) - C++ стиль вывода",
            "vec": "vec(size) - вектор (список)",
            "arr": "arr(size,val) - массив",
            # Rust стиль
            "vec!": "vec!(size) - Rust вектор",
        }

    def evaluate(self, node):
        if node is None:
            return None

        if node.type == "NUMBER":
            return node.value
        elif node.type == "STRING":
            return node.value
        elif node.type == "ASSIGN":
            value = self.evaluate(node.right)
            self.variables[node.value] = value
            return value
        elif node.type == "ID":
            if node.value in self.variables:
                return self.variables[node.value]
            raise Exception(f"Неизвестная переменная '{node.value}'")
        
        # Арифметика
        elif node.type == "PLUS":
            return self.evaluate(node.left) + self.evaluate(node.right)
        elif node.type == "MINUS":
            return self.evaluate(node.left) - self.evaluate(node.right)
        elif node.type == "MUL":
            return self.evaluate(node.left) * self.evaluate(node.right)
        elif node.type == "DIV":
            divisor = self.evaluate(node.right)
            if divisor == 0:
                raise Exception("Деление на ноль!")
            return self.evaluate(node.left) / divisor

        # Функции
        elif node.type in self.help_docs:
            args = [self.evaluate(arg) for arg in (node.children or [])]
            return self.call_builtin(node.type, args)
        
        elif node.type == "FUNC_CALL":
            func_name = node.value
            args = [self.evaluate(arg) for arg in (node.children or [])]
            if func_name in self.functions:
                return self.functions[func_name](*args)
            raise Exception(f"Неизвестная функция '{func_name}'")

    def call_builtin(self, func_name, args):
        if func_name == "PR" or func_name == "CPP_PRINT":
            print(*args)
            return args[0] if args else None
        elif func_name == "IND":
            return input(">> ")
        elif func_name == "ST":
            return str(args[0]) if args else ""
        elif func_name == "IN":
            return int(float(args[0])) if args else 0
        elif func_name == "LEN":
            return len(args[0]) if args else 0
        elif func_name == "SR":
            return str(args[0])[::-1] if args else ""
        elif func_name == "SQUARE":
            return args[0] ** 2 if args else 0
        elif func_name == "SQ":
            val = args[0] if args else 0
            return val / val if val != 0 else 0
        elif func_name == "HELP":
            if not args:
                print("=== СПРАВКА ===")
                for k, v in self.help_docs.items():
                    print(f"{k}: {v}")
            else:
                name = str(args[0]).lower()
                print(self.help_docs.get(name, f"Функция '{name}' не найдена"))
            return None
        elif func_name == "BIT":
            return bin(int(args[0]))[2:] if args else "0"
        elif func_name == "AB":
            return abs(args[0]) if args else 0
        elif func_name == "MX":
            return max(args) if args else 0
        elif func_name == "MN":
            return min(args) if args else 0
        elif func_name == "SM":
            return sum(args) if args else 0
        elif func_name == "FL":
            return float(args[0]) if args else 0.0
        elif func_name == "RN":
            return round(args[0]) if args else 0
        # Новые Python
        elif func_name == "LIST":
            return list(args)
        elif func_name == "DICT":
            d = {}
            for i in range(0, len(args), 2):
                if i+1 < len(args):
                    d[str(args[i])] = args[i+1]
            return d
        elif func_name == "RANGE":
            return list(range(int(args[0]), int(args[1]) if len(args)>1 else args[0]+10))
        elif func_name == "SORT":
            lst = args[0] if isinstance(args[0], list) else list(args[0])
            lst.sort()
            return lst
        elif func_name == "REV":
            return list(reversed(args[0])) if isinstance(args[0], list) else str(args[0])[::-1]
        # C++
        elif func_name == "VEC":
            return [0] * int(args[0]) if args else []
        elif func_name == "ARR":
            size, val = int(args[0]), args[1] if len(args)>1 else 0
            return [val] * size
        # Rust
        elif func_name == "VEC_NEW":
            return [0] * int(args[0]) if args else []
        
        raise Exception(f"Неизвестная функция '{func_name}'")

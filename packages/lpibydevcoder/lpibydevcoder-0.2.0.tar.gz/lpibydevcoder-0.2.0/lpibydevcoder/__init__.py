"""
LPI - Гибридный язык программирования (Python + C++ + Rust)
Простой интерпретатор с поддержкой 30+ встроенных функций
"""

import sys
import os
from .lexer import tokenize
from .parser import Parser
from .interpreter import Interpreter

def run_code(code, interactive=False):
    """
    Выполняет код LPI языка
    
    Args:
        code (str): Исходный код
        interactive (bool): Интерактивный режим
    
    Returns:
        any: Результат выполнения
    """
    try:
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        result = interpreter.evaluate(ast)
        
        if interactive and result is not None:
            print(f"> {result}")
        return result
    except SyntaxError as e:
        print(f"Синтаксическая ошибка: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Ошибка выполнения: {e}", file=sys.stderr)
        return None

def repl():
    """REPL (Read-Eval-Print Loop) для интерактивной работы"""
    interpreter = Interpreter()
    print("LPI v0.2.0 - Гибридный язык (Python+C++/Rust)")
    print("help() - справка | exit - выход")
    print("-" * 50)
    
    while True:
        try:
            code = input("lpi> ")
            if code.lower() in ('exit', 'quit', 'выход'):
                print("Пока!")
                break
            
            if code.strip():
                tokens = tokenize(code)
                if tokens:  # Проверяем, есть ли токены
                    parser = Parser(tokens)
                    ast = parser.parse()
                    result = interpreter.evaluate(ast)
                    if result is not None:
                        print(result)
                        
        except KeyboardInterrupt:
            print("\nВыход...")
            break
        except EOFError:
            print("\nПока!")
            break
        except Exception as e:
            print(f"Ошибка: {e}")

def run_file(filename):
    """Выполняет файл с кодом LPI"""
    if not os.path.exists(filename):
        print(f"Файл не найден: {filename}", file=sys.stderr)
        return 1
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
        
        print(f"Выполнение файла: {filename}")
        result = run_code(code)
        return 0 if result is not None else 1
    except Exception as e:
        print(f"Ошибка выполнения файла: {e}", file=sys.stderr)
        return 1

def main():
    """Главная функция для CLI"""
    if len(sys.argv) == 1:
        # Интерактивный режим
        repl()
    elif len(sys.argv) == 2:
        filename = sys.argv[1]
        if filename == '-i' or filename == '--interactive':
            repl()
        elif filename == '-h' or filename == '--help':
            print("""
LPI v0.2.0 - Гибридный интерпретатор
Использование:
    lpi                  # REPL режим
    lpi file.lpi         # Выполнить файл
    lpi -i               # Интерактивный режим
    lpi -h               # Справка
Примеры:
    pr(42 + 10)
    x := 5; pr(x * 2)
    help()
            """)
        else:
            # Выполнить файл
            sys.exit(run_file(filename))
    else:
        print("Слишком много аргументов", file=sys.stderr)
        sys.exit(1)

# Глобальные функции для удобства
def lpi_eval(code):
    """Короткая функция для оценки кода"""
    return run_code(code)

# Автоматический запуск при прямом вызове
if __name__ == "__main__":
    main()

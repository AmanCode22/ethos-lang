import os
import sys
from pathlib import Path
from sys import exit

from .executer import create_enviroment, run
from .lexer import lex
from .parser import parse
from .version import stage, version

try:
    import readline
except ImportError:
    import pyreadline3 as readline


def main():
    if len(sys.argv) == 1:
        start_repl()
        exit()
    elif len(sys.argv) != 2:
        print("Usage: ethosrun <filename.ethos>")
        exit()
    filename = sys.argv[1]
    if filename == "--version" or filename == "-v":
        print(f"Ethos {version} {stage}")
        exit(0)
    if not filename.endswith(".ethos"):
        print("Filename must have extension .ethos")
        exit()
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    tokens = lex(data)
    if not tokens or tokens == []:
        exit()
    generated_python_code = parse(tokens)
    if (
        not generated_python_code
        or generated_python_code == ""
        or generated_python_code == " "
    ):
        exit()
    run(generated_python_code)


def start_repl():
    history_path = Path.home() / ".ethos" / ".ethos_history"
    history_path.parent.mkdir(parents=True, exist_ok=True)
    if os.path.exists(history_path):
        readline.read_history_file(history_path)
    repl_memory = create_enviroment()
    buffer = ""
    open_blocks = 0
    while True:
        if open_blocks == 0:
            command_input = input("ethos > ")
        else:
            command_input = input("... ")
        if command_input == "exit" or command_input == "quit":
            readline.write_history_file(history_path)
            break
        if not command_input.endswith("."):
            command_input += "."
        tokens = lex(command_input)
        if not tokens or tokens == []:
            continue
        if tokens[0][0] in ["repeat", "while", "if", "how", "count"]:
            open_blocks += 1
        elif tokens[0][0] == "end" and open_blocks != 0:
            buffer += "end."
            open_blocks -= 1
            tokens = lex(buffer)
            if not tokens or tokens == []:
                buffer = ""
                continue
            python_code = parse(tokens)
            if not python_code or python_code == "" or python_code == " ":
                buffer = ""
                continue
            run(python_code, repl_memory)
            buffer = ""
            continue
        elif open_blocks == 0 and tokens[0][0] == "end":
            readline.write_history_file(history_path)
            exit()
        if open_blocks > 0:
            buffer += command_input + "\n"
            continue
        python_code = parse(tokens)
        if not python_code or python_code == " " or python_code == "":
            continue
        run(python_code, repl_memory)

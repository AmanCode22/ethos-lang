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

BLOCK_OPENERS = {"repeat", "while", "if", "how", "count"}


def main():
    if len(sys.argv) == 1:
        start_repl()
        exit()

    if len(sys.argv) != 2:
        print("Usage: ethos <filename.ethos>")
        exit()

    filename = sys.argv[1]

    if filename in ("--version", "-v"):
        print(f"Ethos {version} {stage}")
        exit(0)

    if not filename.endswith(".ethos"):
        print("Filename must have extension .ethos")
        exit()

    with open(filename, encoding="utf-8") as f:
        data = f.read()

    tokens = lex(data)
    if not tokens:
        exit()

    generated_python_code = parse(tokens)
    if not generated_python_code or generated_python_code.strip() == "":
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
        prompt = "... " if open_blocks > 0 else "ethos > "
        command_input = input(prompt)
        if command_input.strip() in ("exit", "quit"):
            readline.write_history_file(history_path)
            break
        if not command_input.strip().endswith("."):
            command_input+="."
        tokens = lex(command_input)
        if not tokens:
            continue

        first_token = tokens[0][0] if tokens[0] else ""

        if first_token in BLOCK_OPENERS:
            open_blocks += 1

        if first_token == "end":
            if open_blocks == 0:
                readline.write_history_file(history_path)
                exit()
            open_blocks -= 1

        if open_blocks > 0 or first_token == "end":
            buffer += command_input + "\n"

            if open_blocks == 0 and first_token == "end":
                block_tokens = lex(buffer)
                buffer = ""
                if block_tokens:
                    python_code = parse(block_tokens)
                    if python_code and python_code.strip():
                        run(python_code, repl_memory)
            continue

        python_code = parse(tokens)
        if python_code and python_code.strip():
            run(python_code, repl_memory)

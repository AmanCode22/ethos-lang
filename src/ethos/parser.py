def convert_operation(operation):
    mapping = {
        "is": "==",
        "is not": "!=",
        "is above": ">",
        "is below": "<",
        "is at least": ">=",
        "is at most": "<=",
        "and": "and",
        "not": "not",
        "or": "or",
        "plus": "+",
        "minus": "-",
        "times": "*",
        "divided by": "/",
        "to the power of": "**",
    }
    return mapping.get(operation, operation)


def preprocess_tokens(tokens_list):
    multi_words_mapper = [
        "is not",
        "is above",
        "is below",
        "is at least",
        "is at most",
        "divided by",
        "to the power of",
        "bring in",
        "how to",
        "otherwise if",
        "run function",
        "delete variable",
    ]
    i = 0
    processed = []
    while i < len(tokens_list):
        found = False
        for length in [4, 3, 2]:
            phrase = " ".join(tokens_list[i : i + length])
            if phrase in multi_words_mapper:
                processed.append(phrase)
                i += length
                found = True
                break
        if not found:
            processed.append(tokens_list[i])
            i += 1
    return processed


def parse(all_tokens):
    final_code = ""
    indent_level = 0
    python_mode = False
    debug_mode = False

    for sentence in all_tokens:
        tokens = preprocess_tokens(sentence)
        if not tokens:
            continue

        first = tokens[0]

        if first == "python":
            python_mode = True
            continue
        elif first == "pythonend":
            python_mode = False
            continue
        elif first == "debug":
            debug_mode = True
            continue
        elif first == "debugend":
            debug_mode = False
            continue

        if first == "end":
            indent_level -= 1
            if indent_level < 0:
                print("Error: 'end' found without a matching block")
                return ""
            continue

        if first == "otherwise":
            indent_level -= 1

        if indent_level < 0:
            indent_level = 0
        padding = " " * (indent_level * 4)
        line_content = ""

        if first == "note":
            line_content = f"# {' '.join(tokens[1:])}\n"
        elif first in ["notes", "endnotes"]:
            line_content = "'''\n"
        elif first == "say":
            if len(tokens) < 2:
                print("Error: 'say' needs a value")
                return ""
            line_content = f"print({tokens[1]})\n"
        elif first == "set":
            if "from" in tokens and "to" in tokens:
                line_content = f"{tokens[1]} = {tokens[1]}[{tokens[3]}:{tokens[5]}]\n"
            else:
                line_content = f"{tokens[1]} =  {' '.join([convert_operation(t) for t in tokens[3:]])}\n"
        elif first == "add":
            line_content = f"{tokens[-1]} += {' '.join([convert_operation(t) for t in tokens[1 : tokens.index('to')]])}\n"
        elif first == "subtract":
            line_content = f"{tokens[-1]} -= {' '.join([convert_operation(t) for t in tokens[1 : tokens.index('from')]])}\n"
        elif first == "bring in":
            line_content = f"import {tokens[1]}\n"
        elif first == "run":
            if tokens[1] == "function":
                args = (
                    ", ".join([i.rstrip(",") for i in tokens[4:]])
                    if "with" in tokens
                    else ""
                )
                line_content = f"{tokens[2]}({args})\n"
            else:
                args = (
                    ", ".join([i.rstrip(",") for i in tokens[3:]])
                    if "with" in tokens
                    else ""
                )
                line_content = f"{tokens[1]}({args})\n"
        elif first == "how to":
            args = (
                ", ".join(
                    [i.rstrip(",") for i in tokens[tokens.index("with") + 1 : -1]]
                )
                if "with" in tokens
                else ""
            )
            line_content = f"def {tokens[1]}({args}):\n"
        elif first in ["if", "while"]:
            py_kw = "if" if first == "if" else "while"
            cond = " ".join([convert_operation(t) for t in tokens[1:-1]])
            line_content = f"{py_kw} {cond}:\n"
        elif first == "otherwise":
            if len(tokens) > 2 and tokens[1] == "if":
                cond = " ".join([convert_operation(t) for t in tokens[2:-1]])
                line_content = f"elif {cond}:\n"
            else:
                line_content = "else:\n"
        elif first == "repeat":
            line_content = f"for _ in range({tokens[1]}):\n"
        elif first == "count":
            var = tokens[tokens.index("variable") + 1]
            start, end = tokens[2], tokens[4]
            step = tokens[6] if "stepping" in tokens else "1"
            offset = "- 1" if step.startswith("-") else "+ 1"
            line_content = (
                f"for {var} in range({start}, int({end}) {offset}, {step}):\n"
            )
        elif first == "delete variable":
            line_content = f"del {tokens[1]}\n"
        elif first == "ask":
            if not len(tokens) == 4:
                print(
                    "Invalid syntax used, correct syntax is ask 'Prompt string' into variable_name"
                )
                return
            if tokens[2] != "into":
                print(
                    "Invalid syntax used, correct syntax is ask 'Prompt string' into variable_name"
                )
                return
            line_content = f"{tokens[3]} = input({tokens[1]})\n"
        if line_content:
            if debug_mode:
                final_code += f"{padding}print('DEBUG: {' '.join(tokens)}')\n"
            if python_mode:
                final_code += f"{padding}print('PY_GEN: {line_content.strip()}')\n"

            final_code += padding + line_content

            if first in ["how to", "if", "while", "otherwise", "repeat", "count"]:
                indent_level += 1

    return final_code

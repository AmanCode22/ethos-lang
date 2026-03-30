TYPE_CASTS = {
    "to number": "int",
    "to decimal": "float",
    "to text": "str",
    "to boolean": "bool",
    "to list": "list",
    "to tuple": "tuple",
    "to set": "set",
    "to dictionary": "dict",
    "to bytes": "bytes",
    "to complex": "complex",
}


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


def apply_casts(expr, cast_chain):
    for cast in reversed(cast_chain):
        py_func = TYPE_CASTS[cast]
        expr = f"{py_func}({expr})"
    return expr


def preprocess_tokens(tokens_list):
    BLOCK_KEYWORDS = {"end", "otherwise", "if", "while", "repeat", "count", "how"}

    cleaned = []
    for token in tokens_list:
        base = token.rstrip(".")
        if base in BLOCK_KEYWORDS:
            cleaned.append(base)
        else:
            cleaned.append(token)
    tokens_list = cleaned

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
        "to number",
        "to decimal",
        "to text",
        "to boolean",
        "to list",
        "to tuple",
        "to set",
        "to dictionary",
        "to bytes",
        "to complex",
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
            var_name = tokens[1]
            if "from" in tokens and "to" in tokens:
                line_content = f"{var_name} = {var_name}[{tokens[3]}:{tokens[5]}]\n"
            elif len(tokens) > 3 and tokens[3] in ("run", "run function"):
                run_tokens = tokens[3:]
                r_first = run_tokens[0]
                start_idx = 2 if r_first == "run function" else 1
                if "with" in run_tokens:
                    w_idx = run_tokens.index("with")
                    f_name = "".join(run_tokens[start_idx:w_idx])
                    f_args = ", ".join([a.rstrip(",") for a in run_tokens[w_idx + 1 :]])
                else:
                    f_name = "".join(run_tokens[start_idx:])
                    f_args = ""
                line_content = f"{var_name} = {f_name}({f_args})\n"
            else:
                rhs_tokens = tokens[3:]
                cast_chain = []
                while rhs_tokens and rhs_tokens[-1] in TYPE_CASTS:
                    cast_chain.append(rhs_tokens.pop())
                expr = " ".join([convert_operation(t) for t in rhs_tokens])
                if cast_chain:
                    expr = apply_casts(expr, cast_chain)
                line_content = f"{var_name} = {expr}\n"

        elif first == "add":
            line_content = f"{tokens[-1]} += {' '.join([convert_operation(t) for t in tokens[1 : tokens.index('to')]])}\n"

        elif first == "subtract":
            line_content = f"{tokens[-1]} -= {' '.join([convert_operation(t) for t in tokens[1 : tokens.index('from')]])}\n"

        elif first == "bring in":
            line_content = f"import {tokens[1]}\n"

        elif first in ("run", "run function"):
            start_idx = 2 if first == "run function" else 1
            if "with" in tokens:
                with_idx = tokens.index("with")
                func_name = "".join(tokens[start_idx:with_idx])
                args = ", ".join([a.rstrip(",") for a in tokens[with_idx + 1 :]])
            else:
                func_name = "".join(tokens[start_idx:])
                args = ""
            line_content = f"{func_name}({args})\n"

        elif first == "how to":
            args = (
                ", ".join(
                    [a.rstrip(",") for a in tokens[tokens.index("with") + 1 : -1]]
                )
                if "with" in tokens
                else ""
            )
            line_content = f"def {tokens[1]}({args}):\n"

        elif first in ("if", "while"):
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
            if len(tokens) != 4 or tokens[2] != "into":
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
            if first in ("how to", "if", "while", "otherwise", "repeat", "count"):
                indent_level += 1

    return final_code

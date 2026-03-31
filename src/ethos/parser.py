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
        if cast == "to bytes":
            expr = f'{py_func}({expr}, "utf-8")'
        else:
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


def parse(all_tokens,debug_mode=False,python_mode=False):
    final_code = ""
    indent_level = 0
    in_multiline_comment = False
    multiline_comment_content = []

    for sentence in all_tokens:
        tokens = preprocess_tokens(sentence)
        if not tokens:
            continue

        first = tokens[0]

        if first == "end":
            indent_level -= 1
            if indent_level < 0:
                print("Error: 'end' found without a matching block")
                return ""
            continue


        if indent_level < 0:
            indent_level = 0

        padding = " " * (indent_level * 4)
        line_content = ""
        override_padding = None

        if first == "note":
            line_content = f"# {' '.join(tokens[1:])}\n"

        elif first == "notes":
            in_multiline_comment = True
            multiline_comment_content = []
            line_content = None
        elif first == "endnotes":
            in_multiline_comment = False
            line_content = "'''\n" + "\n".join(multiline_comment_content) + "\n'''\n"
            multiline_comment_content = []
        elif in_multiline_comment:
            line_content = None
            multiline_comment_content.append(' '.join(tokens))

        elif first == "say":
            if len(tokens) < 2:
                print("Error: 'say' needs a value")
                return ""
            line_content = f"print({tokens[1]})\n"

        elif first == "set":
            var_name = tokens[1]
            if "from" in tokens and "to" in tokens:
                from_idx = tokens.index("from")
                to_idx = tokens.index("to", from_idx)
                source = tokens[from_idx - 1]
                start = tokens[from_idx + 1]
                end = tokens[to_idx + 1]
                line_content = f"{var_name} = {source}[{start}:{end}]\n"
            elif len(tokens) > 3 and tokens[3] in ("run", "run function"):
                run_tokens = tokens[3:]
                start_idx = 1
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
            start_idx = 1
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
                    [a.rstrip(",") for a in tokens[tokens.index("with") + 1 :]]
                )
                if "with" in tokens
                else ""
            )
            line_content = f"def {tokens[1]}({args}):\n"

        elif first in ("if", "while"):
            py_kw = "if" if first == "if" else "while"
            cond = " ".join([convert_operation(t) for t in tokens[1:]])
            line_content = f"{py_kw} {cond}:\n"

        elif first == "otherwise if":
            cond = " ".join([convert_operation(t) for t in tokens[1:]])
            line_content = f"elif {cond}:\n"
            override_padding = (indent_level - 1) * 4
        elif first == "otherwise":
            line_content = "else:\n"
            override_padding = (indent_level - 1) * 4
        elif first == "repeat":
            n = tokens[1]
            line_content = f"for _ in range({n}):\n"

        elif first == "count":
            var = tokens[tokens.index("variable") + 1]
            from_idx = tokens.index("from")
            to_idx = tokens.index("to")
            start = tokens[from_idx + 1]
            end = tokens[to_idx + 1]
            if "stepping" in tokens:
                stepping_idx = tokens.index("stepping")
                step = tokens[stepping_idx + 1]
            else:
                step = "1"
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
            target = tokens[3]
            if not target.isidentifier():
                print(
                    f"Error: '{target}' is not a valid variable name. Use a valid identifier (e.g., my_var, x, result)"
                )
                return
            line_content = f"{target} = input({tokens[1]})\n"

        if line_content:
            if debug_mode:
                debug_str = " ".join(tokens).replace('\\', '\\\\').replace("'", "\\'").replace('"', '\\"')
                final_code += f'{padding}print("DEBUG: {debug_str}")\n'
            if python_mode:
                escaped_content = line_content.strip().replace('\\', '\\\\').replace("'", "\\'").replace('"', '\\"')
                final_code += f'{padding}print("PY_GEN: {escaped_content}")\n'
            if override_padding is not None:
                final_code += " " * override_padding + line_content
            else:
                final_code += padding + line_content
            if first in ("how to", "if", "while", "repeat", "count"):
                indent_level += 1

    return final_code

import re
import shlex


def split_sentences(raw_text):
    sentences = re.findall(
        r"""((?:"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'|\d+\.\d+|[^.])+\.)""", raw_text
    )
    final_sentences = []
    for i in sentences:
        trimmed = i.strip()
        if trimmed == "":
            continue
        final_sentences.append(trimmed)
    return final_sentences


def tokenize_and_normalize(sentence):
    words = shlex.split(sentence, posix=False)
    final_words = []
    for i in words:
        if i.startswith('"') or i.startswith("'"):
            final_words.append(i)
        else:
            final_words.append(i.lower())
    final_words[-1] = final_words[-1][:-1]
    return final_words


def lex(raw_text):
    sentences = split_sentences(raw_text)
    all_tokens = []
    for i in sentences:
        all_tokens.append(tokenize_and_normalize(i))
    return all_tokens

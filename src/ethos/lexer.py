import re
import shlex


def split_sentences(raw_text):
    sentences = []
    current = []
    in_single_quote = False
    in_double_quote = False
    i = 0
    while i < len(raw_text):
        char = raw_text[i]

        if i > 0 and raw_text[i-1] == '\\':
            current.append(char)
            i += 1
            continue

        if char == '"' and not in_single_quote:
            in_double_quote = not in_double_quote
            current.append(char)
        elif char == "'" and not in_double_quote:
            in_single_quote = not in_single_quote
            current.append(char)
        elif char == '\n' and not in_single_quote and not in_double_quote:
            sentence = ''.join(current).strip()
            if sentence:
                sentences.append(sentence)
            current = []
        elif char == '.' and not in_single_quote and not in_double_quote:
            keep_period = False

            if i + 1 < len(raw_text) and raw_text[i + 1].isdigit():
                keep_period = True
            elif i + 1 < len(raw_text) and raw_text[i + 1].isalpha():
                if current and (current[-1].isalnum() or current[-1] == '_'):
                    prev_part = ''.join(current).split()[-1] if ''.join(current).split() else ''
                    if prev_part and prev_part[0].isalpha():
                        keep_period = True

            if keep_period:
                current.append(char)
            else:
                sentence = ''.join(current).strip()
                if sentence:
                    sentences.append(sentence + '.')
                current = []
        else:
            current.append(char)
        i += 1

    remaining = ''.join(current).strip()
    if remaining:
        sentences.append(remaining)

    return sentences


def tokenize_and_normalize(sentence):
    sentence = sentence.rstrip('.')
    words = shlex.split(sentence, posix=False)
    final_words = []
    for i in words:
        if i.startswith('"') or i.startswith("'"):
            final_words.append(i)
        elif i:
            final_words.append(i.lower())
    return final_words


def lex(raw_text):
    sentences = split_sentences(raw_text)
    all_tokens = []
    for i in sentences:
        all_tokens.append(tokenize_and_normalize(i))
    return all_tokens

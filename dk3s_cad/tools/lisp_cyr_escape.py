#!/usr/bin/env python3
"""Заменяет не-ASCII символы внутри строковых литералов AutoLISP на \\U+XXXX.
Комментарии не трогаются. Использование:
    python3 lisp_cyr_escape.py source.lsp > dk3s_drawing.lsp        # кодировать
    python3 lisp_cyr_escape.py --decode dk3s_drawing.lsp > src.lsp  # раскодировать для правки
"""
import sys

def escape_lisp(src: str) -> str:
    out = []
    i, n = 0, len(src)
    in_str = False
    in_block_comment = False
    while i < n:
        ch = src[i]
        if in_block_comment:
            out.append(ch)
            if ch == '|' and i + 1 < n and src[i + 1] == ';':
                out.append(';'); i += 2; in_block_comment = False; continue
            i += 1; continue
        if in_str:
            if ch == '\\' and i + 1 < n:
                out.append(ch); out.append(src[i + 1]); i += 2; continue
            if ch == '"':
                in_str = False; out.append(ch); i += 1; continue
            if ord(ch) > 127:
                out.append('\\\\U+%04X' % ord(ch)); i += 1; continue
            out.append(ch); i += 1; continue
        # вне строки
        if ch == ';':
            if i + 1 < n and src[i + 1] == '|':
                in_block_comment = True; out.append(';|'); i += 2; continue
            j = src.find('\n', i)
            j = n if j < 0 else j
            out.append(src[i:j]); i = j; continue
        if ch == '"':
            in_str = True; out.append(ch); i += 1; continue
        out.append(ch); i += 1
    return ''.join(out)

def unescape_lisp(src: str) -> str:
    """Обратное преобразование \\U+XXXX -> символ (для правки текстов)."""
    import re
    return re.sub(r'\\\\U\+([0-9A-Fa-f]{4})', lambda m: chr(int(m.group(1), 16)), src)


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    text = open(args[0], encoding='utf-8').read()
    if '--decode' in sys.argv:
        sys.stdout.write(unescape_lisp(text))
    else:
        sys.stdout.write(escape_lisp(text))

#!/usr/bin/env python3
"""
autolisp_mini.py — минимальный интерпретатор подмножества AutoLISP для проверки
чертёжных скриптов без CAD-системы. Версия 1.0 (2026-09-19).

Поддерживается: reader (списки, точечные пары, строки с escape, комментарии),
динамическая область видимости, defun/lambda, базовые списковые, арифметические
и строковые функции, entmake (LINE, CIRCLE, ARC, LWPOLYLINE, TEXT, MTEXT, DIMENSION,
LAYER, LTYPE, STYLE, DIMSTYLE) -> ezdxf, tblsearch/tblobjname, getvar/setvar,
command (_.ZOOM, _.-LAYER, _.DIMLINEAR). Целочисленная арифметика как в AutoLISP.

Ограничения: нет vl-* функций, нет DCL, нет ssget/entmod, нет ActiveX.
"""
import math
import re
import sys


# ----------------------------------------------------------------------------
# Данные
# ----------------------------------------------------------------------------
class Sym:
    __slots__ = ("name",)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


_symtab = {}


def sym(name):
    n = name.upper()
    s = _symtab.get(n)
    if s is None:
        s = Sym(n)
        _symtab[n] = s
    return s


class Cons:
    """Точечная пара (car . cdr), где cdr — атом."""
    __slots__ = ("car", "cdr")

    def __init__(self, a, d):
        self.car = a
        self.cdr = d

    def __repr__(self):
        return "(%r . %r)" % (self.car, self.cdr)


class Lambda:
    __slots__ = ("params", "locals", "body", "name")

    def __init__(self, params, locs, body, name="lambda"):
        self.params = params
        self.locals = locs
        self.body = body
        self.name = name

    def __repr__(self):
        return "#<%s>" % self.name


class LispError(Exception):
    pass


T = sym("T")
NIL = None


def is_list(v):
    return isinstance(v, list)


def truthy(v):
    return v is not None


def car(v):
    if v is None:
        return None
    if isinstance(v, Cons):
        return v.car
    if isinstance(v, list):
        return v[0]
    raise LispError("bad argument type: consp %r" % (v,))


def cdr(v):
    if v is None:
        return None
    if isinstance(v, Cons):
        return v.cdr
    if isinstance(v, list):
        return v[1:] if len(v) > 1 else None
    raise LispError("bad argument type: consp %r" % (v,))


def lisp_cons(a, d):
    if d is None:
        return [a]
    if isinstance(d, list):
        return [a] + d
    return Cons(a, d)


def lisp_equal(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) < 1e-9
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(lisp_equal(x, y) for x, y in zip(a, b))
    if isinstance(a, Cons) and isinstance(b, Cons):
        return lisp_equal(a.car, b.car) and lisp_equal(a.cdr, b.cdr)
    return a == b


# ----------------------------------------------------------------------------
# Reader
# ----------------------------------------------------------------------------
_TOKEN = re.compile(r"""\s*(?:(;\|)|(;[^\n]*)|(\()|(\))|(')|("(?:\\.|[^"\\])*")|([^\s()'";]+))""", re.S)


def tokenize(src):
    pos = 0
    n = len(src)
    while pos < n:
        m = _TOKEN.match(src, pos)
        if not m:
            break
        pos = m.end()
        if m.group(1):  # блочный комментарий ;| ... |;
            end = src.find("|;", pos)
            pos = n if end < 0 else end + 2
            continue
        if m.group(2):
            continue
        if m.group(3):
            yield ("(", None)
        elif m.group(4):
            yield (")", None)
        elif m.group(5):
            yield ("'", None)
        elif m.group(6):
            yield ("str", unescape(m.group(6)[1:-1]))
        elif m.group(7):
            yield ("atom", m.group(7))


def unescape(s):
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            d = s[i + 1]
            i += 2
            if d == "n":
                out.append("\n")
            elif d == "t":
                out.append("\t")
            elif d == "r":
                out.append("\r")
            elif d == "e":
                out.append("\x1b")
            elif d == "\\":
                out.append("\\")
            elif d == '"':
                out.append('"')
            elif d in "01234567":
                j = i
                digits = d
                while j < len(s) and len(digits) < 3 and s[j] in "01234567":
                    digits += s[j]
                    j += 1
                i = j
                out.append(chr(int(digits, 8)))
            else:
                out.append(d)  # неизвестный escape — символ без слэша
            continue
        out.append(c)
        i += 1
    return "".join(out)


def parse_atom(tok):
    if re.fullmatch(r"[+-]?\d+", tok):
        return int(tok)
    if re.fullmatch(r"[+-]?(\d+\.\d*|\.\d+|\d+)([eE][+-]?\d+)?", tok):
        return float(tok)
    if tok.upper() == "NIL":
        return None
    return sym(tok)


def read_all(src):
    toks = list(tokenize(src))
    pos = [0]

    def read():
        if pos[0] >= len(toks):
            raise LispError("unexpected EOF")
        kind, val = toks[pos[0]]
        pos[0] += 1
        if kind == "(":
            items = []
            tail = None
            while True:
                if pos[0] >= len(toks):
                    raise LispError("unbalanced parentheses")
                k, v = toks[pos[0]]
                if k == ")":
                    pos[0] += 1
                    break
                if k == "atom" and v == ".":
                    pos[0] += 1
                    tail = read()
                    k2, _ = toks[pos[0]]
                    if k2 != ")":
                        raise LispError("bad dotted pair")
                    pos[0] += 1
                    break
                items.append(read())
            if tail is not None:
                if isinstance(tail, list):
                    return items + tail
                if len(items) != 1:
                    raise LispError("bad dotted pair")
                return Cons(items[0], tail)
            return items if items else None
        if kind == ")":
            raise LispError("unexpected )")
        if kind == "'":
            return [sym("QUOTE"), read()]
        if kind == "str":
            return val
        return parse_atom(val)

    forms = []
    while pos[0] < len(toks):
        forms.append(read())
    return forms


# ----------------------------------------------------------------------------
# Интерпретатор
# ----------------------------------------------------------------------------
class Interp:
    def __init__(self, backend, out=sys.stdout):
        self.frames = [{}]  # динамический стек окружений
        self.funcs = {}
        self.backend = backend
        self.out = out
        self.sysvars = {"CMDECHO": 1, "OSMODE": 0, "CLAYER": "0", "DIMSCALE": 1.0, "DIMASZ": 2.5,
                        "DIMEXO": 0.625, "DIMEXE": 1.25, "DIMTXT": 2.5, "DIMGAP": 0.625,
                        "DIMTIH": 0, "DIMTOH": 0, "DIMTAD": 0, "DIMZIN": 8, "DIMDEC": 2,
                        "DIMDSEP": ".", "DIMTXSTY": "Standard", "DIMSTYLE": "Standard",
                        "DIMLFAC": 1.0, "FILEDIA": 1, "PI": math.pi}
        self.globals()[sym("PI")] = math.pi
        self.globals()[sym("T")] = T
        self.builtins = self._make_builtins()
        self.command_log = []
        self.max_depth = 4000

    def globals(self):
        return self.frames[0]

    # --- переменные ------------------------------------------------------
    def lookup(self, s):
        for fr in reversed(self.frames):
            if s in fr:
                return fr[s]
        if s in self.funcs:
            return self.funcs[s]
        return None

    def assign(self, s, v):
        for fr in reversed(self.frames):
            if s in fr:
                fr[s] = v
                return v
        self.frames[0][s] = v
        return v

    # --- вычисление ------------------------------------------------------
    def eval(self, x):
        if isinstance(x, Sym):
            return self.lookup(x)
        if not isinstance(x, list):
            return x  # число, строка, None, Cons
        head = x[0]
        if isinstance(head, Sym):
            name = head.name
            sf = self.special.get(name)
            if sf is not None:
                return sf(self, x[1:])
            fn = self.funcs.get(head)
            if fn is None:
                fn = self.lookup(head)
            if fn is None:
                bi = self.builtins.get(name)
                if bi is None:
                    raise LispError("no function definition: %s" % name)
                args = [self.eval(a) for a in x[1:]]
                return bi(*args)
            args = [self.eval(a) for a in x[1:]]
            return self.call(fn, args)
        if isinstance(head, list) and head and head[0] is sym("LAMBDA"):
            fn = self.make_lambda(head[1:], "lambda")
            args = [self.eval(a) for a in x[1:]]
            return self.call(fn, args)
        raise LispError("bad function: %r" % (head,))

    def make_lambda(self, rest, name):
        arglist = rest[0]
        body = rest[1:]
        params, locs = [], []
        if arglist:
            seen_slash = False
            for a in arglist:
                if isinstance(a, Sym) and a.name == "/":
                    seen_slash = True
                elif seen_slash:
                    locs.append(a)
                else:
                    params.append(a)
        return Lambda(params, locs, body, name)

    def call(self, fn, args):
        if isinstance(fn, Lambda):
            if len(args) != len(fn.params):
                raise LispError("too %s arguments: %s" % ("few" if len(args) < len(fn.params) else "many", fn.name))
            frame = {}
            for p, a in zip(fn.params, args):
                frame[p] = a
            for l in fn.locals:
                frame[l] = None
            if len(self.frames) > self.max_depth:
                raise LispError("stack overflow")
            self.frames.append(frame)
            try:
                res = None
                for b in fn.body:
                    res = self.eval(b)
                return res
            finally:
                self.frames.pop()
        if isinstance(fn, Sym):
            f = self.funcs.get(fn)
            if f is not None:
                return self.call(f, args)
            bi = self.builtins.get(fn.name)
            if bi is None:
                raise LispError("no function definition: %s" % fn.name)
            return bi(*args)
        if callable(fn):
            return fn(*args)
        raise LispError("bad function: %r" % (fn,))

    def run(self, src):
        res = None
        for form in read_all(src):
            res = self.eval_top(form)
        return res

    def eval_top(self, form):
        try:
            return self.eval(form)
        except LispError as e:
            handler = self.lookup(sym("*ERROR*"))
            if handler is not None:
                self.call(handler, [str(e)])
                return None
            raise

    # --- специальные формы ----------------------------------------------
    def sf_quote(self, a):
        return a[0]

    def sf_setq(self, a):
        v = None
        for i in range(0, len(a), 2):
            v = self.eval(a[i + 1])
            self.assign(a[i], v)
        return v

    def sf_defun(self, a):
        name = a[0]
        fn = self.make_lambda(a[1:], name.name)
        self.funcs[name] = fn
        return name

    def sf_if(self, a):
        if truthy(self.eval(a[0])):
            return self.eval(a[1])
        if len(a) > 2:
            return self.eval(a[2])
        return None

    def sf_cond(self, a):
        for clause in a:
            t = self.eval(clause[0])
            if truthy(t):
                res = t
                for b in clause[1:]:
                    res = self.eval(b)
                return res
        return None

    def sf_progn(self, a):
        res = None
        for b in a:
            res = self.eval(b)
        return res

    def sf_and(self, a):
        res = T
        for b in a:
            res = self.eval(b)
            if not truthy(res):
                return None
        return T

    def sf_or(self, a):
        for b in a:
            if truthy(self.eval(b)):
                return T
        return None

    def sf_while(self, a):
        res = None
        while truthy(self.eval(a[0])):
            for b in a[1:]:
                res = self.eval(b)
        return res

    def sf_repeat(self, a):
        n = self.eval(a[0])
        if not isinstance(n, int):
            raise LispError("bad argument type: fixnump: %r" % (n,))
        res = None
        for _ in range(n):
            for b in a[1:]:
                res = self.eval(b)
        return res

    def sf_foreach(self, a):
        var = a[0]
        lst = self.eval(a[1])
        res = None
        self.frames.append({var: None})
        try:
            for item in (lst or []):
                self.frames[-1][var] = item
                for b in a[2:]:
                    res = self.eval(b)
        finally:
            self.frames.pop()
        return res

    def sf_function(self, a):
        x = a[0]
        if isinstance(x, list) and x[0] is sym("LAMBDA"):
            return self.make_lambda(x[1:], "lambda")
        return x

    def sf_lambda(self, a):
        return self.make_lambda(a, "lambda")

    special = {
        "QUOTE": sf_quote, "SETQ": sf_setq, "DEFUN": sf_defun, "IF": sf_if, "COND": sf_cond,
        "PROGN": sf_progn, "AND": sf_and, "OR": sf_or, "WHILE": sf_while, "REPEAT": sf_repeat,
        "FOREACH": sf_foreach, "FUNCTION": sf_function, "LAMBDA": sf_lambda,
    }

    # --- встроенные функции ------------------------------------------------
    def _make_builtins(self):
        def num(v):
            if not isinstance(v, (int, float)) or isinstance(v, bool):
                raise LispError("bad argument type: numberp: %r" % (v,))
            return v

        def add(*a):
            r = 0
            for v in a:
                r = r + num(v)
            return r

        def sub(*a):
            if len(a) == 1:
                return -num(a[0])
            r = num(a[0])
            for v in a[1:]:
                r = r - num(v)
            return r

        def mul(*a):
            r = 1
            for v in a:
                r = r * num(v)
            return r

        def div(*a):
            if len(a) == 1:
                return (1 // num(a[0])) if isinstance(a[0], int) else 1.0 / a[0]
            r = num(a[0])
            for v in a[1:]:
                num(v)
                if isinstance(r, int) and isinstance(v, int):
                    if v == 0:
                        raise LispError("divide by zero")
                    q = abs(r) // abs(v)
                    r = q if (r >= 0) == (v >= 0) else -q
                else:
                    if v == 0:
                        raise LispError("divide by zero")
                    r = r / v
            return r

        def cmp_chain(op):
            def f(*a):
                for x, y in zip(a, a[1:]):
                    if isinstance(x, str) and isinstance(y, str):
                        ok = op(x, y)
                    else:
                        ok = op(num(x), num(y))
                    if not ok:
                        return None
                return T
            return f

        def eq_(*a):
            for x, y in zip(a, a[1:]):
                if isinstance(x, (int, float)) and isinstance(y, (int, float)):
                    if x != y:
                        return None
                elif x != y:
                    return None
            return T

        def neq(a, b):
            return None if truthy(eq_(a, b)) else T

        def strcat(*a):
            for s in a:
                if not isinstance(s, str):
                    raise LispError("bad argument type: stringp %r" % (s,))
            return "".join(a)

        def substr(s, start, length=None):
            if length is None:
                return s[start - 1:]
            return s[start - 1:start - 1 + length]

        def rtos(v, mode=2, prec=4):
            num(v)
            if mode not in (2, None):
                pass
            s = "%.*f" % (prec, v)
            zin = self.sysvars.get("DIMZIN", 8)
            if zin & 8 and "." in s:
                s = s.rstrip("0").rstrip(".")
            if zin & 4 and s.startswith("0."):
                s = s[1:]
            return s

        def princ(v=None):
            if v is None:
                return None
            self.out.write(v if isinstance(v, str) else lisp_repr(v))
            return v

        def prompt(s):
            self.out.write(s)
            return None

        def mapcar(fn, *lists):
            n = min(len(l or []) for l in lists) if lists else 0
            res = [self.call(fn, [l[i] for l in lists]) for i in range(n)]
            return res if res else None

        def apply_(fn, lst):
            return self.call(fn, list(lst or []))

        def nth(i, lst):
            if lst is None or i >= len(lst) or i < 0:
                return None
            return lst[i]

        def append_(*ls):
            res = []
            for l in ls:
                if l is None:
                    continue
                if isinstance(l, list):
                    res.extend(l)
                else:
                    raise LispError("bad argument type: listp %r" % (l,))
            return res if res else None

        def member(x, lst):
            if lst is None:
                return None
            for i, v in enumerate(lst):
                if lisp_equal(x, v):
                    return lst[i:]
            return None

        def assoc(key, alist):
            for e in (alist or []):
                if lisp_equal(car(e), key):
                    return e
            return None

        def atan_(a, b=None):
            if b is None:
                return math.atan(num(a))
            return math.atan2(num(a), num(b))

        def polar(p, ang, d):
            return [p[0] + d * math.cos(ang), p[1] + d * math.sin(ang)] + ([p[2]] if len(p) > 2 else [])

        def distance(p, q):
            return math.sqrt(sum((a - b) ** 2 for a, b in zip(p, q)))

        def angle(p, q):
            return math.atan2(q[1] - p[1], q[0] - p[0]) % (2 * math.pi)

        def getvar(name):
            return self.sysvars.get(name.upper())

        def setvar(name, v):
            self.sysvars[name.upper()] = v
            return v

        def fix(v):
            return int(math.floor(num(v))) if v >= 0 else -int(math.floor(-v))

        def length(l):
            return 0 if l is None else len(l)

        def reverse_(l):
            return list(reversed(l)) if l else None

        def last_(l):
            return l[-1] if l else None

        def list_(*a):
            return list(a) if a else None

        def entmake(lst):
            return self.backend.entmake(lst, self)

        def tblsearch(table, name):
            return self.backend.tblsearch(table, name)

        def tblobjname(table, name):
            return self.backend.tblobjname(table, name)

        def command(*args):
            self.command_log.append(args)
            return self.backend.command(args, self)

        def itoa(v):
            if not isinstance(v, int):
                raise LispError("bad argument type: fixnump: %r" % (v,))
            return str(v)

        return {
            "+": add, "-": sub, "*": mul, "/": div,
            "1+": lambda v: num(v) + 1, "1-": lambda v: num(v) - 1,
            "ABS": lambda v: abs(num(v)), "MIN": lambda *a: min(num(v) for v in a),
            "MAX": lambda *a: max(num(v) for v in a), "SQRT": lambda v: math.sqrt(num(v)),
            "EXPT": lambda a, b: num(a) ** num(b), "SIN": lambda v: math.sin(num(v)),
            "COS": lambda v: math.cos(num(v)), "ATAN": atan_, "REM": lambda a, b: math.fmod(num(a), num(b)) if isinstance(a, float) or isinstance(b, float) else int(math.fmod(a, b)),
            "FLOAT": lambda v: float(num(v)), "FIX": fix,
            "=": eq_, "/=": neq, "<": cmp_chain(lambda x, y: x < y), ">": cmp_chain(lambda x, y: x > y),
            "<=": cmp_chain(lambda x, y: x <= y), ">=": cmp_chain(lambda x, y: x >= y),
            "EQ": lambda a, b: T if a is b or (isinstance(a, (int, float, str)) and a == b) else None,
            "EQUAL": lambda a, b, fuzz=0.0: T if lisp_equal(a, b) or (isinstance(a, (int, float)) and isinstance(b, (int, float)) and abs(a - b) <= fuzz) else None,
            "NOT": lambda v: T if v is None else None, "NULL": lambda v: T if v is None else None,
            "LISTP": lambda v: T if (v is None or isinstance(v, (list, Cons))) else None,
            "NUMBERP": lambda v: T if isinstance(v, (int, float)) else None,
            "ZEROP": lambda v: T if num(v) == 0 else None, "MINUSP": lambda v: T if num(v) < 0 else None,
            "STRCAT": strcat, "STRLEN": lambda *a: sum(len(s) for s in a), "SUBSTR": substr,
            "STRCASE": lambda s, lower=None: s.lower() if lower else s.upper(),
            "ITOA": itoa, "ATOI": lambda s: int(s) if re.match(r"^[+-]?\d+", s.strip()) else 0,
            "ATOF": lambda s: float(s) if re.match(r"^[+-]?\d", s.strip()) else 0.0, "RTOS": rtos,
            "CHR": chr, "ASCII": lambda s: ord(s[0]) if s else 0,
            "PRINC": princ, "PRIN1": princ, "PRINT": princ, "PROMPT": prompt, "TERPRI": lambda: self.out.write("\n"),
            "LIST": list_, "CONS": lisp_cons, "CAR": car, "CDR": cdr,
            "CADR": lambda v: car(cdr(v)), "CDDR": lambda v: cdr(cdr(v)), "CADDR": lambda v: car(cdr(cdr(v))),
            "CAAR": lambda v: car(car(v)), "CDAR": lambda v: cdr(car(v)),
            "NTH": nth, "LAST": last_, "LENGTH": length, "APPEND": append_, "REVERSE": reverse_,
            "MAPCAR": mapcar, "APPLY": apply_, "MEMBER": member, "ASSOC": assoc,
            "SUBST": lambda new, old, lst: [new if lisp_equal(e, old) else e for e in (lst or [])] or None,
            "POLAR": polar, "DISTANCE": distance, "ANGLE": angle,
            "GETVAR": getvar, "SETVAR": setvar,
            "ENTMAKE": entmake, "ENTLAST": lambda: self.backend.entlast(),
            "ENTGET": lambda e: self.backend.entget(e),
            "TBLSEARCH": tblsearch, "TBLOBJNAME": tblobjname, "COMMAND": command,
            "VL-LOAD-COM": lambda: None,
            "TYPE": lambda v: sym({int: "INT", float: "REAL", str: "STR", list: "LIST", Sym: "SYM"}.get(type(v), "LIST")) if v is not None else None,
        }


def lisp_repr(v):
    if v is None:
        return "nil"
    if v is T:
        return "T"
    if isinstance(v, str):
        return '"%s"' % v
    if isinstance(v, float):
        return repr(v)
    if isinstance(v, list):
        return "(" + " ".join(lisp_repr(x) for x in v) + ")"
    if isinstance(v, Cons):
        return "(%s . %s)" % (lisp_repr(v.car), lisp_repr(v.cdr))
    return str(v)


# ----------------------------------------------------------------------------
# DXF backend (ezdxf)
# ----------------------------------------------------------------------------
def decode_text(s):
    """\\U+XXXX -> символ; %%c/%%d/%%p остаются (их понимает CAD и ezdxf)."""
    return re.sub(r"\\U\+([0-9A-Fa-f]{4})", lambda m: chr(int(m.group(1), 16)), s)


def groups(lst):
    """Список entmake -> список пар (код, значение)."""
    res = []
    for e in (lst or []):
        if isinstance(e, Cons):
            res.append((e.car, e.cdr))
        elif isinstance(e, list):
            res.append((e[0], e[1:]))
        else:
            raise LispError("bad entmake list element: %r" % (e,))
    return res


class DxfBackend:
    def __init__(self, fail_types=()):
        import ezdxf
        self.ezdxf = ezdxf
        self.doc = ezdxf.new("R2010", setup=True)
        self.msp = self.doc.modelspace()
        self.fail_types = set(t.upper() for t in fail_types)
        self.counts = {}
        self.last = None
        self.unsupported = []
        self.dims = []

    # --- таблицы ---------------------------------------------------------
    def tblsearch(self, table, name):
        t = table.upper()
        d = self.doc
        try:
            if t == "LAYER":
                return [Cons(2, name)] if name in d.layers else None
            if t == "LTYPE":
                return [Cons(2, name)] if name in d.linetypes else None
            if t == "STYLE":
                return [Cons(2, name)] if name in d.styles else None
            if t == "DIMSTYLE":
                return [Cons(2, name)] if name in d.dimstyles else None
        except Exception:
            return None
        return None

    def tblobjname(self, table, name):
        return ("ENAME:%s:%s" % (table.upper(), name)) if self.tblsearch(table, name) else None

    def entlast(self):
        return self.last

    def entget(self, e):
        return None

    # --- entmake ----------------------------------------------------------
    def entmake(self, lst, interp):
        g = groups(lst)
        gd = {}
        for code, val in g:
            gd.setdefault(code, []).append(val)
        etype = gd.get(0, [None])[0]
        if etype is None:
            raise LispError("entmake: no entity type")
        etype = etype.upper()
        if etype in self.fail_types:
            return None
        layer = gd.get(8, ["0"])[0]
        first = lambda c, dflt=None: gd.get(c, [dflt])[0]
        A = {"layer": layer}
        try:
            if etype == "LINE":
                self.last = self.msp.add_line(first(10), first(11), dxfattribs=A)
            elif etype == "CIRCLE":
                self.last = self.msp.add_circle(first(10), first(40), dxfattribs=A)
            elif etype == "ARC":
                self.last = self.msp.add_arc(first(10), first(40), first(50, 0.0), first(51, 360.0), dxfattribs=A)
            elif etype == "LWPOLYLINE":
                pts = gd.get(10, [])
                bulges = []
                # bulge (42) следует за своей вершиной — восстанавливаем порядок
                cur = None
                for code, val in g:
                    if code == 10:
                        if cur is not None:
                            bulges.append(cur)
                        cur = 0.0
                    elif code == 42:
                        cur = val
                if cur is not None:
                    bulges.append(cur)
                closed = bool(first(70, 0) & 1)
                w = first(43, 0.0)
                fmt = [(p[0], p[1], w, w, b) for p, b in zip(pts, bulges)]
                A["const_width"] = w
                self.last = self.msp.add_lwpolyline(fmt, format="xyseb", close=closed, dxfattribs=A)
            elif etype in ("TEXT", "MTEXT"):
                from ezdxf.enums import TextEntityAlignment as TA
                txt = decode_text(first(1, ""))
                h = first(40, 2.5)
                rot = first(50, 0.0)
                style = first(7, "Standard")
                if style not in self.doc.styles:
                    style = "Standard"
                A.update({"style": style})
                if first(41) is not None:          # коэффициент ширины (сжатие надписи)
                    A["width"] = float(first(41))
                if etype == "TEXT":
                    hj, vj = first(72, 0), first(73, 0)
                    align = {(0, 0): TA.LEFT, (1, 0): TA.CENTER, (2, 0): TA.RIGHT, (1, 2): TA.MIDDLE_CENTER,
                             (0, 2): TA.MIDDLE_LEFT, (2, 2): TA.MIDDLE_RIGHT, (0, 3): TA.TOP_LEFT,
                             (1, 3): TA.TOP_CENTER, (1, 1): TA.BOTTOM_CENTER}.get((hj, vj), TA.LEFT)
                    p = first(11) if (hj or vj) else first(10)
                    t = self.msp.add_text(txt, height=h, rotation=rot, dxfattribs=A)
                    t.set_placement(p, align=align)
                    self.last = t
                else:
                    A.update({"char_height": h, "rotation": rot})
                    self.last = self.msp.add_mtext(txt, dxfattribs=A)
                    self.last.set_location(first(10))
            elif etype == "DIMENSION":
                style = first(3, "Standard")
                if style not in self.doc.dimstyles:
                    style = "Standard"
                txt = decode_text(first(1, "")) or "<>"
                dim = self.msp.add_linear_dim(base=first(10), p1=first(13), p2=first(14), angle=first(50, 0.0),
                                              text=txt, dimstyle=style, dxfattribs=A)
                dim.render()
                self.last = dim.dimension
                self.dims.append((first(13), first(14), first(10), first(50, 0.0), txt))
            elif etype == "LAYER":
                name = first(2)
                lt = first(6, "Continuous")
                if lt not in self.doc.linetypes:
                    lt = "Continuous"
                self.doc.layers.add(name, color=first(62, 7), linetype=lt, lineweight=first(370, -3))
            elif etype == "LTYPE":
                name = first(2)
                dashes = gd.get(49, [])
                total = first(40, sum(abs(x) for x in dashes))
                self.doc.linetypes.add(name, pattern=[total] + list(dashes), description=first(3, ""))
            elif etype == "STYLE":
                name = first(2)
                st = self.doc.styles.add(name, font=first(3, "arial.ttf"))
                st.dxf.oblique = first(50, 0.0)
                st.dxf.width = first(41, 1.0)
            elif etype == "DIMSTYLE":
                name = first(2)
                m = {40: "dimscale", 41: "dimasz", 42: "dimexo", 43: "dimdli", 44: "dimexe", 140: "dimtxt",
                     144: "dimlfac", 147: "dimgap", 73: "dimtih", 74: "dimtoh", 77: "dimtad", 78: "dimzin",
                     271: "dimdec", 278: "dimdsep", 279: "dimtmove", 171: "dimaltd", 172: "dimtofl",
                     174: "dimtix", 175: "dimsoxd", 176: "dimclrd", 177: "dimclre"}
                attrs = {}
                for code, val in g:
                    if code in m:
                        attrs[m[code]] = val
                    elif code == 340 and isinstance(val, str) and val.startswith("ENAME:STYLE:"):
                        attrs["dimtxsty"] = val.split(":", 2)[2]
                self.doc.dimstyles.new(name, dxfattribs=attrs)
            else:
                self.unsupported.append(etype)
                return None
        except Exception as e:
            raise LispError("entmake %s failed: %s" % (etype, e))
        self.counts[etype] = self.counts.get(etype, 0) + 1
        return lst

    # --- command ----------------------------------------------------------
    def command(self, args, interp):
        if not args:
            return None
        cmd = str(args[0]).upper().lstrip("_.")
        if cmd == "ZOOM":
            return None
        if cmd == "-LAYER":
            # (command "_.-LAYER" "_M" name "_C" color name "_L" ltype name "")
            a = list(args[1:])
            name = a[1] if len(a) > 1 else "0"
            color = 7
            lt = "Continuous"
            for i, v in enumerate(a):
                if str(v).upper() == "_C":
                    color = int(a[i + 1])
                if str(v).upper() == "_L":
                    lt = a[i + 1]
            if name not in self.doc.layers:
                self.doc.layers.add(name, color=color, linetype=lt if lt in self.doc.linetypes else "Continuous")
            return None
        if cmd == "DIMLINEAR":
            a = list(args[1:])
            p1, p2 = a[0], a[1]
            i = 2
            angle = 0.0
            txt = "<>"
            while i < len(a):
                v = a[i]
                if isinstance(v, str) and v.upper() == "_V":
                    angle = 90.0
                    i += 1
                elif isinstance(v, str) and v.upper() == "_H":
                    angle = 0.0
                    i += 1
                elif isinstance(v, str) and v.upper() == "_T":
                    txt = decode_text(a[i + 1]) or "<>"
                    i += 2
                else:
                    pd = v
                    i += 1
            style = interp.sysvars.get("DIMSTYLE", "Standard")
            ov = {k.lower(): interp.sysvars[k] for k in ("DIMSCALE", "DIMASZ", "DIMEXO", "DIMEXE", "DIMTXT", "DIMGAP",
                                                             "DIMTIH", "DIMTOH", "DIMTAD", "DIMZIN", "DIMDEC", "DIMDSEP")
                  if k in interp.sysvars}
            if isinstance(ov.get("dimdsep"), str):      # AutoLISP: (setvar "DIMDSEP" ","), DXF: код символа
                ov["dimdsep"] = ord(ov["dimdsep"][0]) if ov["dimdsep"] else 46
            txsty = interp.sysvars.get("DIMTXSTY")
            if txsty in self.doc.styles:
                ov["dimtxsty"] = txsty
            dim = self.msp.add_linear_dim(base=pd, p1=p1, p2=p2, angle=angle, text=txt,
                                          dimstyle=style if style in self.doc.dimstyles else "Standard",
                                          override=ov, dxfattribs={"layer": interp.sysvars.get("CLAYER", "0")})
            dim.render()
            self.counts["DIMENSION(cmd)"] = self.counts.get("DIMENSION(cmd)", 0) + 1
            return None
        self.unsupported.append("COMMAND " + cmd)
        return None

    # --- вывод ----------------------------------------------------------------
    def save(self, path):
        self.doc.saveas(path)

    def render_png(self, path, width_px=6000, bg="#FFFFFF", mono=True, xlim=(-10, 850), ylim=(-10, 604)):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from ezdxf.addons.drawing import RenderContext, Frontend
        from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
        from ezdxf.addons.drawing.config import Configuration, LineweightPolicy, ColorPolicy, BackgroundPolicy
        w_units = xlim[1] - xlim[0]
        h_units = ylim[1] - ylim[0]
        dpi = 200
        fig = plt.figure(figsize=(width_px / dpi, width_px / dpi * h_units / w_units), dpi=dpi)
        ax = fig.add_axes([0, 0, 1, 1])
        ctx = RenderContext(self.doc)
        ctx.set_current_layout(self.msp)
        out = MatplotlibBackend(ax)
        cfg = Configuration(lineweight_policy=LineweightPolicy.ABSOLUTE, min_lineweight=0.15,
                            color_policy=ColorPolicy.BLACK if mono else ColorPolicy.COLOR,
                            background_policy=BackgroundPolicy.WHITE if mono else BackgroundPolicy.BLACK)
        Frontend(ctx, out, config=cfg).draw_layout(self.msp, finalize=False)
        ax.set_aspect("auto")
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.axis("off")
        fig.set_size_inches(width_px / dpi, width_px / dpi * h_units / w_units)
        fig.savefig(path, dpi=dpi, facecolor=bg if mono else "#000000")
        plt.close(fig)

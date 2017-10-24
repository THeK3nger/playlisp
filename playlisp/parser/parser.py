import operator as op
from playlisp.playlisp import PlayLisp

List = list
Number = (int, float)
Env = dict

PL = PlayLisp()


class TokenType(object):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if not isinstance(other, str):
            return self.value == other.value
        return self.value == other

    def __hash__(self):
        return hash(self.value)


class Symbol(TokenType):
    pass


class String(TokenType):
    def __init__(self, x):
        super(String, self).__init__(x[1:-1])


# TODO: Not now
StringRegex = r'^\".*\"$'


def parse(program):
    """Read a Scheme expression from a string."""
    return read_from_tokens(tokenize(program))


def run_script(program):
    """

    :param program:
    :type program: str
    :return:
    """

    # TODO: Count only parenthesis not in strings...
    def count_open(line):
        return line.count("(")

    def count_closed(line):
        return line.count(")")

    programlines = [""]
    pending = 0
    lines = program.splitlines()
    for line in lines:
        programlines[-1] += line
        pending += count_open(line) - count_closed(line)
        if pending == 0:
            programlines.append("")

    for l in programlines:
        if l.strip():
            eval(parse(l))


def read_from_tokens(tokens):
    """Read an expression from a sequence of tokens."""
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)  # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return atom(token)


def atom(token):
    """Numbers become numbers; every other token is a symbol."""
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            if len(token) >= 2 and token[0] == '"' and token[-1] == '"':
                return String(token)
            return Symbol(token)


def tokenize(chars):
    """Convert a string of characters into a list of tokens."""
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()


def repl(prompt='playlisp> '):
    "A prompt-read-eval-print loop."
    while True:
        val = eval(parse(input(prompt)))
        if val is not None:
            print(schemestr(val))


def schemestr(exp):
    "Convert a Python object back into a Scheme-readable string."
    if isinstance(exp, List):
        return '(' + ' '.join(map(schemestr, exp)) + ')'
    else:
        return str(exp)


def standard_env():
    "An environment with some Scheme standard procedures."
    env = Env()
    env.update({
        'interleave': lambda x, y: x.interleave(y),
        'shuffle': lambda x: x.shuffle(),
        'save': lambda source, dest: PL.save_on(dest, source),
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.floordiv,
        '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq,
        'abs': abs,
        'append': op.add,
        'begin': lambda *x: x[-1],
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'cons': lambda x, y: [x] + y,
        'eq?': op.is_,
        'equal?': op.eq,
        'length': len,
        'list': lambda *x: list(x),
        'list?': lambda x: isinstance(x, list),
        'map': map,
        'max': max,
        'min': min,
        'not': op.not_,
        'null?': lambda x: x == [],
        'number?': lambda x: isinstance(x, Number),
        'procedure?': callable,
        'round': round,
        'symbol?': lambda x: isinstance(x, Symbol),
        'print': lambda x: print(x)
    })
    return env


global_env = standard_env()


def eval(x, env=global_env):
    "Evaluate an expression in an environment."
    if isinstance(x, Symbol):  # variable reference
        return env[str(x)]
    elif isinstance(x, String):  # constant literal
        return x.value
    elif not isinstance(x, List):  # constant literal
        return x
    elif x[0] == 'if':  # conditional
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif x[0] == 'define':  # definition
        (_, var, exp) = x
        env[var] = eval(exp, env)
    elif x[0] == 'playlist':
        (_, plid) = x
        return PL.playlist(str(plid))
    else:  # procedure call
        proc = eval(x[0], env)
        args = [eval(arg, env) for arg in x[1:]]
        return proc(*args)

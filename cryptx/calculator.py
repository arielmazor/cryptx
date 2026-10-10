"""Multi-base calculator with bitwise operations.

Safely evaluates arithmetic and bitwise expressions containing integers
in decimal, hex (0x), octal (0o), and binary (0b) notation.

Supported operators:
  Arithmetic:  +  -  *  /  //  %  **
  Bitwise:     &  |  ^  ~  <<  >>

Supports named variables (e.g. ``ans``, user-defined) via a context dict.
"""

import ast
import operator
import re
import sys


# Map AST node types to safe Python operators
_SAFE_OPS = {
    # Binary operators
    ast.Add:      operator.add,
    ast.Sub:      operator.sub,
    ast.Mult:     operator.mul,
    ast.Div:      operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod:      operator.mod,
    ast.Pow:      operator.pow,
    ast.BitAnd:   operator.and_,
    ast.BitOr:    operator.or_,
    ast.BitXor:   operator.xor,
    ast.LShift:   operator.lshift,
    ast.RShift:   operator.rshift,
    # Unary operators
    ast.Invert:   operator.invert,
    ast.USub:     operator.neg,
    ast.UAdd:     operator.pos,
}

_ASSIGN_RE = re.compile(r"^([a-zA-Z_]\w*)\s*=\s*(.+)$")


def _eval_node(node: ast.AST, context: dict[str, int | float]) -> int | float:
    """Recursively evaluate an AST node using only safe operators."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, context)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.Name):
        if node.id in context:
            return context[node.id]
        raise ValueError(f"Unknown variable: '{node.id}'")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left, context)
        right = _eval_node(node.right, context)
        op_func = _SAFE_OPS.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        return op_func(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand, context)
        op_func = _SAFE_OPS.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        return op_func(operand)

    raise ValueError(
        f"Unsupported expression node: {type(node).__name__}. "
        "Only arithmetic and bitwise operations on literal numbers are allowed."
    )


def safe_eval(expression: str, context: dict[str, int | float] | None = None) -> int | float:
    """Parse and safely evaluate a mathematical / bitwise expression.

    Accepts integers in any Python-supported base:
      - Decimal:  255
      - Hex:      0xff
      - Octal:    0o377
      - Binary:   0b11111111

    Variables in *context* are available by name (e.g. ``ans``).
    Raises ValueError on unsupported syntax (no function calls, no imports).
    """
    try:
        tree = ast.parse(expression.strip(), mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression: {exc.msg}") from exc
    return _eval_node(tree, context or {})


def format_result(value: int | float) -> str:
    """Format a numeric result in decimal, hex, octal, and binary."""
    if isinstance(value, float) and not value.is_integer():
        return f"  Dec:  {value}"

    n = int(value)
    lines = [
        f"  Dec:  {n}",
        f"  Hex:  {hex(n)}",
        f"  Oct:  {oct(n)}",
        f"  Bin:  {bin(n)}",
    ]
    return "\n".join(lines)


def calculate(expression: str, context: dict[str, int | float] | None = None) -> tuple[int | float, str]:
    """Evaluate *expression* and return ``(result, formatted_multibase_string)``."""
    result = safe_eval(expression, context)
    return result, format_result(result)


# ─── Interactive TUI REPL ────────────────────────────────────────────────────

_BANNER = """\
\033[1;36m┌──────────────────────────────────────────────────────────┐
│                   cryptx  calculator                     │
├──────────────────────────────────────────────────────────┤
│  Operators   +  -  *  /  //  %  **                       │
│  Bitwise     &  |  ^  ~  <<  >>                          │
│  Bases       0xff (hex)  0b11 (bin)  0o77 (oct)          │
│  Variables   ans = last result  ·  x = <expr>            │
│  Commands    help · vars · clear · quit                  │
└──────────────────────────────────────────────────────────┘\033[0m"""

_HELP = """\
\033[1mExamples:\033[0m
  0xff + 1            arithmetic on hex
  0b1111 & 0b1010     bitwise AND
  (0xdead << 16) | 0xbeef
  ~0xff               bitwise NOT
  2 ** 32 - 1         exponentiation
  x = 0xdeadbeef      store in variable
  ans >> 16           use last result

\033[1mCommands:\033[0m
  help    show this message
  vars    list stored variables
  clear   clear the screen
  quit    exit (also q, exit, Ctrl-D)"""


def calc_repl() -> None:
    """Run an interactive calculator REPL with history and variables."""
    # Enable readline history / line editing (available on macOS and Linux)
    try:
        import readline  # noqa: F401
    except ImportError:
        pass

    print(_BANNER)
    context: dict[str, int | float] = {}

    while True:
        try:
            line = input("\033[1;33m»\033[0m ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not line:
            continue

        # ── special commands ──
        if line in ("quit", "q", "exit"):
            break
        if line == "help":
            print(_HELP)
            continue
        if line == "clear":
            sys.stdout.write("\033[2J\033[H")
            sys.stdout.flush()
            print(_BANNER)
            continue
        if line == "vars":
            if not context:
                print("  \033[2m(no variables)\033[0m")
            else:
                for name, val in context.items():
                    print(f"  \033[1m{name}\033[0m = {val}  ({hex(int(val)) if isinstance(val, int) else val})")
            continue

        # ── variable assignment: name = expr ──
        match = _ASSIGN_RE.match(line)
        if match:
            var_name, expr = match.group(1), match.group(2)
            try:
                result = safe_eval(expr, context)
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                context[var_name] = result
                context["ans"] = result
                print(format_result(result))
            except (ValueError, ZeroDivisionError, OverflowError) as exc:
                print(f"  \033[31mError: {exc}\033[0m")
            continue

        # ── expression evaluation ──
        try:
            result = safe_eval(line, context)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            context["ans"] = result
            print(format_result(result))
        except (ValueError, ZeroDivisionError, OverflowError) as exc:
            print(f"  \033[31mError: {exc}\033[0m")

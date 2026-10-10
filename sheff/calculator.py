"""Multi-base calculator with bitwise operations.

Safely evaluates arithmetic and bitwise expressions containing integers
in decimal, hex (0x), octal (0o), and binary (0b) notation.

Supported operators:
  Arithmetic:  +  -  *  /  //  %  **
  Bitwise:     &  |  ^  ~  <<  >>
"""

import ast
import operator


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


def _eval_node(node: ast.AST) -> int | float:
    """Recursively evaluate an AST node using only safe operators."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_func = _SAFE_OPS.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        return op_func(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_func = _SAFE_OPS.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        return op_func(operand)

    raise ValueError(
        f"Unsupported expression node: {type(node).__name__}. "
        "Only arithmetic and bitwise operations on literal numbers are allowed."
    )


def safe_eval(expression: str) -> int | float:
    """Parse and safely evaluate a mathematical / bitwise expression.

    Accepts integers in any Python-supported base:
      - Decimal:  255
      - Hex:      0xff
      - Octal:    0o377
      - Binary:   0b11111111

    Raises ValueError on unsupported syntax (no function calls, no variables).
    """
    try:
        tree = ast.parse(expression.strip(), mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression: {exc.msg}") from exc
    return _eval_node(tree)


def format_result(value: int | float) -> str:
    """Format a numeric result in decimal, hex, octal, and binary."""
    if isinstance(value, float) and not value.is_integer():
        return f"Dec:  {value}"

    n = int(value)
    lines = [
        f"Dec:  {n}",
        f"Hex:  {hex(n)}",
        f"Oct:  {oct(n)}",
        f"Bin:  {bin(n)}",
    ]
    return "\n".join(lines)


def calculate(expression: str) -> tuple[int | float, str]:
    """Evaluate *expression* and return ``(result, formatted_multibase_string)``."""
    result = safe_eval(expression)
    return result, format_result(result)

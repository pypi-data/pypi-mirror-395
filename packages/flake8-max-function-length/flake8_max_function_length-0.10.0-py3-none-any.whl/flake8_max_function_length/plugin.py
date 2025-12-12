import ast
from tokenize import TokenInfo
from typing import List, Optional, Union

from flake8.options.manager import OptionManager

FuncDef = Union[ast.FunctionDef, ast.AsyncFunctionDef]


class Plugin:
    name = "flake8-max-function-length"
    version = "0.10.0"

    def __init__(self, tree, file_tokens):
        self.tree = tree
        self.file_tokens = file_tokens

    def run(self):
        functions = [
            node
            for node in ast.walk(self.tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]
        for func in functions:
            func_length = get_function_length(
                func,
                self.file_tokens,
                self.include_function_definition,
                self.include_docstring,
                self.include_empty_lines,
                self.include_comment_lines,
            )
            if func_length > self.max_length:
                msg = f"MFL000: Function too long ({func_length} > {self.max_length})"
                yield func.lineno, func.col_offset, msg, type(self)

    @classmethod
    def add_options(cls, options_manager: OptionManager):
        def int_gte_1(max_length):
            value = int(max_length)
            if value < 1:
                raise ValueError
            return value

        options_manager.add_option(
            "--max-function-length",
            dest="max_length",
            type=int_gte_1,
            default=50,
            parse_from_config=True,
            help="Maximum allowed function length. (Default: %(default)s)",
            metavar="n",
        )
        options_manager.add_option(
            "--mfl-include-function-definition",
            dest="include_function_definition",
            default=False,
            action="store_true",
            parse_from_config=True,
            help=(
                "Include the function definition line(s) when calculating the "
                "function length. (Default: disabled)"
            ),
        )
        options_manager.add_option(
            "--mfl-include-docstring",
            dest="include_docstring",
            default=False,
            action="store_true",
            parse_from_config=True,
            help=(
                "Include the length of the docstring when calculating the "
                "function length. (Default: disabled)"
            ),
        )
        options_manager.add_option(
            "--mfl-include-empty-lines",
            dest="include_empty_lines",
            default=False,
            action="store_true",
            parse_from_config=True,
            help=(
                "Include empty lines inside the function when calculating the "
                "function length. (Default: disabled)"
            ),
        )
        options_manager.add_option(
            "--mfl-include-comment-lines",
            dest="include_comment_lines",
            default=False,
            action="store_true",
            parse_from_config=True,
            help=(
                "Include comment lines when calculating the function length. "
                "(Default: disabled)"
            ),
        )

    @classmethod
    def parse_options(cls, options):
        cls.max_length = options.max_length
        cls.include_function_definition = options.include_function_definition
        cls.include_docstring = options.include_docstring
        cls.include_empty_lines = options.include_empty_lines
        cls.include_comment_lines = options.include_comment_lines


def get_function_length(
    func: FuncDef,
    file_tokens: List[TokenInfo],
    include_func_def=False,
    include_docstring=False,
    include_empty_lines=False,
    include_comment_lines=False,
) -> int:
    func_start, func_end = func.lineno, func.end_lineno

    if not include_func_def:
        func_start = func.body[0].lineno

    func_length = func_end - func_start + 1

    if not include_docstring and (docstring := get_docstring(func)):
        func_length -= docstring.end_lineno - docstring.lineno + 1

    if not include_empty_lines:
        tokens = get_function_tokens(file_tokens, func_start, func_end)
        empty_lines = {token.start[0] for token in tokens if not token.line.strip()}
        func_length -= len(empty_lines)

    if not include_comment_lines:
        tokens = get_function_tokens(file_tokens, func_start, func_end)
        comment_lines = {
            token.start[0] for token in tokens if token.line.strip().startswith("#")
        }
        func_length -= len(comment_lines)

    return func_length


def get_docstring(func: FuncDef) -> Optional[ast.Expr]:
    # Check if the first element in the function body is a docstring or not.
    # This check is based on ast.get_docstring
    has_docstring = (
        isinstance(func.body[0], ast.Expr)
        and isinstance(func.body[0].value, ast.Constant)
        and isinstance(func.body[0].value.value, str)
    )
    if has_docstring:
        return func.body[0]


def get_function_tokens(
    file_tokens: List[TokenInfo], start: int, end: int
) -> List[TokenInfo]:
    return [token for token in file_tokens if start <= token.start[0] <= end]

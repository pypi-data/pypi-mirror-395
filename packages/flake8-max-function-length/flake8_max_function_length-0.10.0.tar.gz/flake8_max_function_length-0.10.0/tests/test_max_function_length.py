import pathlib
from typing import List, Tuple
from unittest.mock import MagicMock

from flake8.processor import FileProcessor

from flake8_max_function_length.plugin import Plugin


def test_function_length_no_error():
    result = get_results("sample_function.py", max_length=15)
    assert result == []


def test_function_length_with_func_def():
    result = get_results(
        "sample_function.py", max_length=15, include_function_definition=True
    )
    assert result == [(1, 0, "MFL000: Function too long (22 > 15)")]


def test_function_length_with_docstring():
    result = get_results("sample_function.py", max_length=14, include_docstring=True)
    assert result == [(1, 0, "MFL000: Function too long (15 > 14)")]


def test_function_length_with_empty_lines():
    result = get_results("sample_function.py", max_length=15, include_empty_lines=True)
    assert result == [(1, 0, "MFL000: Function too long (18 > 15)")]


def test_function_length_with_comment_lines():
    result = get_results(
        "sample_function.py", max_length=15, include_comment_lines=True
    )
    assert result == [(1, 0, "MFL000: Function too long (16 > 15)")]


def test_async_function_length_no_error():
    result = get_results("sample_async_function.py", max_length=15)
    assert result == []


def test_async_function_length_with_func_def():
    result = get_results(
        "sample_async_function.py", max_length=15, include_function_definition=True
    )
    assert result == [(1, 0, "MFL000: Function too long (22 > 15)")]


def test_async_function_length_with_docstring():
    result = get_results(
        "sample_async_function.py", max_length=14, include_docstring=True
    )
    assert result == [(1, 0, "MFL000: Function too long (15 > 14)")]


def test_async_function_length_with_empty_lines():
    result = get_results(
        "sample_async_function.py", max_length=15, include_empty_lines=True
    )
    assert result == [(1, 0, "MFL000: Function too long (18 > 15)")]


def test_async_function_length_with_comment_lines():
    result = get_results(
        "sample_async_function.py", max_length=15, include_comment_lines=True
    )
    assert result == [(1, 0, "MFL000: Function too long (16 > 15)")]


def test_method_length_no_error():
    result = get_results("sample_method.py", max_length=15)
    assert result == []


def test_method_length_with_func_def():
    result = get_results(
        "sample_method.py", max_length=15, include_function_definition=True
    )
    assert result == [(2, 4, "MFL000: Function too long (23 > 15)")]


def test_method_length_with_docstring():
    result = get_results("sample_method.py", max_length=15, include_docstring=True)
    assert result == [(2, 4, "MFL000: Function too long (19 > 15)")]


def test_method_length_with_empty_lines():
    result = get_results("sample_method.py", max_length=15, include_empty_lines=True)
    assert result == [(2, 4, "MFL000: Function too long (18 > 15)")]


def test_method_length_with_comment_lines():
    result = get_results("sample_method.py", max_length=15, include_comment_lines=True)
    assert result == [(2, 4, "MFL000: Function too long (16 > 15)")]


def test_async_method_length_no_error():
    result = get_results("sample_async_method.py", max_length=15)
    assert result == []


def test_async_method_length_with_func_def():
    result = get_results(
        "sample_async_method.py", max_length=15, include_function_definition=True
    )
    assert result == [(2, 4, "MFL000: Function too long (23 > 15)")]


def test_async_method_length_with_docstring():
    result = get_results(
        "sample_async_method.py", max_length=15, include_docstring=True
    )
    assert result == [(2, 4, "MFL000: Function too long (19 > 15)")]


def test_async_method_length_with_empty_lines():
    result = get_results(
        "sample_async_method.py", max_length=15, include_empty_lines=True
    )
    assert result == [(2, 4, "MFL000: Function too long (18 > 15)")]


def test_async_method_length_with_comment_lines():
    result = get_results(
        "sample_async_method.py", max_length=15, include_comment_lines=True
    )
    assert result == [(2, 4, "MFL000: Function too long (16 > 15)")]


def get_results(filename: str, **options) -> List[Tuple[int, int, str]]:
    current_dir = pathlib.Path(__file__).parent.resolve()
    full_file_path = current_dir / filename

    mocked_options = get_mocked_options(**options)
    processor = FileProcessor(str(full_file_path), mocked_options)
    plugin = Plugin(processor.build_ast(), processor.file_tokens)
    plugin.parse_options(mocked_options)

    return [
        # retrieve position of the error and the msg only
        (lineno, col_offset, msg)
        for lineno, col_offset, msg, _ in plugin.run()
    ]


def get_mocked_options(**options):
    mock = MagicMock()
    defaults = {
        "max_length": 50,
        "include_function_definition": False,
        "include_docstring": False,
        "include_empty_lines": False,
        "include_comment_lines": False,
    }
    for option, default in defaults.items():
        setattr(type(mock), option, options.get(option, default))

    return mock

# Standard library imports
from io import TextIOWrapper
import typing as t


def chunks(seq, size) -> t.Iterable:
    """
    Iterate through `seq` in `size` chunks
    """
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def write_comment(f: TextIOWrapper, text: str) -> None:
    """
    Write comment in following form:

    /**
     * text
    **/
    """
    f.write(generate_comment(text))


def generate_comment(text: str) -> str:
    """
    Generate comment in following form:

    /**
     * text
    **/
    """
    return (
        "/**\n"
        f" * {text}\n"
        "**/\n"
    )

#MTG3 - MR3: negating the input reverses the negated output.

if __name__ == "__main__":
    import sys
    from pathlib import Path

    _ROOT = Path(__file__).resolve().parents[1]
    sys.path[:0] = [str(_ROOT), str(_ROOT / "src")]

from tests._mr_checks import SOURCE_INPUTS  # noqa: E402
from tests._mr_checks import check_mr3_negation  # noqa: E402


def test_mtg_3():
    for index, source_input in enumerate(SOURCE_INPUTS):
        print(f"Running MTG3.{index + 1}:")
        check_mr3_negation(source_input)
        print("MR3 passed for input:", source_input)
        print("--------------------------------")


if __name__ == "__main__":
    test_mtg_3()

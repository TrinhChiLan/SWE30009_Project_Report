#MTG4 - MR4: duplicating the input duplicates each output element.

if __name__ == "__main__":
    import sys
    from pathlib import Path

    _ROOT = Path(__file__).resolve().parents[1]
    sys.path[:0] = [str(_ROOT), str(_ROOT / "src")]

from tests._mr_checks import SOURCE_INPUTS  # noqa: E402
from tests._mr_checks import check_mr4_duplication  # noqa: E402


def test_mtg_4():
    for index, source_input in enumerate(SOURCE_INPUTS):
        print(f"Running MTG4.{index + 1}:")
        check_mr4_duplication(source_input)
        print("MR4 passed for input:", source_input)
        print("--------------------------------")


if __name__ == "__main__":
    test_mtg_4()

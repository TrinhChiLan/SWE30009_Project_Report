#MTG5 - MR5: inserting new min/max bounds extends the output.

if __name__ == "__main__":
    import sys
    from pathlib import Path

    _ROOT = Path(__file__).resolve().parents[1]
    sys.path[:0] = [str(_ROOT), str(_ROOT / "src")]

from tests._mr_checks import SOURCE_INPUTS  # noqa: E402
from tests._mr_checks import check_mr5_boundary_insertion  # noqa: E402


def test_mtg_5():
    for index, source_input in enumerate(SOURCE_INPUTS):
        print(f"Running MTG5.{index + 1}:")
        check_mr5_boundary_insertion(source_input)
        print("MR5 passed for input:", source_input)
        print("--------------------------------")


if __name__ == "__main__":
    test_mtg_5()

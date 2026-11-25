#MTG2 - MR2: an affine transform (2x+3) of the input applies to the output.

if __name__ == "__main__":
    import sys
    from pathlib import Path

    _ROOT = Path(__file__).resolve().parents[1]
    sys.path[:0] = [str(_ROOT), str(_ROOT / "src")]

from tests._mr_checks import SOURCE_INPUTS  # noqa: E402
from tests._mr_checks import check_mr2_affine_transformation  # noqa: E402


def test_mtg_2():
    for index, source_input in enumerate(SOURCE_INPUTS):
        print(f"Running MTG2.{index + 1}:")
        check_mr2_affine_transformation(source_input)
        print("MR2 passed for input:", source_input)
        print("--------------------------------")


if __name__ == "__main__":
    test_mtg_2()

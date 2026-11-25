#MTG1 - MR1: permutation of the input must not change the output.

if __name__ == "__main__":
    import sys
    from pathlib import Path

    _ROOT = Path(__file__).resolve().parents[1]
    sys.path[:0] = [str(_ROOT), str(_ROOT / "src")]

from tests._mr_checks import SOURCE_INPUTS  
from tests._mr_checks import check_mr1_permutation  


def test_mtg_1():
    for index, source_input in enumerate(SOURCE_INPUTS):
        print(f"Running MTG1.{index + 1}:")
        check_mr1_permutation(source_input)
        print("MR1 passed for input:", source_input)
        print("--------------------------------")


if __name__ == "__main__":
    test_mtg_1()

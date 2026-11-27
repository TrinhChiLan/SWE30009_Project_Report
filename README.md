# SWE30009 Project Report — Metamorphic Testing of QuickSort

Metamorphic testing (MT) of a recursive QuickSort implementation, with pytest and
mutmut.

- **Program under test:** `src/Quick_Sort.py` — in-place `quickSort(arr, low, high)`
  backed by a Lomuto-style `partition`.
- **Test technique:** five metamorphic relations (MRs), grouped as MTG1–MTG5.
- **Tools:** pytest (test runner), mutmut (mutation testing), coverage.

> **Why metamorphic?** A QuickSort has a trivial oracle — `sorted(x)`. The MRs are
> not justified by beating that oracle (they don't); they demonstrate the technique
> that generalises to programs where no oracle exists. The mutation results are
> covered in [Results](#results).

---

## What the tests do

Each test takes a **source input**, runs it through `quickSort`, then produces a
**follow-up input** with a known relationship to the source and checks that the two
outputs satisfy the same relationship. The implementation is never compared against
a hard-coded expected answer.

### Metamorphic relations

| Group | File | Relation applied to input `x` | Assertion |
|---|---|---|---|
| **MTG1** | `tests/test_mtg_1.py` | shuffle: `x' = shuffled(x)` | `out(x') == out(x)` |
| **MTG2** | `tests/test_mtg_2.py` | affine: `x' = [2v + 3 for v in x]` | `out(x') == [2v + 3 for v in out(x)]` |
| **MTG3** | `tests/test_mtg_3.py` | negate: `x' = [-v for v in x]` | `out(x') == [-v for v in reversed(out(x))]` |
| **MTG4** | `tests/test_mtg_4.py` | duplicate: `x' = x + x` | `out(x') == [v for v in out(x) for _ in (0, 1)]` |
| **MTG5** | `tests/test_mtg_5.py` | insert bounds: `x' = [max+10] + x[:mid] + [min-10] + x[mid:]` | `out(x') == [min-10] + out(x) + [max+10]` |

Rationale:

- **MR1 (permutation).** A sort is a function of the *multiset* of its input. Reordering
  the input must not change the output.
- **MR2 (affine).** `2v+3` is strictly increasing, so it preserves every comparison and
  the list length. `out` should commute with it.
- **MR3 (negation).** Negation reverses order, so the output must be the negated and
  reversed source output.
- **MR4 (duplication).** Concatenating a list with itself doubles every element's
  multiplicity; each output element must appear twice as often.
- **MR5 (boundary insertion).** Adding a new maximum at the front and a new minimum in
  the middle must not disturb the existing ordering: they sort to the ends.

### Shared inputs

Every MR runs over the same seven source inputs (`tests/_mr_checks.py`):

| # | Input | Category |
|---|---|---|
| 1 | `[5, 12, 4, 1, 6, 5, 6, 11, 11, 1]` | Unsorted, with duplicates |
| 2 | `[5, 6, 7, 8, 9, 10, 11, 12]` | Already ascending |
| 3 | `[20, 19, 18, 17, 16, 15, 14, 12, 11]` | Descending |
| 4 | `[2, 2, 2, 2, 2, 2, 2]` | All identical |
| 5 | `[0, -5, -2, 5, 8, -9, -10, 4]` | Mixed signs and zero |
| 6 | `[]` | Empty |
| 7 | `[6, 2]` | Short / descending pair |

Each test asserts its relation for all seven inputs (7 source + 7 follow-up runs per MR).

> **Note on empty input.** MR5 cannot take `min`/`max` of an empty list, so it
> substitutes `0` and `99` as the bounds for that one case.

---

## Quickstart

### 1. Install

```bash
git clone https://github.com/TrinhChiLan/SWE30009_Project_Report.git
cd SWE30009_Project_Report

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
```

### 2. Run the tests

```bash
pytest                     # all five MRs
pytest -v                  # one line per MTG
pytest tests/test_mtg_2.py # a single MTG
```

Expected:

```
.....                                                                    [5/5]
5 passed in 0.02s
```

Each helper also prints the source and follow-up values, so a failure shows
exactly which transformation broke:

```
Source input: [6, 2] Follow-up Input: [15, 7]
Source output: [2, 6] Follow-up Output: [7, 15]
MR2 passed for input: [6, 2]
```

### 3. Mutation testing

mutmut 3 has **no CLI flag** for choosing which tests to run — the selection is read
from `pyproject.toml`:

```toml
[tool.mutmut]
pytest_add_cli_args_test_selection = ["tests"]              # all five MRs
# pytest_add_cli_args_test_selection = ["tests/test_mtg_2.py::test_mtg_2"]   # one MTG
```

Then:

```bash
mutmut run        # mutate src/Quick_Sort.py, run the selected tests
mutmut results    # survivors only
mutmut results --all true   # every mutant with its status
mutmut show <mutant-name>   # the diff for one mutant
mutmut browse     # interactive TUI
```

> **Changing the selection between runs:** mutmut caches verdicts in `mutants/`. When
> you switch `pytest_add_cli_args_test_selection`, timings change and `_mr_checks.py`
> is treated as a new dependency, so mutmut re-runs stats — but results from the
> previous selection can persist. Delete the tree when in doubt:
>
> ```bash
> rm -rf mutants && mutmut run
> ```

---

## Results

`src/Quick_Sort.py` produces **46 mutants**. Running the **full suite** kills **44**:

```
46/46  🎉 44 🫥 0  ⏰ 0  🤔 0  🙁 2  🔇 0  🧙 0
```

| MTG | Relation | Killed | Survived | Score |
|---|---|---|---|---|
| MTG1 | permutation | 44 | 2 | 95.7% |
| **MTG2** | **affine `2v+3`** | **38** | **8** | **82.6%** |
| MTG3 | negation | 44 | 2 | 95.7% |
| MTG4 | duplication | 44 | 2 | 95.7% |
| MTG5 | boundary insertion | 44 | 2 | 95.7% |
| **All five** | | **44** | **2** | **95.7%** |

### The 2 survivors common to every MR

| Mutant | Change | Nature |
|---|---|---|
| `Quick_Sort.x_quickSort__mutmut_3` | `if low < high:` → `low <= high:` | **Equivalent mutant.** Recursing on a one-element range calls `partition(low, low)`, which returns `low`; both recursive calls are immediately no-ops. Identical output for every input. |
| `Quick_Sort.x_partition__mutmut_9` | `if arr[j] <= pivot:` → `arr[j] < pivot:` | **Output-equivalent under black-box testing.** Only changes where pivot-equal elements land. The array is still sorted correctly (verified over all 5,461 arrays of length 0–6). Killable only by asserting `partition`'s internal contract. |

### MR2 is the weakest relation

The six mutants killed by every MR *except* MR2 are all **ordering or indexing** faults:

| Mutant | Change | Bug produced |
|---|---|---|
| `x_partition__mutmut_15` | `arr[i+1]` → `arr[i-1]` (target) | Writes the wrong slot |
| `x_partition__mutmut_17` | `arr[i+1]` → `arr[i-1]` (source) | Corrupts the array |
| `x_quickSort__mutmut_1` | `len(arr) == 1` → `!= 1` | Returns input unsorted |
| `x_quickSort__mutmut_2` | `len(arr) == 1` → `== 2` | Two-element lists unsorted |
| `x_quickSort__mutmut_18` | `pi-1` → `pi-2` | Skips an element |
| `x_quickSort__mutmut_26` | `pi+1` → `pi+2` | Skips an element |

`2v+3` is an order-preserving bijection. It changes the **values** but preserves
**relative order, length, and equality** — exactly the properties sorting depends on.
The algorithm therefore executes the *identical* control flow on `x` and `x'`, so a
reproducible bug appears on both sides of the relation and cancels:

```
x        = [5, 12, 4, 1, 6, 5, 6, 11, 11, 1]
out(x)   = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]          # mutmut_17: every element becomes 1
x'       = [13, 27, 11, 5, 15, 13, 15, 25, 25, 5]
out(x')  = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]          # ...and 2·1+3 = 5
2v+3 for v in out(x) = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]   # MR2 PASSES
```

The other four MRs each vary a property the bug *is* sensitive to — MR1 order, MR3
inverted order, MR4 multiplicity, MR5 bounds — which is why they catch all six.

**Takeaway:** MR2 adds little detection power beyond MR1 for a comparison sort. It
varies the least disruptive dimension.

### Relation to a direct oracle

QuickSort has a cheap oracle (`sorted()`), which would kill 44/46 too. The MRs are
not justified by superior fault detection; they mirror the oracle's kill rate while
using no oracle, and would remain the only available check for a program where
`sorted()` does not exist.

---

## Alternative mutation workflow

`pyproject.toml` holds a **single** selection, so mutating each MTG separately means
editing it between runs and clearing `mutants/` each time (see the cache note above).

If you want arbitrary per-MTG runs without touching `pyproject.toml`, use
**`pytest`'s `-k` / node-id selection with a fresh tree per run**:

```bash
for n in 1 2 3 4 5; do
  rm -rf mutants
  # edit pyproject.toml -> ["tests/test_mtg_$n.py::test_mtg_$n"]
  mutmut run
  mutmut results
done
```

---

## Project layout

```
.
├── pyproject.toml          # pytest + mutmut configuration (single source of truth)
├── requirements-dev.txt    # pinned pytest / coverage / mutmut
├── src/
│   └── Quick_Sort.py       # program under test
└── tests/
    ├── _mr_checks.py       # shared inputs + the five MR checks
    ├── test_mtg_1.py       # MTG1 — permutation
    ├── test_mtg_2.py       # MTG2 — affine 2v+3
    ├── test_mtg_3.py       # MTG3 — negation
    ├── test_mtg_4.py       # MTG4 — duplication
    └── test_mtg_5.py       # MTG5 — boundary insertion
```

Each MTG has its own module so it can be run, and selected for mutation, in
isolation.

### Import conventions (important)

The code is imported as the **bare module** `Quick_Sort`, and `src/` and the project
root are on `sys.path` via `pythonpath = [".", "src"]`:

```python
from Quick_Sort import quickSort
```

This mirrors how mutmut imports the mutant. Two constraints follow:

- **Do not import it as `src.Quick_Sort`.** mutmut copies `src/` to `mutants/src/`
  and imports the mutant as `Quick_Sort`; an `src.`-prefixed import makes the
  recursive calls dispatch into the *original* module, and mutmut aborts with
  `Failed trampoline hit. Module name starts with 'src.'`.
- **Do not add `tests/__init__.py` or `tests/conftest.py`.** The suite relies on
  `consider_namespace_packages = true` so modules resolve as `tests._mr_checks`. A
  package would make pytest record `tests.test_mtg_N` while mutmut knows the file as
  `Quick_Sort`, and every mutant would report **No Tests**.

---

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `ModuleNotFoundError: No module named 'Quick_Sort'` | The `ModuleNotFoundError` in a test helper means `src/` is not on `sys.path`. The test modules add it themselves, so they work standalone; only a *new* helper would need `sys.path.insert(0, ".../src")`. |
| `mutmut results` shows `0.00 mutations/second` | Verdicts were loaded from cache, not executed. The numbers are stale — `rm -rf mutants` and re-run. |
| Every mutant says **No Tests** | A `tests/__init__.py` or `tests/conftest.py` was added (see [Import conventions](#import-conventions-important)). |
| `Failed trampoline hit. Module name starts with 'src.'` | A test imports `src.Quick_Sort` instead of `Quick_Sort`. |
| Mutation numbers changed after editing `SOURCE_INPUTS` | mutmut tracks function bodies, not module-level constants. Delete `mutants/` before re-running. |

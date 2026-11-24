import copy
import random
from Quick_Sort import quickSort

def run_quicksort(arr):
    data = copy.deepcopy(arr)
    if len(data) > 0:
        quickSort(data, 0, len(data) - 1)
    return data

SOURCE_INPUTS = [
    [5, 12, 4, 1, 6, 5, 6, 11, 11, 1], #Unsorted, mixed with duplicates.
    [5, 6, 7, 8, 9, 10, 11, 12], #Sorted in ascending order.
    [20, 19, 18, 17, 16, 15, 14, 12, 11], #Sorted in descending order.
    [2, 2, 2, 2, 2, 2, 2], #All identical elements.
    [0, -5, -2, 5, 8, -9, -10, 4] #Mixed positive and negative numbers and zero.
]

def test_mr1_permutation(source_input):
    source_out = run_quicksort(source_input)
    shuffled = source_input.copy()
    random.Random(42).shuffle(shuffled)
    shuffled_out = run_quicksort(shuffled)
    print("Source input:", source_input, "Follow-up Input:", shuffled)
    print("Source output:", source_out, "Follow-up Output:", shuffled_out)
    assert sorted(shuffled_out) == sorted(source_out)

def test_mr2_affine_transformation(source_input):
    source_out = run_quicksort(source_input)
    scaled = [2 * x + 3 for x in source_input]
    scaled_out = run_quicksort(scaled)
    print("Source input:", source_input, "Follow-up Input:", scaled)
    print("Source output:", source_out, "Follow-up Output:", scaled_out)
    assert scaled_out == [2 * x + 3 for x in source_out]

def test_mr3_negation(source_input):
    source_out = run_quicksort(source_input)
    negated = [-x for x in source_input]
    negated_out = run_quicksort(negated)
    print("Source input:", source_input, "Follow-up Input:", negated)
    print("Source output:", source_out, "Follow-up Output:", negated_out)
    assert negated_out == [-x for x in reversed(source_out)]

def test_mr4_duplication(source_input):
    source_out = run_quicksort(source_input)
    duplicated = source_input + source_input
    expected = [x for x in source_out for _ in (0, 1)]
    duplicated_out = run_quicksort(duplicated)
    print("Source input:", source_input, "Follow-up Input:", duplicated)
    print("Source output:", source_out, "Follow-up Output:", duplicated_out)
    assert duplicated_out == expected

def test_mr5_boundary_insertion(source_input):
    source_out = run_quicksort(source_input)
    min_val = min(source_input) - 10
    max_val = max(source_input) + 10
    mid = len(source_input) // 2
    injected = [max_val] + source_input[:mid] + [min_val] + source_input[mid:]
    injected_out = run_quicksort(injected)
    print("Source input:", source_input, "Follow-up Input:", injected)
    print("Source output:", source_out, "Follow-up Output:", injected_out)
    assert injected_out == [min_val] + source_out + [max_val]

def mtg_1():
    for index, source_input in enumerate(SOURCE_INPUTS):
        print(f"Running MTG1.{index + 1}:")
        test_mr1_permutation(source_input)
        print("MR1 passed for input:", source_input)
        print("--------------------------------")

def mtg_2():
    for index, source_input in enumerate(SOURCE_INPUTS):
        print(f"Running MTG2.{index + 1}:")
        test_mr2_affine_transformation(source_input)
        print("MR2 passed for input:", source_input)
        print("--------------------------------")

def mtg_3():
    for index, source_input in enumerate(SOURCE_INPUTS):
        print(f"Running MTG3.{index + 1}:")
        test_mr3_negation(source_input)
        print("MR3 passed for input:", source_input)
        print("--------------------------------")

def mtg_4():
    for index, source_input in enumerate(SOURCE_INPUTS):
        print(f"Running MTG4.{index + 1}:")
        test_mr4_duplication(source_input)
        print("MR4 passed for input:", source_input)
        print("--------------------------------")

def mtg_5():
    for index, source_input in enumerate(SOURCE_INPUTS):
        print(f"Running MTG5.{index + 1}:")
        test_mr5_boundary_insertion(source_input)
        print("MR5 passed for input:", source_input)
        print("--------------------------------")

mtg_1()
mtg_2()
mtg_3()
mtg_4()
mtg_5()
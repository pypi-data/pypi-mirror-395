from typing import List

from mitos.scripts.update_hmm import Hit, filter_best_per_target


# helper function to create a Hit
def make_hit(
    target: str, query: str, evalue: float, score: float, line: str = ""
) -> Hit:
    return {
        "target": target,
        "query": query,
        "evalue": evalue,
        "score": score,
        "line": line,
    }


def test_empty_list():
    best, discarded = filter_best_per_target([])
    assert best == []
    assert discarded == []


def test_single_hit():
    hits: List[Hit] = [make_hit("t1", "q1", 1e-5, 50)]
    best, discarded = filter_best_per_target(hits)
    assert best == hits
    assert discarded == []


def test_two_hits_same_target_different_evalue():
    h1: Hit = make_hit("t1", "q1", 1e-5, 50)
    h2: Hit = make_hit("t1", "q1", 1e-6, 40)
    best, discarded = filter_best_per_target([h1, h2])
    assert best == [h2]
    assert discarded == [h1]


def test_two_hits_same_target_same_evalue_different_score():
    h1: Hit = make_hit("t1", "q1", 1e-5, 50)
    h2: Hit = make_hit("t1", "q1", 1e-5, 60)
    best, discarded = filter_best_per_target([h1, h2])
    assert best == [h2]
    assert discarded == [h1]


def test_tie_same_evalue_and_score():
    h1: Hit = make_hit("t1", "q1", 1e-5, 50)
    h2: Hit = make_hit("t1", "q1", 1e-5, 50)
    best, discarded = filter_best_per_target([h1, h2])
    assert best == [h1]  # first Hit stays
    assert discarded == [h2]  # second Hit gets discarded


def test_multiple_targets():
    h1: Hit = make_hit("t1", "q1", 1e-5, 50)
    h2: Hit = make_hit("t2", "q1", 1e-6, 40)
    h3: Hit = make_hit("t1", "q1", 1e-6, 45)
    best, discarded = filter_best_per_target([h1, h2, h3])

    # each target should exist exactly once in best
    best_targets = {h["target"] for h in best}
    assert best_targets == {"t1", "t2"}

    assert h3 in best
    assert h2 in best
    assert discarded == [h1]


def test_sorted_output():
    h1: Hit = make_hit("t1", "q2", 1e-5, 50)
    h2: Hit = make_hit("t2", "q1", 1e-4, 40)
    h3: Hit = make_hit("t3", "q1", 1e-6, 55)
    h4: Hit = make_hit("t4", "q3", 1e-3, 60)
    best, _ = filter_best_per_target([h1, h2, h3, h4])
    # should be sorted by query first, then evalue
    assert best == [h3, h2, h1, h4]

from .interval import union, contains, excluding, overlapping, excludingco, complements, remove_overlapping_intervals
from . import test_interval_data as cases

def test_union():
    for x, y, z in cases.union:
        assert union(x, y) == z

def test_contains():
    for x, y, z in cases.contains:
        assert contains(x, y) == z

def test_overlapping():
    for x, y, z in cases.overlapping:
        assert overlapping(x, y) == z

def test_excluding():
    for x, y, z in cases.excluding:
        assert excluding(x, y) == z

def test_excludingco():
    for x, y, z in cases.excludingco:
        assert excludingco(x, y) == z

def test_complements():
    for x, y, z in cases.complements:
        assert complements(x, y) == z

def test_remove_overlapping_intervals():
    for x, y in cases.remove_overlapping_intervals:
        assert remove_overlapping_intervals(x) == y

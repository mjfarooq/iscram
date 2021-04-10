import dd.cudd as _bdd

import pytest

from iscram.domain.model import SystemGraph
from iscram.domain.metrics.bdd_functions import (
    build_bdd, bdd_prob
)


def test_smoke_build_bdd(simple_or: SystemGraph):
    bdd, root = build_bdd(simple_or)
    assert bdd is not None


def test_prob_ex_rauzy_1():
    vars = ["a", "c", "b"]
    r_expr = "(a | c) & (b | c)"

    bdd = _bdd.BDD()
    bdd.declare(*vars)
    r = bdd.add_expr(r_expr)
    x = {v: 0.5 for v in vars}

    assert bdd_prob(bdd, r, x, dict()) == .625


def test_prob_ex_nasa_1():
    # NASA Fault Tree Handbook pp.VIII-12 - VIII-14
    vars = ["T", "K_2", "S", "S_1", "K_1", "R"]

    r_expr = "T | K_2 | (S & S_1) | (S & K_1) | (S & R)"

    bdd = _bdd.BDD()
    bdd.declare(*vars)
    r = bdd.add_expr(r_expr)
    x = {
        "T": 5e-6,
        "K_2": 3e-5,
        "S": 1e-4,
        "S_1": 3e-5,
        "K_1": 3e-5,
        "R": 1e-4
    }
    assert pytest.approx(bdd_prob(bdd, r, x, dict()) == 3.4e-5)


def test_prob_ex_sinnamon_1():
    # pg 217, 1996 RAMS
    vars = ["x1", "x2", "x3", "x4"]

    bdd = _bdd.BDD()
    bdd.declare(*vars)
    r_expr = "ite(x1, ite(x2, ite(x3, TRUE, ite(x4, TRUE, FALSE)), ite(x3, TRUE, FALSE)), FALSE)"
    r = bdd.add_expr(r_expr)

    p = {
        "x1": 0.01,
        "x2": 0.02,
        "x3": 0.03,
        "x4": 0.04
    }

    ''' 
    minimal cutsets:
        x1, x2, x3
        x1, x2, x4
        x1, x3
    '''
    assert pytest.approx(bdd_prob(bdd, r, p, dict()) == 3.0776e-4)


def test_prob_negated_edge_basic():
    r_expr = "a & ~b"
    bdd = _bdd.BDD()
    bdd.declare('a', 'b')
    r = bdd.add_expr(r_expr)

    x = {"a": 0.5, "b": 0.25}
    assert (bdd_prob(bdd, r, x, dict()) == 0.375)


def test_prob_negated_edge_basic_2():
    r_expr = "a & ~(b | ~c)"
    bdd = _bdd.BDD()
    bdd.declare('a', 'b', 'c')
    r = bdd.add_expr(r_expr)

    x = {"a": 0.5, "b": 0.25, "c" : 0.125}
    assert (bdd_prob(bdd, r, x, dict()) == 0.046875)
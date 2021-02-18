from iscram.domain.metrics.importance import (
    birnbaum_importance, birnbaum_structural_importance
)
from iscram.domain.model import (
    SystemGraph, Component, Indicator, RiskRelation
)


def test_birnbaum_importance_simple_and():
    components = frozenset({Component(1, "one", "and"),
                            Component(2, "two", "and"),
                            Component(3, "three", "and")})

    indicator = Indicator("and", frozenset({RiskRelation(3, -1)}))

    deps = frozenset({RiskRelation(1, 3), RiskRelation(2, 3)})

    sg = SystemGraph("simple", components, frozenset(), deps, frozenset(), indicator)

    b_imps = birnbaum_importance(sg)

    assert b_imps == {1: 0.0, 2: 0.0, 3: 1.0}


def test_birnbaum_structural_importance_simple_and():
    components = frozenset({Component(1, "one", "and"),
                            Component(2, "two", "and"),
                            Component(3, "three", "and")})

    indicator = Indicator("and", frozenset({RiskRelation(3, -1)}))

    deps = frozenset({RiskRelation(1, 3), RiskRelation(2, 3)})

    sg = SystemGraph("simple", components, frozenset(), deps, frozenset(), indicator)

    b_imps = birnbaum_structural_importance(sg)

    assert b_imps == {1: 0.25, 2: 0.25, 3: 0.75}

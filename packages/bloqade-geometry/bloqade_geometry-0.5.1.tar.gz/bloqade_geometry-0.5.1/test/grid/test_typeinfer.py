from typing import Any, Literal

from kirin import types
from kirin.dialects import ilist

from bloqade.geometry.dialects import grid
from bloqade.geometry.prelude import geometry


def test_typeinfer_1():

    @geometry(typeinfer=True)
    def test_1(spacing: ilist.IList[float, Literal[2]]):
        return grid.new(spacing, [1.0, 2.0], 0.0, 0.0)

    assert test_1.return_type.is_subseteq(
        grid.GridType[types.Literal(3), types.Literal(3)]
    )


def test_typeinfer_2():
    @geometry(typeinfer=True)
    def test_2(spacing: ilist.IList[float, Any]):
        return grid.new(spacing, [1.0, 2.0], 0.0, 0.0)

    assert test_2.return_type.is_subseteq(grid.GridType[types.Any, types.Literal(3)])


def test_typeinfer_get_index_1():
    @geometry(typeinfer=True, fold=False)
    def test_1():
        g = grid.from_positions([0.0, 3.0, 5.0], [0.0, 1.0, 2.0])
        return g[1:-1, :5]

    assert test_1.return_type.is_subseteq(grid.GridType)


def test_typeinfer_get_index_2():
    @geometry(typeinfer=True, fold=False)
    def test_1():
        g = grid.from_positions([0.0, 3.0, 5.0], [0.0, 1.0, 2.0])
        return g[1, :5]

    assert test_1.return_type.is_subseteq(grid.GridType[types.Literal(1), types.Any])


def test_typeinfer_get_index_3():
    @geometry(typeinfer=True, fold=False)
    def test_1(idx: ilist.IList[int, Any]):
        g = grid.from_positions([0.0, 3.0, 5.0], [0.0, 1.0, 2.0])
        return g[1, idx]

    assert test_1.return_type.is_subseteq(grid.GridType[types.Literal(1), types.Any])


def test_typeinfer_get_index_4():
    @geometry(typeinfer=True, fold=False)
    def test_1(idx: ilist.IList[int, Any]):
        g = grid.from_positions([0.0, 3.0, 5.0], [0.0, 1.0, 2.0])
        return g[[1, 2], idx]

    assert test_1.return_type.is_subseteq(grid.GridType[types.Literal(2), types.Any])

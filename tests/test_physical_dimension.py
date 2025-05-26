import pytest
from gci.model import physical_dimension_prompt
from gci.model import physical_dimension_no_prompt


def test_1d_dimension_prompt(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "1")
    assert physical_dimension_prompt() == 1.0


def test_2d_dimension_prompt(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "2")
    assert physical_dimension_prompt() == 1.0/2


def test_3d_dimension_prompt(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "3")
    assert physical_dimension_prompt() == 1.0/3


def test_1d_dimension_no_prompt():
    dimension_1d = "1"
    f_2d = physical_dimension_no_prompt(dimension_1d)
    assert f_2d == 1.0


def test_2d_dimension_no_prompt():
    dimension_2d = "2"
    f_2d = physical_dimension_no_prompt(dimension_2d)
    assert f_2d == 1.0/2


def test_3d_dimension_no_prompt():
    dimension_3d = "3"
    f_3d = physical_dimension_no_prompt(dimension_3d)
    assert f_3d == 1.0/3


def test_wrong_input_string_no_prompt():
    with pytest.raises(TypeError):
        physical_dimension_no_prompt("three-dimensional")


def test_wrong_input_float_no_prompt():
    with pytest.raises(TypeError):
        physical_dimension_no_prompt(2.0)


def test_wrong_input_end_of_line_no_prompt():
    with pytest.raises(TypeError):
        physical_dimension_no_prompt("\n")

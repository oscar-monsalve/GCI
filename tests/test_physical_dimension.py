import pytest
from gci.model import physical_dimension_prompt
from gci.model import physical_dimension_no_prompt


def test_2d_dimension_prompt(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "2D")
    assert physical_dimension_prompt() == 1/2
    monkeypatch.setattr("builtins.input", lambda _: "2d")
    assert physical_dimension_prompt() == 1/2


def test_3d_dimension_prompt(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "3D")
    assert physical_dimension_prompt() == 1/3
    monkeypatch.setattr("builtins.input", lambda _: "3d")
    assert physical_dimension_prompt() == 1/3


def test_wrong_input_string_prompt(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "three-dimensional")
    with pytest.raises(TypeError):
        physical_dimension_prompt()


def test_wrong_input_float_prompt(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: 1.0)
    with pytest.raises(TypeError):
        physical_dimension_prompt()


def test_wrong_input_end_of_line_prompt(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "\n")
    with pytest.raises(TypeError):
        physical_dimension_prompt()


def test_2d_dimension_no_prompt():
    dimension_2d, dimension_2D = "2d", "2D"
    f_2d = physical_dimension_no_prompt(dimension_2d)
    f_2D = physical_dimension_no_prompt(dimension_2D)
    assert f_2d == 1/2
    assert f_2D == 1/2


def test_3d_dimension_no_prompt():
    dimension_3d, dimension_3D = "3d", "3D"
    f_3d = physical_dimension_no_prompt(dimension_3d)
    f_3D = physical_dimension_no_prompt(dimension_3D)
    assert f_3d == 1/3
    assert f_3D == 1/3


def test_wrong_input_string_no_prompt():
    with pytest.raises(TypeError):
        physical_dimension_no_prompt("three-dimensional")


def test_wrong_input_float_no_prompt():
    with pytest.raises(TypeError):
        physical_dimension_no_prompt(2.0)


def test_wrong_input_end_of_line_no_prompt():
    with pytest.raises(TypeError):
        physical_dimension_no_prompt("\n")

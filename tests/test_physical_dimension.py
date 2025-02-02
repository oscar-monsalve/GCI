import pytest
from gci.model import physical_dimension_no_prompt


def test_2d_dimension():
    dimension_2d, dimension_2D = "2d", "2D"
    f_2d = physical_dimension_no_prompt(dimension_2d)
    f_2D = physical_dimension_no_prompt(dimension_2D)
    assert f_2d == 1/2
    assert f_2D == 1/2


def test_3d_dimension():
    dimension_3d, dimension_3D = "3d", "3D"
    f_3d = physical_dimension_no_prompt(dimension_3d)
    f_3D = physical_dimension_no_prompt(dimension_3D)
    assert f_3d == 1/3
    assert f_3D == 1/3


def test_wrong_input_int():
    with pytest.raises(TypeError):
        physical_dimension_no_prompt(2)


def test_wrong_input_float():
    with pytest.raises(TypeError):
        physical_dimension_no_prompt(2.0)


def test_wrong_input_incorrect_string():
    with pytest.raises(TypeError):
        physical_dimension_no_prompt("three-dimensional")


def test_wrong_input_end_of_line():
    with pytest.raises(TypeError):
        physical_dimension_no_prompt("\n")

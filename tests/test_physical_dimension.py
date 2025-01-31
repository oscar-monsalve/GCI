from gci.model import physical_dimension_no_prompt


def test_physical_dimension_prompt_2d():
    dimension_2d, dimension_2D = "2d", "2D"
    f_2d = physical_dimension_no_prompt(dimension_2d)
    f_2D = physical_dimension_no_prompt(dimension_2D)
    assert f_2d == 1/2
    assert f_2D == 1/2


def test_physical_dimension_prompt_3d():
    dimension_3d, dimension_3D = "3d", "3D"
    f_3d = physical_dimension_no_prompt(dimension_3d)
    f_3D = physical_dimension_no_prompt(dimension_3D)
    assert f_3d == 1/3
    assert f_3D == 1/3

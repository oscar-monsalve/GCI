from gci.model import physical_dimension_no_prompt


def test_physical_dimension_prompt_2d():
    dimension = "2d"
    f = physical_dimension_no_prompt(dimension)
    assert f == 1/2

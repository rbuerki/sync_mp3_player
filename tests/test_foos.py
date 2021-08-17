from src import foos


def test_compare_dicts_1(source_dict, target_dict):
    result = foos.compare_dicts(source_dict, source_dict)
    assert result[0] == result[1] == result[2] == []


def test_compare_dicts_2(source_dict, target_dict):
    result = foos.compare_dicts(source_dict, target_dict)
    assert (
        result[0] == ["new"]
        and result[1] == ["updated"]
        and result[2] == ["deleted"]
    )

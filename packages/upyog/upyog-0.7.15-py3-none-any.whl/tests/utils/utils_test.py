from upyog.utils.utils import is_collection


def test_collection():
    assert is_collection([1, 2, 3])  # True
    assert is_collection((1, 2, 3))  # True
    assert not is_collection("string")  # False
    assert not is_collection(123)  # False
    assert is_collection({'a': 1})  # True
    assert is_collection({1, 2, 3})  # True

import pytest

# Assuming the example function and other methods are imported from your module
from polly.help import example, checkclass, get_fun_name, checkpath, lookfor


class Polly:
    __name__ = "Polly"


class OmixAtlas:
    __name__ = "OmixAtlas"


class Workspaces:
    __name__ = "Workspaces"


def test_example_function():
    # Testing with Polly class
    example(Polly)
    # Test for valid function name
    example(Polly, function_name="get_all_omixatlas()")
    # Test for invalid function name
    example(Polly, function_name="invalid_function")

    # Test with other allowed classes
    example(OmixAtlas)
    example(Workspaces)


def test_checkclass():
    # Test allowed classes
    checkclass(Polly)
    checkclass(OmixAtlas)
    checkclass(Workspaces)

    # Test disallowed class
    with pytest.raises(Exception):

        class InvalidClass:
            __name__ = "Invalid"

        checkclass(InvalidClass)


def test_get_fun_name():
    # Test extracting function name from string with parentheses
    assert get_fun_name("get_all_omixatlas()") == "get_all_omixatlas"
    # Test for string without parentheses
    assert get_fun_name("get_all_omixatlas") == "get_all_omixatlas"
    # Test for empty string
    assert get_fun_name("") is None


def test_checkpath():
    # Test for public function
    assert checkpath("valid_function") is True
    # Test for private function
    assert checkpath("_private_function") is False


def test_lookfor():
    # Assuming 'polly' is the module we are looking into
    result = lookfor("polly", True)
    assert result is not None
    assert isinstance(result, list)

    # Test that it returns non-empty results for known valid cases
    found = False
    for item in result:
        if "class" in item[1] or "func" in item[1]:
            found = True
            break
    assert found

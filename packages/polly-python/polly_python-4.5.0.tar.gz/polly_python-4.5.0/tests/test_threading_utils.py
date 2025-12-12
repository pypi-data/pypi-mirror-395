import pytest
from unittest.mock import patch, MagicMock
from polly.threading_utils import for_each_threaded, FailureLimitError


def test_successful_run():
    """Test that the function runs successfully when no errors occur."""
    items = [1, 2, 3]
    fn = MagicMock()
    for_each_threaded(items, fn)
    assert fn.call_count == len(items)


def test_failure_limit_error():
    """Test that the function raises `FailureLimitError` when the error percentage exceeds `max_error_perc`."""
    items = [1, 2, 3, 4, 5]
    fn = MagicMock(side_effect=[None, Exception(), None, Exception(), Exception()])
    with pytest.raises(FailureLimitError):
        for_each_threaded(items, fn, max_error_perc=0.4)


def test_empty_items():
    """Test that the function handles empty items without errors."""
    fn = MagicMock()
    for_each_threaded([], fn)
    fn.assert_not_called()


def test_keyboard_interrupt():
    """Test that the function cancels remaining tasks upon `KeyboardInterrupt`."""
    items = [1, 2, 3]
    fn = MagicMock()
    with patch("polly.threading_utils.ThreadPoolExecutor") as mock_executor:
        mock_executor.return_value.__enter__.return_value.submit.side_effect = (
            KeyboardInterrupt
        )
        with pytest.raises(KeyboardInterrupt):
            for_each_threaded(items, fn)

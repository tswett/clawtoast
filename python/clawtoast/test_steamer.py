import pytest

from clawtoast import steamer

@pytest.mark.xfail()
def test_can_run_connect_to_nucleo() -> None:
    steamer.connect_to_nucleo()

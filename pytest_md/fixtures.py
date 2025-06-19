import pytest


extras_stash_key = pytest.StashKey[list]()


@pytest.fixture
def extras(pytestconfig):
    """Add details to the HTML reports.

    .. code-block:: python

        import pytest_html


        def test_foo(extras):
            extras.append(pytest_html.extras.url("https://www.example.com/"))
    """
    pytestconfig.stash[extras_stash_key] = []
    yield pytestconfig.stash[extras_stash_key]
    del pytestconfig.stash[extras_stash_key][:]

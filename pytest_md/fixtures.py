import pytest


extras_stash_key = pytest.StashKey[list]()
metrics_stash_key = pytest.StashKey[list]()

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

@pytest.fixture
def metrics(pytestconfig):
    """Add metrics to be displayed in MLFlow runs.
    For example:
    .. code-block:: python

        def test_foo(metrics):
            metrics.append(("accuracy", 0.95))
            metrics.append(("loss", 0.05))

    """
    pytestconfig.stash[metrics_stash_key] = []
    yield pytestconfig.stash[metrics_stash_key]
    del pytestconfig.stash[metrics_stash_key][:]
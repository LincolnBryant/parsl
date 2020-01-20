import parsl
from parsl.app.app import python_app


@python_app
def slow_double(x):
    import time
    time.sleep(0.1)
    return x * 2


def test_garbage_collect():
    """ Launches an app with a dependency and waits till it's done and asserts that
    the internal refs were wiped
    """
    x = slow_double(slow_double(10))

    if x.done() is False:
        assert parsl.dfk().tasks[x.tid]['app_fu'] == x, "Tasks table should have app_fu ref before done"

    x.result()
    parsl.dfk().checkpoint()

    assert parsl.dfk().tasks[x.tid]['app_fu'] is None, "Tasks should have app_fu ref wiped after task completion"


if __name__ == '__main__':

    from parsl.tests.configs.htex_local_alternate import config
    parsl.load(config)
    # parsl.load()
    test_garbage_collect()
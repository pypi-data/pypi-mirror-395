from tomwer.core.utils.time import Timer


def test_timer():
    with Timer("timer name"):
        pass

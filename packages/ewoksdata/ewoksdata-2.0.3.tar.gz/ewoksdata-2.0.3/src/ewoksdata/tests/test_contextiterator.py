from ..data import contextiterator


def test_context_iterator():

    exited = False

    @contextiterator.contextiterator
    def iterator():
        nonlocal exited
        exited = False
        try:
            yield from [1, 2, 3]
        finally:
            exited = True

    # Use like a normal iterator
    it = iterator()
    assert next(it) == 1
    assert not exited

    # Use like a context iterator
    with iterator() as it:
        assert next(it) == 1
        assert not exited
    assert exited


def test_context_generator():

    @contextiterator.contextiterator
    def generator():
        nonlocal exited
        exited = False
        try:
            while True:
                x = yield
                yield x * 2
        finally:
            exited = True

    # Use like a normal generator
    exited = False
    gen = generator()
    assert next(gen) is None  # run up to first yield
    assert not exited
    assert gen.send(10) == 20
    assert next(gen) is None
    assert gen.send(15) == 30
    assert not exited

    # Use like a context iterator
    exited = False
    with generator() as gen:
        assert next(gen) is None
        assert not exited
        assert gen.send(10) == 20
        assert next(gen) is None
        assert gen.send(15) == 30
        assert not exited
    assert exited

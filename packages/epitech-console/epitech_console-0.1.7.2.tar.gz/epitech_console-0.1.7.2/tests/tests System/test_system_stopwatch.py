import pytest
import time


from epitech_console.System import StopWatch


def test_stopwatch_default_start_false(
    ) -> None:
    sw = StopWatch()
    assert sw._start == 0.0
    assert sw == 0.0


def test_stopwatch_start_and_stop(
    ) -> None:
    sw = StopWatch()
    sw.start()
    time.sleep(0.05)
    sw.stop()

    assert 0.05 < sw < 0.06


def test_stopwatch_elapsed_manual_update(
    ) -> None:
    sw = StopWatch(start=True)
    time.sleep(0.05)
    elapsed = sw.elapsed(auto_update=True)

    assert elapsed >= 0.05


def test_stopwatch_reset(
    ) -> None:
    sw = StopWatch(start=True)
    time.sleep(0.02)
    sw.stop()
    sw.reset()

    assert sw == 0.0
    assert sw._start == 0.0


def test_stopwatch_double_start(
    ) -> None:
    sw = StopWatch(start=True)
    old_start = sw._start
    time.sleep(0.02)
    sw.start()  # Should restart

    assert sw._start != old_start
    assert sw == 0.0


def test_stopwatch_update(
    ) -> None:
    sw = StopWatch(start=True)
    time.sleep(0.03)
    sw.update()

    assert sw > 0.0

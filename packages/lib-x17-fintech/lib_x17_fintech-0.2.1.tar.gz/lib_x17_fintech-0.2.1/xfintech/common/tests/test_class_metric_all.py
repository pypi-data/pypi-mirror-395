import pandas as pd

from xfintech.common.metric import Metric


def test_metric_start_finish():
    m = Metric("test")
    m.start()
    assert m.start_at is not None

    m.finish()
    assert m.finish_at is not None
    assert m.duration >= 0


def test_metric_mark():
    m = Metric("mark_test")
    m.start()
    m.mark("stage1")
    m.mark("stage2")
    assert "stage1" in m.marks
    assert "stage2" in m.marks
    assert isinstance(m.marks["stage1"], pd.Timestamp)


def test_metric_describe():
    m = Metric("describe_test")
    m.start()
    m.mark("step1")
    m.finish()
    info = m.describe()
    assert info["name"] == "describe_test"
    assert info["started_at"] is not None
    assert info["finished_at"] is not None
    assert "step1" in info["marks"]


def test_metric_to_dict():
    m = Metric("dict_test")
    m.start()
    m.finish()
    d = m.to_dict()
    assert d["name"] == "dict_test"
    assert isinstance(d["started_at"], pd.Timestamp)
    assert isinstance(d["finished_at"], pd.Timestamp)


def test_metric_context_manager_no_error():
    with Metric("cm_test") as m:
        pass  # do nothing

    assert m.start_at is not None
    assert m.finish_at is not None
    assert m.error == []


def test_metric_context_manager_with_error():
    try:
        with Metric("cm_error_test") as m:
            raise ValueError("bad")
    except ValueError:
        pass

    assert m.error != []
    assert any("ValueError" in line for line in m.error)


def test_metric_reset():
    m = Metric("reset_test")
    m.start()
    m.mark("a")
    m.finish()
    m.reset()
    assert m.start_at is None
    assert m.finish_at is None
    assert m.error == []
    assert m.marks == {}

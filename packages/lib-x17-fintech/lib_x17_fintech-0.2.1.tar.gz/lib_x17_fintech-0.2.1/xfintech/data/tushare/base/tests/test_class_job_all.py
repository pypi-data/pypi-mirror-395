import pandas as pd

from xfintech.common.output import Output
from xfintech.common.source import Source
from xfintech.data.tushare.base.job import Job


class DummySessionNoConn:
    pass


class DummySessionWithConn:
    def __init__(self):
        self.connection = object()


class DummyRetry:
    def __init__(self):
        self.calls = 0

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            self.calls += 1
            return func(*args, **kwargs)

        return wrapper

    def describe(self):
        return {"type": "dummy-retry"}

    def to_dict(self):
        return {"type": "dummy-retry"}


class DummyConf:
    def __init__(self, limit=5, size=3):
        self.limit = limit
        self.size = size
        self.offset = 0
        self.cool_calls = 0

    def reset(self):
        self.offset = 0

    def next(self):
        self.offset += self.size

    def cool(self):
        self.cool_calls += 1

    def describe(self):
        return {
            "limit": self.limit,
            "size": self.size,
            "offset": self.offset,
            "cool_calls": self.cool_calls,
        }

    def to_dict(self):
        return self.describe()


class DummyJob(Job):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.run_called = False
        self.run_result = None

    def _run(self):
        self.run_called = True
        self.run_result = {"status": "ok"}
        return self.run_result


def test_job_basic_init_defaults():
    job = Job(session=DummySessionNoConn())
    assert isinstance(job.id, str)
    assert len(job.id) == 8
    assert job.name == "job"
    assert job.connected is False
    assert isinstance(job.source, Source)
    assert isinstance(job.output, Output)
    assert job.source.name == job.name
    assert job.output.name == job.name

    metric_info = job.metric.describe()
    cache_info = job.cache.describe()
    assert "duration" in metric_info
    assert "name" in cache_info


def test_job_custom_name_and_tags():
    job = Job(
        session=DummySessionNoConn(),
        name="My-Job",
        tags={"project": "finance"},
    )
    assert job.name == "my-job"
    assert job.tags == {"project": "finance"}


def test_job_connection_detection():
    job = Job(session=DummySessionWithConn())
    assert job.connected is True
    assert job.connection is not None


def test_job_source_output_from_dict():
    src_dict = {
        "name": "src1",
        "url": "http://api",
        "args": {"a": 1},
        "tableinfo": {
            "desc": "test table",
            "columns": [
                {"name": "col1", "kind": "string"},
            ],
        },
    }
    out_dict = {
        "name": "out1",
        "tableinfo": {
            "desc": "out table",
            "columns": [
                {"name": "id", "kind": "integer"},
            ],
        },
    }
    job = Job(
        session=DummySessionNoConn(),
        source=src_dict,
        output=out_dict,
    )
    assert job.source.name == "src1"
    assert job.output.name == "out1"
    assert job.source.args["a"] == 1
    assert "col1" in job.source.tableinfo.columns
    assert "id" in job.output.tableinfo.columns


def test_job_run_uses_retry_and_metric():
    dummy_retry = DummyRetry()
    job = DummyJob(
        session=DummySessionNoConn(),
        retry=dummy_retry,
    )
    result = job.run()
    assert job.run_called is True
    assert result == {"status": "ok"}
    assert dummy_retry.calls == 1

    metric_info = job.metric.describe()
    assert "duration" in metric_info
    assert isinstance(metric_info["duration"], float)


def test_job_fetchall_pagination():
    data = pd.DataFrame({"x": list(range(7))})

    def api(limit: int, offset: int, **params) -> pd.DataFrame:
        return data.iloc[offset : offset + limit].reset_index(drop=True)

    dummy_conf = DummyConf(limit=10, size=3)
    job = DummyJob(
        session=DummySessionNoConn(),
        conf=dummy_conf,
    )
    df = job._fetchall(api, extra="ignored")
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 7
    assert df["x"].tolist() == list(range(7))
    assert job.conf.offset >= job.conf.size
    assert job.conf.cool_calls >= 1


def test_job_describe_and_to_dict_structure():
    dummy_retry = DummyRetry()
    dummy_conf = DummyConf()
    job = DummyJob(
        session=DummySessionWithConn(),
        name="test-job",
        retry=dummy_retry,
        conf=dummy_conf,
        tags={"env": "dev"},
    )
    info = job.describe()
    dct = job.to_dict()
    for payload in (info, dct):
        assert payload["id"] == job.id
        assert payload["name"] == job.name
        assert payload["connected"] is True
        assert "conf" in payload
        assert "retry" in payload
        assert "cache" in payload
        assert "metric" in payload
        assert payload["tags"] == {"env": "dev"}


def test_job_fetchall_empty_first_page():
    def api(limit: int, offset: int, **params) -> pd.DataFrame:
        return pd.DataFrame()

    dummy_conf = DummyConf(limit=5, size=3)
    job = DummyJob(
        session=DummySessionNoConn(),
        conf=dummy_conf,
    )
    df = job._fetchall(api)
    assert isinstance(df, pd.DataFrame)
    assert df.empty
    assert job.conf.offset == 0


def test_job_fetchall_respects_limit():
    data = pd.DataFrame({"x": list(range(100))})

    def api(limit: int, offset: int, **params) -> pd.DataFrame:
        return data.iloc[offset : offset + limit].reset_index(drop=True)

    dummy_conf = DummyConf(limit=2, size=10)
    job = DummyJob(
        session=DummySessionNoConn(),
        conf=dummy_conf,
    )
    df = job._fetchall(api)
    assert len(df) == 20


def test_job_keeps_given_source_and_output_instance():
    src = Source(name="custom-src")
    out = Output(name="custom-out")
    job = Job(
        session=DummySessionNoConn(),
        source=src,
        output=out,
    )
    assert job.source is src
    assert job.output is out

from datetime import datetime

from xfintech.data.tushare.session.session import Session


def test_session_init_and_connect(monkeypatch):
    class FakePro:
        def __init__(self):
            self.connected = True

    monkeypatch.setattr("tushare.set_token", lambda token: None)
    monkeypatch.setattr("tushare.pro_api", lambda: FakePro())

    s = Session(credential="fake-token")

    assert s.connected
    assert isinstance(s.connection, FakePro)
    assert isinstance(s.start, datetime)
    assert s.finish is None
    assert "Session" in repr(s)


def test_session_disconnect(monkeypatch):
    monkeypatch.setattr("tushare.set_token", lambda token: None)
    monkeypatch.setattr("tushare.pro_api", lambda: object())

    s = Session(credential="fake-token")
    assert s.connected

    s.disconnect()
    assert not s.connected
    assert isinstance(s.finish, datetime)


def test_session_describe_and_to_dict(monkeypatch):
    monkeypatch.setattr("tushare.set_token", lambda token: None)
    monkeypatch.setattr("tushare.pro_api", lambda: object())

    s = Session(credential="fake-token")
    info1 = s.describe()

    assert isinstance(info1, dict)
    assert "connected" in info1

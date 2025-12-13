import pytest
import mock
from analyzer_socket import AnalyzerCmd
import socket
from unittest.mock import Mock
import json


@pytest.fixture
def create_instance_helper():
    with mock.patch('analyzer_socket.socket.socket'):
        obj = AnalyzerCmd(ip="192.168.2.67")
        obj.s.connect.assert_called_with(('192.168.2.67', 17000))
        return obj


@pytest.fixture
def send_helper(monkeypatch):
    send_mock = Mock()
    monkeypatch.setattr(socket.socket, "sendall", send_mock)
    # yield send_mock.assert_called_once()


@pytest.fixture
def recv_helper(monkeypatch):
    def recv_wrapper(byte_count):
        return b'\x00B{"cmd":"responseappcmd","ok":true,"p1":"startMeasuring","v":"2.7"}'
    monkeypatch.setattr(socket.socket, "recv", recv_wrapper)


@pytest.mark.parametrize("income, outcome", [(True, False), (False, True)])
def test_start_measuring(monkeypatch, income, outcome, create_instance_helper, send_helper, recv_helper):
    # Arrange
    fake_response = {"cmd": "responseappcmd",
                     "ok": income, "p1": "startMeasuring", "v": "2.7"}
    json_load_mock = Mock(return_value=fake_response)
    monkeypatch.setattr(json, "loads", json_load_mock)
    # send_helper.assert_called_once()
    # Act / Assert
    try:
        create_instance_helper.start_measuring()
    except Exception as exc:
        assert outcome

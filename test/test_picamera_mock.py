import pi_camera_capture.picamera_mock
from pi_camera_capture.cam import capture, cam


def test_mock_capture(monkeypatch):
    expected_length = 144
    stream = capture()
    assert stream.getbuffer().nbytes == 144

import io
from picamera import PiCamera

cam = PiCamera()
cam.rotation = 180
cam.resolution = (300, 300)


def capture():
    stream = io.BytesIO()
    cam.capture(stream, "jpeg", True)
    stream.seek(0)
    return stream
